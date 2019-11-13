#!/usr/bin/python

import alpaca_trade_api as tradeapi

if __name__ == "__main__":
    
    api = tradeapi.REST('<key_id>', '<secret_key>', api_version='v2') # or use ENV Vars shown below
    account = api.get_account()
    api.list_positions()