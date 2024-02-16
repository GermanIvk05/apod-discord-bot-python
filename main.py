import asyncio
import logging
import logging.handlers
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def setup_logging():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log", encoding="utf-8", maxBytes=32 * 1024 * 1024, backupCount=5
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class SpaceStop(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:  # todo: implement commands loading and synchronization
        await self.load_extension('spacestop.apod')

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s).")


async def main() -> None:
    setup_logging()  # Configure logging
    logger = logging.getLogger("discord")

    logger.info('Starting the SpaceStop bot...')
    intents = discord.Intents.default()

    token = os.getenv('DISCORD_TOKEN')
    async with SpaceStop(command_prefix='', intents=intents) as bot:
        await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())
