from matplotlib.pyplot import contourf
import tweepy
import pandas as pd

# Reference
# https://github.com/RodolfoFerro/pandas_twitter/blob/master/01-extracting-data.md

class Twitter:

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        self.api = self.configure(consumer_key, consumer_secret, access_token, access_secret)

    def configure(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret))
        auth.set_access_token(access_token, access_secret)
        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def latest20TweetsFromAccount(self, account_name: str, count: int):
        last_20_tweets = self.api.user_timeline(screen_name=account_name, count=count)
        for n in last_20_tweets:
            print(n._json)
        pass
        
    def searchTweetsWithStockSymbol(self, symbol: str, count: int): 
        results = self.api.search(q=symbol, count=count)
        json = [r._json for r in results]
        print(json)
        pass 

    def searchTweetsWithCryptoSymbol(self, symbol: str, count: int):
        results = self.api.search(q=symbol, count=count)
        json = [r._json for r in results]
        pass 