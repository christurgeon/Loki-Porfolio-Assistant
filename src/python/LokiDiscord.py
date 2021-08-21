import os
import discord
from dotenv import load_dotenv
from pathlib import Path
import sys
import LokiLogger


class LokiClient(discord.Client):
    
    def __init__(self, logger):
        self.logging = logger
        super(LokiClient, self).__init__()

    async def on_ready(self):
        self.logging.info(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        msg = message.content.lower().strip()
        # await message.channel.send(response)
        if msg.startswith('-ark'):
            await message.channel.send('Hello!')
        else:
            return

    async def on_error(self, event, *args, **kwargs):
        if event == "on_message":
            self.logging.exception(f"Unhandled Exception for message: {args[0]}")
        else:
            raise

    async def on_member_join(self, member):
        print(f'member {member.name} joined')
        return
        # Sends a direct message to that user
        # await member.create_dm()
        # await member.dm_channel.send(
        #     f'Welcome {member.name}!'
        # )


if __name__ == "__main__":
    load_dotenv(Path("./token.env"))
    logging = LokiLogger.getLogger("Discord")
    try:
        client = LokiClient(logging)
        client.run(os.getenv('DISCORD_TOKEN'))
        sys.exit(0)
    except Exception as e:
        logging.error(f"LokiClient failed with: {e}")
        sys.exit(-1)
