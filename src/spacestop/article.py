from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional

import discord

from . import parser


@dataclass
class Media:
    type: str
    url: str
    thumbnail_url: Optional[str] = None
    copyright: Optional[str] = None

    def is_video(self) -> bool:
        return self.type == "video"
    
    def is_image(self) -> bool:
        return self.type == "image"
    
    def has_copyright(self) -> bool:
        return self.copyright is not None


def embed_to_video(url: str) -> str:
    """
    Contverts YouTube embed link to YouTube video link
    """
    return f"https://www.youtube.com/watch?v={url.split('/')[-1].split('?')[0]}"


@dataclass
class Article(discord.ui.View):
    title: str
    description: str
    content: Media
    date: date
    
    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Article:
        content = Media(
            type=parser.get_media_type(data),
            url=parser.get_hdurl(data) or parser.get_url(data),
            thumbnail_url=parser.get_thumbnail_url(data),
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

        if self.content.has_copyright():
            embed.set_footer(text=f"Image Credit & Copyright: {self.content.copyright}")

        if self.content.is_video():
            embed.set_thumbnail(url=self.content.thumbnail_url)

            # initialize the discord.ui.View to add a link button to YouTube
            super().__init__()
            self.add_item(discord.ui.Button(label="YouTube", url=embed_to_video(self.content.url), emoji="▶️"))
            await interaction.response.send_message(embed=embed, view=self)
        else:
            embed.set_image(url=self.content.url)
            await interaction.response.send_message(embed=embed)