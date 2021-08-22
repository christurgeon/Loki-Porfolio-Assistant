import config
import requests
from bs4 import BeautifulSoup
from utils.LokiLogger import Logger
from utils.Exceptions import ParserFailedException

class StockNews:

    def __init__(self):
        self.url = config.marketwatch
        self.logging = Logger.getLogger(__name__)

    def getMarketwatchURLs(self, ticker):
        self.logging.info("getting articles for ticker {}".format(ticker))
        response = requests.get(self.url + ticker)
        html = BeautifulSoup(response.content, "html.parser")
        news_articles = html.find_all("a", attrs={"class": "figure__image"})    
        if (news_articles == None):
            raise ParserFailedException()
        self.logging.info("found {} articles".format(len(news_articles)))
        return [i["href"] for i in news_articles if i["href"].startswith("http")]