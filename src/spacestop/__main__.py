import os
from datetime import date

import discord
from discord import app_commands
from discord.ext import commands

from . import parser
from .article import Article

API_KEY = os.getenv("NASA_APIKEY")


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)
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
        article = Article.from_response(parser.get_data(api_key=API_KEY))
        await article.send(interaction)

    @app_commands.command()
    async def random(self, interaction: discord.Interaction) -> None:
        """
        Get random APOD
        """
        article = Article.from_response(parser.get_data(api_key=API_KEY, count=1)[0])
        await article.send(interaction)
          
    @app_commands.command(name="date")
    async def get_date(self, interaction: discord.Interaction, day: str, month: str, year: str) -> None:
        """
        Get APOD for specific date
        """
        in_date = date(int(year), int(month), int(day))

        if not is_valid_date(in_date):
            return
            
        article = Article.from_response(
            parser.get_data(api_key=API_KEY, date=in_date.strftime("%Y-%m-%d"))
            )
        await article.send(interaction)


