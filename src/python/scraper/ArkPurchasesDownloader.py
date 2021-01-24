if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os
import io
import config
import sys
import logging.handlers
import requests
import pandas as pd
from utils.Exceptions import InvalidInputException

LOGPATH = config.logpath
MODULE_NAME = "".join(c for c in os.path.splitext(os.path.basename(__file__))[0] if c.isalnum() or c == "_")
LOGFILE_NAME = "Log_{}.log".format(MODULE_NAME)


class ArkFundTracker:

    def __init__(self, logging):
        self.logging = logging 
        self.statistics = ["top", "all"]

    def parseHoldings(self, etf, statistic):
        if statistic not in self.statistics:
            raise InvalidInputException("invalid stat type <{}>".format(statistic))
        etf = etf.lower()
        if etf == "arkk": 
            self.parse(config.arkk, statistic)
        elif etf == "arkq":
            self.parse(config.arkq, statistic)
        elif etf == "arkw":
            self.parse(config.arkw, statistic)
        elif etf == "arkg":
            self.parse(config.arkg, statistic)
        elif etf == "arkf":
            self.parse(config.arkf, statistic)
        else:
            raise InvalidInputException("invalid etf type <{}>".format(etf))
 
    def parse(self, url, statistic):
        headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36" }
        resp = requests.get(url, headers=headers)
        df = pd.read_csv(io.StringIO(resp.text))
        df.dropna(inplace=True)
        print(df)



if __name__ == "__main__":
    # log_file_name = os.path.join(LOGPATH, LOGFILE_NAME)
    # logging.basicConfig(level=logging.INFO,
    #                     format="%(asctime)s %(levelname)-8s %(message)s",
    #                     datefmt="%m-%d %H:%M:%S")
    # handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="d", interval=1, backupCount=5)
    # formatter = logging.Formatter("%(asctime)s[%(levelname)-8s]%(message)s")
    # handler.setFormatter(formatter)
    # logging.getLogger("").addHandler(handler)
    # logging.info("========================================")
    # logging.info("START")
    try:
        a = ArkFundTracker(None)
        a.parseHoldings("ARKL", "top")
    except Exception as e:
        # logging.error("Exception: {}".format(e))
        print(e)
    sys.exit(0)
