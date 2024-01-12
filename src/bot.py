import os
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

import apod_object_parser as apod

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("NASA_APIKEY")


def create_apod_embed(
        title: str, description: str, 
        date: datetime,  copyright: Optional[str] = None
        ) -> discord.Embed:
    """
    Creates APOD discord embed
    """
    embed = discord.Embed(title=title, description=description)
    embed.set_author(name=date.strftime("%d %b %Y"))

    if copyright:
        embed.set_footer(text=f"Image Credit & Copyright: {copyright}")
    return embed
 

async def send_apod_embed(ctx, data) -> None:
    """
    Sends discord embed based on content type
    """
    embed = create_apod_embed(
        title=apod.get_title(data),
        description=apod.get_explaination(data),
        date=datetime.strptime(apod.get_date(data), "%Y-%m-%d"),
        copyright=apod.get_copyright(data)
    )

    media_type = apod.get_media_type(data)

    if media_type == "image":
        embed.set_image(url=apod.get_hdurl(data))
        
    await ctx.send(embed=embed)

    if media_type == "video":
        await ctx.send(apod.get_url(data))


description = '''
Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.
'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready() -> None:
    print(f" Logged on as {bot.user}!")


@bot.command()
async def today(ctx) -> None:
    """
    Get today's APOD
    """
    data = apod.get_data(api_key=API_KEY)
    await send_apod_embed(ctx, data)


@bot.command()
async def random(ctx) -> None:
    """
    Get random APOD
    """
    data = apod.get_data(api_key=API_KEY, count=1)[0]
    await send_apod_embed(ctx, data)
    


if __name__ == "__main__":
    bot.run(TOKEN)