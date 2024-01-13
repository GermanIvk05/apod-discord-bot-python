import os
from datetime import date

import discord
from discord import app_commands
from discord.ext import commands

from .article import Article
from . import parser

API_KEY = os.getenv("NASA_APIKEY")


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)    # first Astronomy Pictire Of the Day
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
        article = Article.from_response(parser.get_data(thumbs=True, api_key=API_KEY))
        await article.send(interaction)

    @app_commands.command()
    async def random(self, interaction: discord.Interaction) -> None:
        """
        Get random APOD
        """
        article = Article.from_response(parser.get_data(count=1, thumbs=True, api_key=API_KEY)[0])
        await article.send(interaction)
          
    @app_commands.command(name="date")
    async def get_date(self, interaction: discord.Interaction, day: int, month: int, year: int) -> None:
        """
        Get APOD for specific date
        """
        in_date = date(year, month, day)

        if is_valid_date(in_date):
            article = Article.from_response(parser.get_data(date=in_date, thumbs=True, api_key=API_KEY))
            await article.send(interaction)


