import requests
from bs4 import BeautifulSoup


class ParserFailedException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class StockNewsScraper:

    def __init__(self, base_url):
        self.url = base_url

    def getMarketwatchURLs(self, ticker):
        response = requests.get(self.url + ticker)
        html = BeautifulSoup(response.content, "html.parser")
        news_articles = html.find_all("a", attrs={"class": "figure__image"})    
        if (news_articles == None):
            raise ParserFailedException()
        return [i["href"] for i in news_articles]