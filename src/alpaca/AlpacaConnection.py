import logging
import requests

"""
add a call back method to send the message to the c++
backend - investigate a method... port maybe...

TODO: have a generic return object if something fails
"""

class AlpacaConnection:

    def __init__(self, api, logger):
        self.api = api
        self.logger = logger
        self.data = ""

    def getAccountInformation(self):
        try: 
            self.data = self.api.get_account()
        except self.api.rest.APIError as error:
            self.data = self.buildErrorMessage(error)
            self.logger.warning("Failed to get account information: " + self.data)
        return self.data

    def getClock(self):
        return self.api.get_clock()

    def listPositions(self):
        return self.api.list_positions()

    def getSpecificPosition(self, ticker):
        return self.api.get_position(ticker)

    def cancelAllOrders(self):
        self.api.cancel_all_orders()

    def buildErrorMessage(self, error):
        return str(error) + str(error.status_code)

    