if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import config
import json
import logging.handlers
import os
import queue
import sys

import alpaca_trade_api as tradeapi
from alpaca.AlpacaConnector import AlpacaConnection
from scraper.StockNewsScraper import StockNewsScraper
from utils.Exceptions import ParserFailedException

LOGPATH      = config.logpath
MODULE_NAME  = "".join(c for c in os.path.splitext(os.path.basename(__file__))[0] if c.isalnum() or c == "_")
LOGFILE_NAME = "Log_{}.log".format(MODULE_NAME)
CONFIGURATION_FILE_PATH = config.settings

class CommandDelegator:
    def __init__(self, discord, alpaca, market_watch, delay_ms=0):
        self.discord = discord
        self.alpaca = alpaca
        self.market_watch = market_watch
        self.delay_ms = delay_ms
        self.job_queue = queue.Queue()
        logging.debug("CommandDelegator Configured")



if __name__ == "__main__":
    log_file_name = os.path.join(LOGPATH, LOGFILE_NAME)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M:%S")
    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="d", interval=1, backupCount=5)
    formatter = logging.Formatter("%(asctime)s[%(levelname)-8s]%(message)s")
    handler.setFormatter(formatter)
    logging.getLogger("").addHandler(handler)
    logging.info("========================================")
    logging.info("START")

    key_id = secret_key = ""
    try:
        file = open(CONFIGURATION_FILE_PATH, "r")
        data = json.load(file)
        key_id = data["config"]["alpaca_key_id"]
        secret_key = data["config"]["alpaca_private_key"]
    except:
        logging.fatal("ERROR: failed to extract keys from configuration file located at \"%s\"" % CONFIGURATION_FILE_PATH)
        sys.exit(-1)

    alpaca = AlpacaConnection(key_id, secret_key)
    news_scraper = StockNewsScraper()
    account = alpaca.getAccountInformation()

    print(account)

    tickers_list = ["TSLA", "MSFT"]
    alpaca.createWatchlist(tickers_list)

    wlist = alpaca.getWatchlist()
    print(wlist)

    ticker = "TSLA"
    try:
        articles = news_scraper.getMarketwatchURLs(ticker)
        print(articles)
    except ParserFailedException as e:
        logging.warning("WARNING: BeautifulSoup failed to extract articles for \"%s\"" % ticker)

    logging.shutdown()
    sys.exit(0)
