import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import apod_object_parser as apod

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("NASA_APIKEY")


description = '''
Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.
'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f" Logged on as {bot.user}!")


@bot.command()
async def today(ctx) -> None:
    """
    Provides today's APOD
    """
    data = apod.get_data(API_KEY)

    embed = discord.Embed(title=apod.get_title(data), description=apod.get_explaination(data))
    embed.set_author(name=apod.get_date(data))
    embed.set_image(
        url=apod.get_hdurl(data) if apod.get_media_type(data) == "image" else apod.get_url(data)
        )
    embed.set_footer(text=f"Imagse Credit & Copyright: {apod.get_copyright(data)}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)