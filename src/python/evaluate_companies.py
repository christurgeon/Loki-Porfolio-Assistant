# PYTHON IMPLEMENTATION OF https://github.com/recola-wand/undervalued-stocks
#
# Each company is rated on following three values:
#   1. Profit to Book Value
#   2. Quarertly Earnings
#   3. forwardEps minus trailingEps
#
# The lower rating the better. Each rating is summed to give the total rating.
# Number 1 company receieves 1 point, number 2 receieves 2, etc.
#
# Note: It is extremely unlikely that a company would receieve 3 points (i.e. best at all)
# A low profit to book value means the company stock is undervalued. If such a company also
# has stellar quarterly earnings growth plus notable forward outlook then
# it is more significantly undervalued.


import json
import logging
import requests
import sys
from bs4 import BeautifulSoup


SP_URL = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
YAHOO_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?region=US&lang=en&symbol={ticker}"
YAHOO_HEADER = {
    "x-rapidapi-host"   : "apidojo-yahoo-finance-v1.p.rapidapi.com",
    "x-rapidapi-key"    : "YOUR-API-KEY"
}


def download(sess):
    """
    @goal   | retrieve data for S&P 500 companies and dump to json
    @param  | sess - requests.Session() object
    @return | 0 if successful, -1 if not, can throw exception
    """

    logger.info("download() start retrieving S&P 500 list")
    tickers = []
    for i in range(3):
        resp = requests.get(url=SP_URL)
        if resp.status_code != 200:
            logger.error("download() could not reach {} response.status_code = {}".format(resp.url, resp.status_code))
            return -1
        else:
            break
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class" : "wikitable sortable"})
    for row in table.findAll("tr")[1:]:
        tickers.append(row.findAll("td")[0].text.strip())
    logger.info(tickers)

    logger.info("download() start retrieving S&P 500 data")
    spdata = ""
    for i, t in enumerate(tickers):
        try:
            resp = sess.get(url=YAHOO_URL.format(ticker=t), headers=YAHOO_HEADER)
            logger.info("{}\t{}\t\t| response.status_code = {}".format(i, t, resp.status_code))
            spdata += resp.text
        except Exception as e:
            logger.exception("download() exception occurred for {}: [{}]".format(t, e))
    with open("spdata.json", "w") as file:
        logger.info("download() start writing data to spdata.json")
        json.dump(spdata, file)
    return 0


if __name__ == "__main__":
    logging.basicConfig(filename="evaluate_companies.log", filemode="w", format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger()
    ret = -1
    logger.info("==========START==========")
    with requests.Session() as sess:
        try:
            ret = download(sess)
        except Exception as e:
            logger.exception("Exception: [{}]".format(e))
    logger.info("Exiting with code = {}".format(ret))
    logger.info("==========DONE==========")
    sys.exit(ret)
