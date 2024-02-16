import os
from datetime import date, datetime, timedelta
from typing import Dict, Any

from discord.ext import commands
from discord import app_commands
import discord

from nasa.apod import APODClient, DateOutOfRangeError


def create_apod_embed(apod_data: Dict[str, Any]) -> discord.Embed:
    # Ensure necessary keys exist
    if 'date' not in apod_data or 'title' not in apod_data or 'explanation' not in apod_data:
        raise ValueError("APOD data is missing required keys.")

    apod_date = date.fromisoformat(apod_data['date'])
    apod_url = f'https://apod.nasa.gov/apod/ap{apod_date.strftime("%y%m%d")}.html'

    embed = discord.Embed(
        color=discord.Color.dark_purple(),
        title=apod_data['title'],
        url=apod_url,
        description=apod_data['explanation']
    )

    if copyright := apod_data.get('copyright'):
        embed.add_field(name='Copyright', value=copyright, inline=True)     # todo: make a formatter

    if apod_data.get('media_type') == 'video':
        embed.set_thumbnail(url=apod_data.get('thumbnail_url'))
    else:
        embed.set_image(url=apod_data.get('hdurl') or apod_data.get('url'))

    embed.set_footer(text=apod_date.strftime("%d %b %Y"))
    return embed


class Navigation(discord.ui.View):
    """
    A class representing a navigation view for Astronomy Picture of the Day (APOD) within a Discord bot interface.

    This view includes interactive buttons to navigate through APOD entries by date and displays the selected entry.

    Attributes:
        apod_client: The client instance used to fetch APOD data.
        apod_date (datetime): The current date for which the APOD is being displayed.
        message: The Discord message object associated with the view. Used for editing the message after timeout.

    Parameters:
        apod_client: An initialized client for accessing the APOD API.
        apod_date (datetime): The initial date for the APOD to display.
    """

    def __init__(self, apod_client, apod_date: datetime) -> None:
        """
        Initializes the Navigation view with the APOD client and the specified date.

        :param apod_client: The APOD client used to fetch APOD entries.
        :param apod_date: The date of the APOD entry to initially display.
        """
        super().__init__(timeout=15)
        self.apod_client = apod_client
        self.apod_date = apod_date
        self.youtube_button = None  # todo: update the doc string
        self.message = None

    async def fetch_and_display_new_apod(self, interaction, days: int):
        """
        Fetches and displays a new APOD entry based on the navigation direction indicated by the user.

        :param interaction: The Discord interaction object representing the user's interaction with the navigation
        button.
        :param days: An integer indicating the direction and magnitude of the date change. Positive for
        future dates, negative for past dates.
        """
        initial_date = self.apod_date
        self.apod_date += timedelta(days=days)
        try:
            new_apod = self.apod_client.get(self.apod_date.date(), True)
            if new_apod.get('media_type') == 'video':
                if self.youtube_button is not None:
                    self.remove_item(self.youtube_button)

                self.youtube_button = discord.ui.Button(style=discord.ButtonStyle.url,
                                                        label='YouTube',
                                                        url=new_apod['url'],
                                                        emoji='▶️')
                self.add_item(self.youtube_button)
            await interaction.response.edit_message(embed=create_apod_embed(new_apod), view=self)
        except DateOutOfRangeError as e:
            self.apod_date = initial_date
            await interaction.response.send_message(content=str(e), ephemeral=True)  # Handle date out of range

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.secondary, emoji='⬅️')
    async def prev(self, interaction, button: discord.ui.Button) -> None:
        """
        An asynchronous method triggered by pressing the 'Previous' button, navigating to the previous APOD entry.

        :param interaction: The Discord interaction object for this button press.
        :param button: The button instance that was pressed.
        """
        await self.fetch_and_display_new_apod(interaction, -1)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.secondary, emoji='➡️')
    async def next(self, interaction, button: discord.ui.Button) -> None:
        """
        An asynchronous method triggered by pressing the 'Next' button, navigating to the next APOD entry.

        :param interaction: The Discord interaction object for this button press.
        :param button: The button instance that was pressed.
        """
        await self.fetch_and_display_new_apod(interaction, 1)

    async def on_timeout(self) -> None:
        """
        An asynchronous method called when the view times out (after a period of inactivity).

        This method disables all interactive components in the view to prevent further interaction.
        """
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)


class AstronomyPictureOfTheDay(commands.Cog):
    """
    A Discord bot cog that fetches and displays the Astronomy Picture of the Day (APOD) from NASA's APOD API.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
        apod_client (APODClient): The client used to interact with the NASA APOD API.
    """
    def __init__(self, bot: commands.Bot, apod_client: APODClient) -> None:
        """
        Initializes the Astronomy Picture of the Day cog with a Discord bot and an APOD client.

        :param bot: The Discord bot instance.
        :param apod_client: The APOD client used to fetch astronomical pictures and information.
        """
        self.bot = bot
        self.apod_client = apod_client

    async def fetch_and_respond(self, interaction, **kwargs):
        """
        Fetches Astronomy Picture of the Day based on specified criteria and responds to a Discord interaction.

        :param interaction: The Discord interaction context to respond to.
        :param kwargs: Keyword arguments used for fetching APOD data, such as date or random selection.
        """
        try:
            count = kwargs.get('count')
            if count:
                data = self.apod_client.get_random(**kwargs)
                if count == 1:
                    nav_view = Navigation(self.apod_client, datetime.fromisoformat(data[0].get('date')))
                    if data[0].get('media_type') == 'video':
                        nav_view.youtube_button = discord.ui.Button(style=discord.ButtonStyle.url,
                                                                    label='YouTube',
                                                                    url=data[0]["url"],
                                                                    emoji='▶️')
                        nav_view.add_item(nav_view.youtube_button)
                    await interaction.response.send_message(embed=create_apod_embed(data[0]), view=nav_view)
                    nav_view.message = await interaction.original_response()
                else:
                    await interaction.response.send_message(embeds=[create_apod_embed(item) for item in data])
            else:
                data = self.apod_client.get(**kwargs)
                nav_view = Navigation(self.apod_client, datetime.fromisoformat(data.get('date')))
                if data.get('media_type') == 'video':
                    nav_view.youtube_button = discord.ui.Button(style=discord.ButtonStyle.url,
                                                                label='YouTube',
                                                                url=data["url"],
                                                                emoji='▶️')
                    nav_view.add_item(nav_view.youtube_button)
                await interaction.response.send_message(embed=create_apod_embed(data), view=nav_view)
                nav_view.message = await interaction.original_response()
        except DateOutOfRangeError as e:
            await interaction.response.send_message(content=str(e), ephemeral=True)

    @app_commands.command(
        name='today',
        description='Shows today\'s APOD-selected astronomical image and its explanation.'
    )
    async def get_today(self, interaction) -> None:
        """
        Responds to an interaction with today's Astronomy Picture of the Day, including its image and explanation.

        :param interaction: The Discord interaction context to respond to.
        """
        await self.fetch_and_respond(interaction, thumbs=True)

    @app_commands.command(
        name='random',
        description='Returns a random APOD astronomy picture and its backstory.'
    )
    async def get_random(self, interaction, count: int = 1) -> None:
        """
        Responds to an interaction with a random Astronomy Picture of the Day and its backstory.

        :param interaction: The Discord interaction context to respond to.
        :param count: The number of random APOD entries to fetch. Defaults to 1.
        """
        await self.fetch_and_respond(interaction, count=count, thumbs=True)

    @app_commands.command(
        name='date',
        description='Fetches the APOD astronomy picture of the day for a specified date.'
    )
    async def get_date(self, interaction, day: int, month: int, year: int) -> None:
        """
        Fetches and responds with the Astronomy Picture of the Day for a specified date.

        :param interaction: The Discord interaction context to respond to.
        :param day: The day of the month for the APOD.
        :param month: The month of the year for the APOD.
        :param year: The year for the APOD.
        """
        # todo: test ability of pydantic to parse dates
        await self.fetch_and_respond(interaction, when=date(year, month, day), thumbs=True)


async def setup(bot: commands.Bot) -> None:
    apod_client = APODClient(key=os.getenv('NASA_APIKEY'))
    await bot.add_cog(AstronomyPictureOfTheDay(bot, apod_client))
