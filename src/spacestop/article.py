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


@dataclass
class Article:
    title: str
    content: str
    media: Media
    date: date

    
def parse_media_and_article_from(data: dict[str, Any]) -> Article:
    media = Media(
        type=parser.get_media_type(data),
        url=parser.get_hdurl(data) or parser.get_url(data),
        thumbnail_url=parser.get_thumbnail_url(data),
        copyright=parser.get_copyright(data)
    )
    article = Article(
        title=parser.get_title(data),
        content=parser.get_explaination(data),
        media=media,
        date=datetime.strptime(parser.get_date(data), "%Y-%m-%d")
    )
    return article
    
    
def create_embed_from(article: Article) -> discord.Embed:
    embed = discord.Embed(
        title=article.title, 
        description=article.content, 
        url=f"https://apod.nasa.gov/apod/ap{article.date.strftime('%y%m%d')}.html"
        )

    embed.set_author(name=article.date.strftime("%d %b %Y"))

    if article.media.is_video():
        embed.set_thumbnail(url=article.media.thumbnail_url)
    else:
        embed.set_image(url=article.media.url)

    if article.media.has_copyright():
        embed.set_footer(text=f"Image Credit & Copyright: {article.media.copyright}")
    return embed