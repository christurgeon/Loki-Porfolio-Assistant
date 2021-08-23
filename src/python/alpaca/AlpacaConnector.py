import config
import requests
import alpaca_trade_api as tradeapi
from utils.LokiLogger import Logger



API_WATCHLIST_URL = "https://paper-api.alpaca.markets/v2/watchlists"
WATCHLIST_NAME = "mywatchlist"

class AlpacaConnection:

    def __init__(self, logging, key_id, secret_key):
        self.api = tradeapi.REST(key_id, secret_key, api_version='v2')
        self.logging = Logger.getLogger("Alpaca")
        self.account_data = ""
        self.header = { "APCA-API-KEY-ID":key_id, "APCA-API-SECRET-KEY":secret_key}

    def getAccountInformation(self):
        try:
            self.account_data = self.api.get_account()
        except Exception as error:
            self.account_data = self.buildErrorMessage(error)
            self.logging.error("Failed to get account information: " + self.account_data)
        return self.account_data

    def getClock(self):
        return self.api.get_clock()

    def listPositions(self):
        return self.api.list_positions()

    def getSpecificPosition(self, ticker):
        return self.api.get_position(ticker)

    def cancelAllOrders(self):
        self.api.cancel_all_orders()

    def addToWatchlist(self, tickers):
        pass

    def createWatchlist(self, tickers):
        params = { "name":WATCHLIST_NAME, "symbols":tickers }
        response = requests.post(url=API_WATCHLIST_URL, params=params, headers=self.header)
        self.logging.debug("Status Code: {} | Response: {}".format(response.text, response.status_code))

    def getWatchlist(self):
        endpoint = API_WATCHLIST_URL + "/" + WATCHLIST_NAME
        response = requests.get(url=endpoint, headers=self.header)
        watchlist = response.json()
        self.logging.debug("Watchlist: {}".format(watchlist))
        return watchlist

    def removeSymbol(self, ticker):
        endpoint = API_WATCHLIST_URL + "/" + WATCHLIST_NAME + "/" + ticker
        response = requests.delete(url=endpoint, headers=self.header)
        self.logging.debug("Status Code: {} | Response: {}".format(response.text, response.status_code))

    def buildErrorMessage(self, error):
        return str(error) + str(error.status_code)
