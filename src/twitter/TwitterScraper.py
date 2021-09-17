if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from pandas.core.frame import DataFrame
import tweepy
import pandas as pd
# from textblob import TextBlob

# Reference
# https://github.com/RodolfoFerro/pandas_twitter/blob/master/01-extracting-data.md

class Twitter:

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        self.api = self.__configure(consumer_key, consumer_secret, access_token, access_secret)

    def __configure(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def __parseHelper(self, tweets) -> DataFrame:
        rowbuilder = dict.fromkeys(["Tweet", "Date", "Likes", "Retweets"])
        df = DataFrame(columns=rowbuilder.keys())
        for tweet in tweets:
            try:
                rowbuilder["Tweet"] = tweet.retweeted_status.full_text
            except AttributeError:
                rowbuilder["Tweet"] = tweet.full_text
            rowbuilder["Date"] = tweet.created_at
            rowbuilder["Likes"] = tweet.favorite_count
            rowbuilder["Retweets"] = tweet.retweet_count
            df = df.append(rowbuilder, ignore_index=True)
        return df

    # def __cleanTweet(self, tweet):
    #     # remove links and special characters
    #     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # def __sentimentAnalysis(self, tweet):
    #     analysis = TextBlob(self.__cleanTweet(tweet))
    #     if analysis.sentiment.polarity > 0:
    #         return 1 
    #     elif analysis.sentiment.polarity == 0:
    #         return 0
    #     else:
    #         return -1

    def latestTweetsFromUser(self, account_name: str, count: int = 5) -> DataFrame:
        count = min(count, 25)
        return self.__parseHelper(self.api.user_timeline(screen_name=account_name, count=count, tweet_mode="extended"))
        
    def searchTweetsWithSymbol(self, symbol: str, count: int = 5) -> DataFrame: 
        count = min(count, 25)
        return self.__parseHelper(self.api.search(q=symbol, count=count, tweet_mode="extended"))

    @staticmethod
    def prettyFormatTweets(tweets: DataFrame):
        formatted_tweets = []
        for tweet in tweets.iterrows():
            series = tweet[1]
            text = series.Tweet
            date = series.Date 
            likes = series.Likes 
            retweets = series.Retweets
            formatted_tweets.append(f"Tweet from *{date}*: **{likes} likes, {retweets} retweets**\n```yaml\n{text}```")
        return formatted_tweets




from dotenv import load_dotenv
from pathlib import Path
import os
if __name__ == "__main__":
    load_dotenv(Path("../config.env"))
    tk, ta = os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET")
    tkk, taa = os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
    T = Twitter(tk, ta, tkk, taa)
    # T.searchTweetsWithStockSymbol("#aapl", 5)
    a = T.latestTweetsFromUser("visualsofchris", 1)
    print(a)

    b = Twitter.prettyFormatTweets(a)
    for i in b: 
        print(b)
