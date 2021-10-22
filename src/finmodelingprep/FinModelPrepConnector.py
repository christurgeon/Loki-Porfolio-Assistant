if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
from logging import raiseExceptions
from utils.LokiLogger import Logger
from utils.RequestsHelper import getRequestWrapper
from utils.Exceptions import EmptyHTTPResponseException

class FinancialModelingPrep:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logging = Logger.getLogger(__name__)
        self.base_url_v3 = "https://financialmodelingprep.com/api/v3/"
        self.base_url_v4 = "https://financialmodelingprep.com/api/v4/"


    def __helper(self, v3: bool, symbol: str, endpoint: str, msg: str, additional_params = None):
        url = (self.base_url_v3 if v3 else self.base_url_v4) + f"/{endpoint}/{symbol}"
        params = { "apikey" : self.api_key }
        msg = msg + " failed for symbol " + symbol
        if additional_params:
            params.update(additional_params)
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        obj = response.json()
        if obj is None or len(obj) == 0:
            raise EmptyHTTPResponseException()
        print(response.json())
        print(len(response.text))


    # https://financialmodelingprep.com/developer/docs/companies-key-stats-free-api
    def getCompanyProfile(self, symbol: str):
        result = self.__helper(v3=True, symbol=symbol, endpoint="profile", msg=f"getCompanyProfile()")
        print(result)


    # https://financialmodelingprep.com/developer/docs/stock-api
    def getQuote(self, symbol: str):
        result = self.__helper(v3=True, symbol=symbol, endpoint="quote", msg=f"getQuote()")


    # https://financialmodelingprep.com/developer/docs/companies-rating-free-api
    def getCompanyRating(self, symbol: str, limit: int = 1):
        result = self.__helper(v3=True, symbol=symbol, endpoint="historical-rating", msg=f"getCompanyRating()", additional_params={"limit" : limit})


    # https://financialmodelingprep.com/developer/docs/historical-stock-splits
    def getStockSplits(self, symbol: str):
        result = self.__helper(v3=True, symbol=symbol, endpoint="historical-price-full/stock_split", msg=f"getStockSplits()")


    # https://financialmodelingprep.com/developer/docs/stock-insider-trading
    def getInsiderTrading(self, symbol: str, limit: int = 50):
        result = self.__helper(v3=False, symbol=symbol, endpoint="insider-trading", msg=f"getInsiderTrading()", additional_params={"limit" : limit})


    # https://financialmodelingprep.com/developer/docs/stock-grade
    def getStockGrade(self,  symbol: str, limit: int = 50):
        result = self.__helper(v3=False, symbol=symbol, endpoint="grade", msg=f"getStockGrade()", additional_params={"limit" : limit})


if __name__ == "__main__":
    a = FinancialModelingPrep()
    a.getCompanyProfile("aapl")
