import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


description = '''
Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.
'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready() -> None:
    print(f" Logged on as {bot.user}!")
    await bot.load_extension("spacestop")

if __name__ == "__main__":
    bot.run(TOKEN)