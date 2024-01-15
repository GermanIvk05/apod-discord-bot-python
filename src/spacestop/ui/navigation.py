from datetime import date, datetime, timedelta

import discord

from .. import parser
from ..article import Article, create_embed_from, parse_media_and_article_from


class NotAValidDate(Exception):
    pass

def embed_to_video(url: str) -> str:
    """
    Contverts YouTube embed link to YouTube video link
    """
    return f"https://www.youtube.com/watch?v={url.split('/')[-1].split('?')[0]}"
    

def calulate_next_day(current_date: date) -> date:
    """
    Calculates the next calendar date
    """
    current_datetime = datetime.combine(current_date, datetime.min.time())
    next_datetime = current_datetime + timedelta(days=1)
    next_date = next_datetime.date()

    if not parser.is_valid_date(next_date):
        raise NotAValidDate
    
    return next_date


def calculate_previous_day(current_date: date) -> date:
    """
    Calculates the previous calendar date
    """
    current_datetime = datetime.combine(current_date, datetime.min.time())
    previous_datetime = current_datetime - timedelta(days=1)
    previous_date = previous_datetime.date()

    if not parser.is_valid_date(previous_date):
        raise NotAValidDate
    
    return previous_date


class Navigation(discord.ui.View):

    def __init__(self, article: Article) -> None:
        super().__init__()
        self.date = article.date
        self.youtube_button = None
        
        # if the article has a YouTube video, add a discord link button with URL to the YouTube video
        if article.media.is_video():
            self.youtube_button = discord.ui.Button(label="YouTube", url=embed_to_video(article.media.url), emoji="▶️")
            self.add_item(self.youtube_button)


    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        Shows previous APOD
        """
        try:
            self.date = calculate_previous_day(current_date=self.date)
            article = parse_media_and_article_from(data=parser.get_specific_APOD(date=self.date))

            if self.youtube_button is not None:
                self.remove_item(self.youtube_button)   # remove YouTube link button if exists

            # if the article has a YouTube video, add a discord link button with URL to the YouTube video
            if article.media.is_video():
                self.youtube_button = discord.ui.Button(label="YouTube", url=embed_to_video(article.media.url), emoji="▶️")
                self.add_item(self.youtube_button)

            # modify message with updated embed and article navigation view
            await interaction.response.edit_message(embed=create_embed_from(article), view=self)

        except NotAValidDate:
            await interaction.response.send_message(content="You reached the latest/oldest of Astronomy Picture of the Day!", ephemeral=True)


    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        Shows next APOD
        """
        try:
            self.date = calulate_next_day(current_date=self.date)
            article = parse_media_and_article_from(data=parser.get_specific_APOD(date=self.date))

            if self.youtube_button is not None:
                self.remove_item(self.youtube_button)   # remove YouTube link button if exists

            # if the article has a YouTube video, add a discord link button with URL to the YouTube video
            if article.media.is_video():
                self.youtube_button = discord.ui.Button(label="YouTube", url=embed_to_video(article.media.url), emoji="▶️")
                self.add_item(self.youtube_button)

            # modify message with updated embed and article navigation view
            await interaction.response.edit_message(embed=create_embed_from(article), view=self)

        except NotAValidDate:
            await interaction.response.send_message(content="You reached the latest/oldest of Astronomy Picture of the Day!", ephemeral=True)