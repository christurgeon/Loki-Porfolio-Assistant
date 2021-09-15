# Greetings from Loki

## Overview
Loki is a Discord Bot built to assist you and your Discord server in stock research. Similar to the Bloomberg Terminal, it accepts a variety of commands and performs actions based on those commands. Examples include retreiving news articles for a ticker, getting a list of upcoming IPOs, and even displaying recent tweets that mention a specific stock. To get the bot up and running, simply install Docker and create a ```config.env``` file [see below]. 

## Personal Configuration 
Create a file called ```config.env``` and place it in the ```src/``` directory of the application. You will need to retrieve some API keys that Loki uses to fetch data and initialize the config file as follows:

```
# Discord Related
DISCORD_TOKEN=xxxxxxxxx
DISCORD_GUILD=xxxxxxxxx

# AlphaVantage Related
ALPHA_VANTAGE_TOKEN=xxxxxxxxx
REQUESTS_INTERVAL_MILLIS=12000 

# FinancialModelingPrep Related
FINANCIAL_MODELING_PREP_TOKEN=xxxxxxxxx

# Twitter Related
TWITTER_CONSUMER_KEY=xxxxxxxxx
TWITTER_CONSUMER_SECRET=xxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxx
```


## Build
We are currently still in a development phase, but if you are interested in picking up where we are currently. You can simply run the ```LokiDiscord.py``` script to get the bot up and running. Currently supported features include requesting news articles, retreiving high and low short interest stocks, retreiving tweets from a user or that mention a certain phrase (i.e. $AAPL), and retreiving latest futures data. 

Have a look at our ```TODO.txt``` file to see the next features to be implemented.