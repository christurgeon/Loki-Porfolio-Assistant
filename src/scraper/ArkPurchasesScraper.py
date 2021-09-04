if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


import io
import config
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame

from utils.LokiLogger import Logger
from utils.RequestsHelper import getRequestWrapper
from utils.Exceptions import InvalidInputException, EmptyHTTPResponseException


class ArkFundTracker:

    def __init__(self):
        self.funds_dict = {
              "arkk" : config.arkk
            , "arkq" : config.arkq
            , "arkw" : config.arkw
            , "arkg" : config.arkg
            , "arkf" : config.arkf
        }
        self.recent_purchases_url = config.ark_purchases
        self.logging = Logger.getLogger(__name__)
        pd.options.display.float_format = '{:.2f}'.format


    def getFundHoldings(self, fundname: str) -> DataFrame:
        if fundname not in self.funds_dict:
            raise InvalidInputException("ARK fund {} not recognized!") 
        url = self.funds_dict[fundname]
        return self.parse(url)


    def getFundRecentPurchases(self, fundname: str, limit: int = 25) -> DataFrame:
        msg = f"getFundRecentPurchases() failed for fund {fundname}"
        if fundname not in self.funds_dict:
            raise InvalidInputException("ARK fund {} not recognized!") 
        url = self.recent_purchases_url.format(fundname)
        response = getRequestWrapper(logging=self.logging, url=url, msg=msg)
        html = BeautifulSoup(response.content, "html.parser")
        div = html.find("div", {"class" : "ant-table-content"}) 
        table = div.find("table")
        df = pd.read_html(str(table))[0]
        df.dropna(inplace=True)
        return df
    

    def parse(self, url: str) -> DataFrame:
        msg = f"parse() failed for request to {url}"
        response = getRequestWrapper(logging=self.logging, url=url, msg=msg)
        df = pd.read_csv(io.StringIO(response.content))
        if df is None or len(df.index) == 0: 
            raise EmptyHTTPResponseException("parse() returned empty, please validate request")
        df.dropna(subset=["fund"], inplace=True)
        df.drop(columns=["date","fund"], inplace=True)
        df.set_index("company", inplace=True)
        df.sort_values(by=["weight(%)"], ascending=False)
        return df

if __name__ == "__main__":
    af = ArkFundTracker()
    funds = ["arkk", "arkq", "arkg", "arkf", "arkw"]

    for f in funds:
        af.getFundRecentPurchases(f)
        break
        # print(af.getFundHoldings(f).to_html())
        print("\n\n")