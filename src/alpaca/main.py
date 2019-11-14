import alpaca_trade_api as tradeapi
from AlpacaConnection import AlpacaConnection

import json
import logging
import sys

CONFIGURATION_FILE_PATH = "../../settings.json"


if __name__ == "__main__":

    logging.basicConfig(filename="alpaca.log", filemode="w", format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger()

    key_id = secret_key = ""
    try:
        file = open(CONFIGURATION_FILE_PATH, "r")
        data = json.load(file)
        key_id = data["alpaca_key_id"]
        secret_key = data["alpaca_private_key"] 
    except:
        logger.fatal("ERROR: failed to extract keys from configuration file located at \"%s\"" % CONFIGURATION_FILE_PATH)
        sys.exit()

    api = tradeapi.REST(key_id, secret_key, api_version='v2') 
    alpaca = AlpacaConnection(api, logger)
    account = alpaca.getAccountInformation()
    
    print(account)

    logging.shutdown()