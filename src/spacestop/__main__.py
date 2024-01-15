from datetime import date

import discord
from discord import app_commands
from discord.ext import commands

from . import parser
from .article import create_embed_from, parse_media_and_article_from
from .article_ui import Navigation


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)    # first Astronomy Picture Of the Day
    max_date = date.today()
    return max_date >= in_date >= min_date


class SpaceStop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def today(self, interaction: discord.Interaction) -> None:
        """
        Get today's APOD
        """
        article = article = parse_media_and_article_from(data=parser.get_today_APOD())
        await interaction.response.send_message(embed=create_embed_from(article), view=Navigation(article))

    @app_commands.command()
    async def random(self, interaction: discord.Interaction) -> None:
        """
        Get random APOD
        """
        article = parse_media_and_article_from(data=parser.get_random_APOD(count=1)[0])
        await interaction.response.send_message(embed=create_embed_from(article), view=Navigation(article))
          
    @app_commands.command(name="date")
    async def get_date(self, interaction: discord.Interaction, day: int, month: int, year: int) -> None:
        """
        Get APOD for specific date
        """
        in_date = date(year, month, day)

        if is_valid_date(in_date):
            article = parse_media_and_article_from(data=parser.get_specific_APOD(date=in_date))
            await interaction.response.send_message(embed=create_embed_from(article), view=Navigation(article))


