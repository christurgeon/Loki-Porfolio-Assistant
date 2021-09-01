import config
import pandas as pd
from pandas.core.frame import DataFrame
from io import BytesIO
import matplotlib.pyplot as plt

from utils.LokiLogger import Logger
from utils.RequestsHelper import getRequestWrapper
from utils.Exceptions import EmptyHTTPResponseException


class AlphaVantage:

    def __init__(self, api_key: str, request_interval: int):
        self.api_key = api_key
        self.request_interval = request_interval
        self.base_url = config.alphavantage
        self.logging = Logger.getLogger(__name__)


    def getQuote(self, symbol: str) -> DataFrame:
        params = {
              "function" : "GLOBAL_QUOTE"
            , "symbol"   : symbol 
            , "apikey"   : self.api_key
            , "datatype" : "csv"
        }
        msg = f"getQuote() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        df = pd.read_csv(BytesIO(response.content))
        if df is None or len(df.index) == 0:
            raise EmptyHTTPResponseException("getQuote() returned empty, please validate request")
        if "Error Message" in df.iloc[0][0]:
            raise EmptyHTTPResponseException("getQuote() invalid API call, please validate request")
        return df


    def getEarnings(self, symbol: str) -> DataFrame:
        params = {
              "function" : "EARNINGS_CALENDAR"
            , "symbol"   : symbol 
            , "apikey"   : self.api_key
            , "datatype" : "csv"
        }
        msg = f"getEarnings() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        df = pd.read_csv(BytesIO(response.content))
        if df is None or len(df.index) == 0:
            raise EmptyHTTPResponseException(f"getEarnings() returned empty for {symbol}, please validate request")
        return df


    def getUpcomingIPOs(self) -> DataFrame:
        params = { 
              "function" : "IPO_CALENDAR"
            , "apikey"   : self.api_key 
        }
        msg = "getUpcomingIPOs() failed to fetch IPOs"
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        df = pd.read_csv(BytesIO(response.content))
        if df is None or len(df.index) == 0:
            raise EmptyHTTPResponseException("getUpcomingIPOs() returned empty, please validate request")
        return df


    def getFXRate(self, from_ccy: str, to_ccy: str) -> DataFrame:
        params = {
              "function"        : "CURRENCY_EXCHANGE_RATE"
            , "from_currency"   : from_ccy 
            , "to_currency"     : to_ccy
            , "apikey"          : self.api_key
        }
        msg = f"getFXRate() failed to fetch conversion from {from_ccy} to {to_ccy}"
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        data = response.json()
        data = data.get("Realtime Currency Exchange Rate", None)
        if data is None:
            raise EmptyHTTPResponseException(f"getFXRate() errored for {from_ccy} to {to_ccy} rate, please validate request")
        return DataFrame.from_dict(data, orient="index")


    def getCryptoRating(self, symbol: str) -> DataFrame:
        params = { 
              "function" : "CRYPTO_RATING"
            , "symbol"   : symbol
            , "apikey"   : self.api_key 
            , "datatype" : "csv"
        }
        msg = f"cryptoRating() failed for symbol {symbol}"
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        data = response.json()
        data = data.get("Crypto Rating (FCAS)", None)
        if data is None:
            raise EmptyHTTPResponseException(f"getCryptoRating() returned empty for {symbol}, please validate request")
        return DataFrame.from_dict(data, orient="index")
        
    
    def alphaVantageAPIHelper(self, function: str, msg: str, extra_params: list = [], filter_lambda=None) -> DataFrame:
        params = { 
              "function" : function
            , "apikey"   : self.api_key 
            , "datatype" : "csv"
        }
        for k, v in extra_params:
            params[k] = v
        response = getRequestWrapper(logging=self.logging, url=self.base_url, params=params, msg=msg)
        df = None
        try:
            df = pd.read_csv(BytesIO(response.content))
            if filter_lambda:
                df = df[df.apply(filter_lambda, axis=1)]
        except Exception as e:
            self.logging.error(f"Could not filter JSON results: {e}")
        if df is None or len(df.index) == 0:
            raise EmptyHTTPResponseException(f"Query to {function} retrieved no resuls, please validate request")
        return df


    def getRealGDP(self, annual: bool, asof: str = "1900-01-01") -> DataFrame:
        params = [("interval", "annual" if annual else "quarterly")]
        f = lambda df: df["timestamp"] >= asof
        msg = f"getRealGDP() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper(function="REAL_GDP", msg=msg, extra_params=params, filter_lambda=f)


    def getRealGDPPerCapita(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = "getRealGDPPerCapita() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper(function="REAL_GDP_PER_CAPITA", msg=msg, filter_lambda=f)


    def getTreasuryYield(self, interval: str, maturity: str, asof: str = "1900-01-01") -> DataFrame:
        params = [("interval", interval), ("maturity", maturity)]
        f = lambda df: df["timestamp"] >= asof
        msg = f"getTreasuryYield() failed to fetch results for interval {interval} and maturity {maturity} asof {asof}"
        return self.alphaVantageAPIHelper(function="TREASURY_YIELD", msg=msg, extra_params=params, filter_lambda=f)


    def getFederalFundsRate(self, interval: str, asof: str = "1900-01-01") -> DataFrame:
        params = [("interval", interval)]
        f = lambda df: df["timestamp"] >= asof
        msg = f"getTreasuryYield() failed to fetch results for {interval} asof {asof}"
        return self.alphaVantageAPIHelper(function="FEDERAL_FUNDS_RATE", msg=msg, extra_params=params, filter_lambda=f)


    def getConsumerPriceIndex(self, interval: str, asof: str = "1900-01-01") -> DataFrame:
        params = [("interval", interval)]
        f = lambda df: df["timestamp"] >= asof
        msg = f"getConsumerPriceIndex() failed to fetch results for {interval} asof {asof}"
        return self.alphaVantageAPIHelper("CPI", msg=msg, extra_params=params, filter_lambda=f)


    def getInflation(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getInflation() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("INFLATION", msg=msg, filter_lambda=f)


    def getInflationExpectation(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getInflationExpectation() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("INFLATION_EXPECTATION", msg=msg, filter_lambda=f)


    def getConsumerSentiment(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getConsumerSentiment() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("CONSUMER_SENTIMENT", msg=msg, filter_lambda=f)


    def getRetailSales(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getRetailSales() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("RETAIL_SALES", msg=msg, filter_lambda=f)


    def getDurableGoods(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getDurableGoods() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("DURABLES", msg=msg, filter_lambda=f)


    def getUnemployment(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getUnemployment() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("UNEMPLOYMENT", msg=msg, filter_lambda=f)


    def getNonfarmPayroll(self, asof: str = "1900-01-01") -> DataFrame:
        f = lambda df: df["timestamp"] >= asof
        msg = f"getNonfarmPayroll() failed to fetch results asof {asof}"
        return self.alphaVantageAPIHelper("NONFARM_PAYROLL", msg=msg, filter_lambda=f)


    def graphData(self, df: DataFrame):
        fig = df.plot(x="timestamp", figsize=(15, 5), grid=True)
        plt.xlabel("Date")
        plt.xticks(rotation=65)
        plt.subplots_adjust(bottom=0.25)
        return fig.get_figure()