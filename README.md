# Greetings from Loki

## Personal Configuration 
Create a file called ```config.env``` and place it in the ```src/python``` directory of the application. You will need to get some API keys and initialize it as follows:

```
# Discord Related
DISCORD_TOKEN=<your-key-here>

# AlphaVantage Related
ALPHA_VANTAGE_TOKEN=<your-key-here>
```


## Build
We are currently still in a development phase, but if you are interested in picking up where we are currently. You can simply run the ```run-python.sh``` script to get the bot up and running. Currently supported functinality includes requesting news articles, retreiving high and low short interest stocks, and requesting data from AlphaVantage. 

Have a look at our ```TODO.txt``` file to see the next features to be implemented.