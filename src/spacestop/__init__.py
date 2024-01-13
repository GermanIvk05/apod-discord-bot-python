import discord
from discord.ext import commands

from .__main__ import SpaceStop


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SpaceStop(bot))