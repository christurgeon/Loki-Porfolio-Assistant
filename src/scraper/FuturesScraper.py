if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


import re
import config
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame

from utils.LokiLogger import Logger
from utils.RequestsHelper import getRequestWrapper
from utils.Exceptions import EmptyHTTPResponseException


class Futures:

    def __init__(self):
        self.futures_url = config.futures
        self.logging = Logger.getLogger(__name__)

    def getLatestFutures(self) -> DataFrame:
        msg = f"getLatestFutures() failed to reach webpage"
        response = getRequestWrapper(logging=self.logging, url=self.futures_url, msg=msg)
        html = BeautifulSoup(response.content, "html.parser")
        div = html.find("div", {"data-test" : "price-table"})
        table = div.find("table")
        df = pd.read_html(str(table))[0]
        df.drop(columns=["Unnamed: 0", "Unnamed: 9"], inplace=True)
        df.fillna("", inplace=True)
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: re.sub("derived", "", x)) # column: Index
        df[df.columns[1]] = df[df.columns[1]].apply(lambda x: re.sub("Ex.", "", x)) # column: Month
        if df is None or len(df.index) == 0:
            raise EmptyHTTPResponseException("getLatestFutures() could not parse the table, please validate request")
        return df