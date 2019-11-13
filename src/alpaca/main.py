import alpaca_trade_api as tradeapi

import json
import sys

CONFIGURATION_FILE_PATH = "../../settings.json"


if __name__ == "__main__":

    key_id = secret_key = ""
    try:
        file = open(CONFIGURATION_FILE_PATH, "r")
        data = json.load(file)
        key_id = data["alpaca_public_key"]
        secret_key = data["alpaca_private_key"] 
    except:
        print("ERROR: failed to extract keys from configuration file located at \"%s\"" % CONFIGURATION_FILE_PATH)
        sys.exit()

    api = tradeapi.REST(key_id, secret_key, api_version='v2') 
    account = api.get_account()
    # api.list_position