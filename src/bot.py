import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f" Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {self, message}")


def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(TOKEN)


if __name__ == "__main__":
    main()