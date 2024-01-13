from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional

import discord
from discord.ext import commands

from . import parser


@dataclass
class Media:
    type: str
    url: str
    copyright: Optional[str] = None

    def is_video(self) -> bool:
        return self.type == "video"
    
    def is_image(self) -> bool:
        return self.type == "image"
    
    def has_copyright(self) -> bool:
        return self.copyright is not None
    

@dataclass
class Article:
    title: str
    description: str
    content: Media
    date: date
    
    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Article:
        content = Media(
            type=parser.get_media_type(data),
            url=parser.get_hdurl(data) or parser.get_url(data),
            copyright=parser.get_copyright(data)
        )
        return cls(
            title=parser.get_title(data),
            description=parser.get_explaination(data),
            content=content,
            date=datetime.strptime(parser.get_date(data), "%Y-%m-%d")
        )

    async def send(self, interaction: discord.Interaction) -> discord.Embed:
        embed = discord.Embed(title=self.title, description=self.description)
        embed.set_author(name=self.date.strftime("%d %b %Y"))

        if self.content.is_image():
            embed.set_image(url=self.content.url)

        if self.content.has_copyright():
            embed.set_footer(text=f"Image Credit & Copyright: {self.content.copyright}")

        await interaction.response.send_message(embed=embed)

        if self.content.is_video():
            await interaction.response.send_message(self.content.url)