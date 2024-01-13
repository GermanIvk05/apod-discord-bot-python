from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import discord
from discord.ext import commands

import apod_object_parser as apod_parser

API_KEY = os.getenv("NASA_APIKEY")

MEDIA_PARSER = {
    "image": apod_parser.get_hdurl,
    "video": apod_parser.get_url
}

@dataclass
class Media:
    type: str
    url: str

    def is_video(self) -> bool:
        return self.type == "video"
    
    def is_image(self) -> bool:
        return self.type == "image"


@dataclass
class Article:
    title: str
    description: str
    content: Media
    date: date
    copyright: Optional[str] = None


    @classmethod
    def from_data(cls, *, api_key="DEMO_KEY", **kwargs) -> Article:
        response = apod_parser.get_data(api_key=api_key, **kwargs)

        if isinstance(response, list):
            response = response[0]

        title = apod_parser.get_title(response)
        description = apod_parser.get_explaination(response)
        media_type = apod_parser.get_media_type(response)
        content = Media(media_type, MEDIA_PARSER[media_type](response))
        date = datetime.strptime(apod_parser.get_date(response), "%Y-%m-%d")
        copyright = apod_parser.get_copyright(response)
    
        return cls(title, description, content, date, copyright)
    
    
    async def send(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title=self.title, description=self.description)
        embed.set_author(name=self.date.strftime("%d %b %Y"))

        if self.content.is_image():
            embed.set_image(url=self.content.url)

        if self.copyright:
            embed.set_footer(text=f"Image Credit & Copyright: {self.copyright}")

        await ctx.send(embed=embed)

        if self.content.is_video():
            await ctx.send(content=self.content.url)


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)
    max_date = date.today()
    return max_date >= in_date >= min_date


class SpaceStop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self. bot = bot


    @commands.command()
    async def today(self, ctx: commands.Context) -> None:
        """
        Get today's APOD
        """
        article = Article.from_data(api_key=API_KEY)
        await article.send(ctx)


    @commands.command()
    async def random(self, ctx: commands.Context) -> None:
        """
        Get random APOD
        """
        article = Article.from_data(api_key=API_KEY, count=1)
        await article.send(ctx)
        
        
    @commands.command(name="date")
    async def get_date(self, ctx: commands.Context, day: str, month: str, year: str) -> None:
        """
        Get APOD for specific date
        """
        in_date = date(int(year), int(month), int(day))

        if not is_valid_date(in_date):
            return
            
        article = Article.from_data(api_key=API_KEY, date=in_date.strftime("%Y-%m-%d"))
        await article.send(ctx)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SpaceStop(bot))