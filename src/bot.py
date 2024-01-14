"""
Based on one of the examples from https://github.com/Rapptz/discord.py
"""

import asyncio
import logging
import logging.handlers
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


description = '''
Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.
'''

class SpaceBot(commands.Bot):

    def __init__(self, *args, initial_extensions: list[str], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # TODO: implement a check to sync only when the changes are made
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s).")


async def main() -> None:
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    extensions = ["spacestop"]
    intents = discord.Intents.default()
    async with SpaceBot(
        commands.when_mentioned,
        initial_extensions=extensions, 
        description=description,
        intents=intents
    ) as bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())