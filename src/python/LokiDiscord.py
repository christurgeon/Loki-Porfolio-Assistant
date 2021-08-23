import os
import config
import discord
from dotenv import load_dotenv
from pathlib import Path
import sys
from html2image import Html2Image

from alphavantage.AlphaVantageConnector import AlphaVantage
from scraper.ShortInterestScraper import ShortInterest
from scraper.StockNewsScraper import StockNews
from utils.Exceptions import EmptyHTTPResponseException
from utils.LokiDiscordHelpers import Usage, Files
from utils.LokiLogger import Logger


class LokiClient(discord.Client):
    
    def __init__(self, logger):
        self.logging = logger
        self.short_interest_scraper = ShortInterest()
        self.news_scraper = StockNews()
        self.alpha_vantage = AlphaVantage()
        self.hti = Html2Image()
        super(LokiClient, self).__init__()

    async def on_ready(self):
        self.logging.info(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg = message.content.lower().strip()

        # Handle query for ark investments 
        if msg.startswith('-ark'):
            await message.channel.send('Hello!')

        # Handle query for short interest for a number of stocks
        if msg.startswith('-short'):
            args = msg[7:].split(" ")
            if len(args) != 2 or args[0] not in ("low", "high"):
                await message.channel.send(Usage.ShortInterest)
                return
            self.logging.info(f"Arguments for short interest <{args}>")
            try:
                if args[1].isnumeric():
                    data, size = self.short_interest_scraper.fetchRangeShortInterest(int(args[1]), args[0])
                else:
                    await message.channel.send(Usage.ShortInterest)
                    return
                css = "body {background: white;}"
                self.hti.screenshot(html_str=data, css_str=css, save_as=Files.ShortInterest, size=(600, 40*size))  
                await message.channel.send(config.lowfloat if args[0] == "low" else config.highfloat)
                await message.channel.send(file=discord.File(Files.ShortInterest))
            except Exception as e:
                self.logging.exception(f"Exception while extracting short interest: {e}")
                await message.channel.send(Usage.Default)

        # Provide news articles for a given ticker
        if msg.startswith('-news'):
            args = msg[6:].split(" ")
            if len(args) != 1:
                await message.channel.send(Usage.News)
                return
            self.logging.info(f"Preparing to scrape articles for {args}")
            try:
                articles = self.news_scraper.getMarketwatchURLs(args[0])
                number_of_articles = min(len(articles), int(args[1])) if len(args) == 2 and args[1].isnumeric() else len(articles)
                for i in range(number_of_articles):
                    await message.channel.send(articles[i])
            except Exception as e:
                self.logging.exception(f"Exception while scraping news: {e}")
                await message.channel.send(Usage.Default)

        # CHANGE TO USE REGULAR EXPRESSIONS TO MATCH THIS
        # each command should match and if it does then call that command

        # Interact with the AlphaVantage API
        if msg.startswith('-alpha'):
            args = msg[7:].split(" ")
            try:
                command = args[0].lower()
                if command in ("q", "quote"):
                    data = self.alpha_vantage.getQuote(args[1]) 
                elif command in ("e", "earnings"):
                    data = self.alpha_vantage.getEarnings(args[1])
                elif command == "ipo":
                    data = self.alpha_vantage.getUpcomingIPOs()
                elif command in "fx":
                    data = self.alpha_vantage.getUpcomingIPOs(args[1], args[2])
                elif command == "crypto":
                    data = self.alpha_vantage.getCryptoRating(args[1])
                elif command == "gdp" and len(args) > 1 and args[1] in ("a", "annual", "q", "quarterly"):
                    annual = True if args[1] in ("a", "annual") else False
                    asof = args[2] if len(args) == 3 else None
                    data = self.alpha_vantage.getRealGDP(annual, asof)
                await message.channel.send(data)
            except (IndexError, EmptyHTTPResponseException) as e:
                await message.channel.send(Usage.AlphaVantage)
            except Exception as e:
                await message.channel.send(Usage.Default)
              
        # Ignore
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
    load_dotenv(Path("./config.env"))
    logging = Logger.getLogger("Discord")
    try:
        client = LokiClient(logging)
        client.run(os.getenv('DISCORD_TOKEN'))
        sys.exit(0)
    except Exception as e:
        logging.error(f"LokiClient failed with: {e}")
        sys.exit(-1)
