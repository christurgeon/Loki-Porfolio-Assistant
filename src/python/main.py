import alpaca_trade_api as tradeapi
from alpaca.AlpacaConnection import AlpacaConnection
from marketwatch.StockNewsScraper import StockNewsScraper
from marketwatch.StockNewsScraper import ParserFailedException

import json
import logging
import sys

CONFIGURATION_FILE_PATH = "../../settings.json"
BASE_MARKETWATCH_URL = "https://marketwatch.com/investing/stock/"

if __name__ == "__main__":

    logging.basicConfig(filename="python.log", filemode="w", format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger()

    key_id = secret_key = ""
    try:
        file = open(CONFIGURATION_FILE_PATH, "r")
        data = json.load(file)
        key_id = data["config"]["alpaca_key_id"]
        secret_key = data["config"]["alpaca_private_key"] 
    except:
        logger.fatal("ERROR: failed to extract keys from configuration file located at \"%s\"" % CONFIGURATION_FILE_PATH)
        sys.exit()

    alpaca = AlpacaConnection(logger, key_id, secret_key)
    news_scraper = StockNewsScraper(BASE_MARKETWATCH_URL)
    account = alpaca.getAccountInformation()


    print(account)

    tickers_list = ["TSLA", "MSFT"]
    alpaca.createWatchlist(tickers_list)

    # wlist = alpaca.getWatchlist()
    # print(wlist)

    ticker = "TSLA"
    try: 
        articles = news_scraper.getMarketwatchURLs(ticker)
        print(articles)
    except ParserFailedException as e:
        logger.warning("WARNING: BeautifulSoup failed to extract articles for \"%s\"" % ticker)        

    logging.shutdown()