from utils.LokiLogger import Logger
from utils.RequestsHelper import getRequestWrapper
from utils.Exceptions import EmptyHTTPResponseException

class FinancialModelingPrep:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logging = Logger.getLogger(__name__)
        self.base_url_v3 = "https://financialmodelingprep.com/api/v3/"
        self.base_url_v4 = "https://financialmodelingprep.com/api/v4/"


    # https://financialmodelingprep.com/developer/docs/companies-key-stats-free-api
    def getCompanyProfile(self, symbol: str):
        url = self.base_url_v3 + f"/profile/{symbol}"
        params = { "apikey" : self.api_key }
        msg = f"getCompanyProfile() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())


    # https://financialmodelingprep.com/developer/docs/stock-api
    def getQuote(self, symbol: str):
        url = self.base_url_v3 + f"/quote/{symbol}"
        params = { "apikey" : self.api_key }
        msg = f"getQuote() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())


    # https://financialmodelingprep.com/developer/docs/companies-rating-free-api
    def getCompanyRating(self, symbol: str, limit: str = "1"):
        url = self.base_url_v3 + f"/historical-rating/{symbol}"
        params = { "apikey" : self.api_key, "limit" : limit }
        msg = f"getCompanyRating() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())


    # https://financialmodelingprep.com/developer/docs/historical-stock-splits
    def getStockSplits(self, symbol: str):
        url = self.base_url_v3 + f"/historical-price-full/stock_split/{symbol}"
        params = { "apikey" : self.api_key }
        msg = f"getStockSplits() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())


    # https://financialmodelingprep.com/developer/docs/stock-insider-trading
    def getInsiderTrading(self, symbol: str, limit: str = "50"):
        url = self.base_url_v4 + f"/insider-trading/{symbol}"
        params = { "apikey" : self.api_key, "limit" : limit }
        msg = f"getInsiderTrading() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())


    # https://financialmodelingprep.com/developer/docs/stock-grade
    def getStockGrade(self,  symbol: str, limit: str = "50"):
        url = self.base_url_v4 + f"/grade/{symbol}"
        params = { "apikey" : self.api_key, "limit" : limit }
        msg = f"getStockGrade() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=url, params=params, msg=msg)
        print(response.json())