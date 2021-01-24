if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os
import config
import logging.handlers
import alpaca_trade_api as tradeapi
from alpaca.AlpacaConnection import AlpacaConnector
from marketwatch.StockNewsScraper import StockNewsScraper
from marketwatch.StockNewsScraper import ParserFailedException

import json
import sys
import queue

LOGPATH = config.logpath
MODULE_NAME = "".join(c for c in os.path.splitext(os.path.basename(__file__))[0] if c.isalnum() or c == "_")
LOGFILE_NAME = "Log_{}.log".format(MODULE_NAME)

CONFIGURATION_FILE_PATH = "../../settings.json"
BASE_MARKETWATCH_URL = "https://marketwatch.com/investing/stock/"

#
    # 1. PERHAPS CONFIGURE SOME OBJECTS THEN HAVE A WAY FOR C++ TO SEND MESSAGES TO THIS PROGRAM WHICH WILL THEN DELEGATE TO SUB SCRIPTS
    # 2. Encrypt the settings / config is fine but settings with keys and passwords should be Encrypted and decrypted
#

class CommandDelegator:
    def __init__(self, delay_ms=0, discord, alpaca, market_watch):
        self.delay_ms = delay_ms
        self.discord = discord
        self.alpaca alpaca
        self.market_watch = market_watch
        self.job_queue = queue.Queue()
        logging.debug("CommandDelegator Configured")

    def addJob(message_string):
        self.job_queue.put(_)
        pass

    def executeNextJob():
        # Script and proper action should be determined, popped off the queue and executed asynchronously
        pass

    def executor():
        # Helper function to execute script, should be kicked off in the background
        pass




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
        logging.warning("WARNING: BeautifulSoup failed to extract articles for \"%s\"" % ticker)

    logging.shutdown()
    sys.exit(0)
