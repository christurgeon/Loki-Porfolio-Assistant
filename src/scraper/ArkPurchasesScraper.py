import os
import io
import config
import sys
import re
import requests
import pandas as pd
from utils.Exceptions import InvalidInputException, EmptyDataframeException

STATISTICS   = r"|".join([r"^top\s+\d+$", r"^all$"])


class ArkFundTracker:

    def __init__(self):
        self.statistics = re.compile(STATISTICS, re.IGNORECASE)
        self.logging = LokiLogger.getLogger(__name__)

    def parseHoldings(self, etf, statistic):
        self.logging.info("parseHoldings() ETF: [{}] STATISTIC: [{}]".format(etf, statistic))
        
        if not self.statistics.match(statistic):
            raise InvalidInputException("invalid statistic type <{}>".format(statistic))

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
        self.logging.info("parse() downloading data")
        headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36" }
        resp = requests.get(url, headers=headers)
        df = pd.read_csv(io.StringIO(resp.text))
        if df.empty: 
            raise EmptyDataframeException("request to {} yielded no data".format(url))
        df.dropna(subset=["fund"], inplace=True)
        df.drop(columns=["date","fund"], inplace=True)
        df.set_index("company", inplace=True)
        df.sort_values(by=["weight(%)"], ascending=False)
        html = ""
        if statistic.startswith("top"): 
            count = list(map(int, re.findall(r"\d+", statistic)))[-1]
            self.logging.info("parsed request for <{}> rows".format(count))
            df = df.head(count)
        html = df.to_html()
        # print(html)
        print(df)

# a = ArkFundTracker()
# a.parseHoldings("ARKG", "top 5")