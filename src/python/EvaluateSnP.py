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

import config
import json
import logging
import os
import requests
import sys
from bs4 import BeautifulSoup
from utils.LokiLogger import getLogger

logger = getLogger(__name__)

SPDATA_FILE = "spdata50.json"
SP_URL = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
YAHOO_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail?region=US&lang=en&symbol={ticker}"
YAHOO_HEADER = {
    "x-rapidapi-host"   : "apidojo-yahoo-finance-v1.p.rapidapi.com",
    "x-rapidapi-key"    : "YOUR-API-KEY"
}



def getSP500():
    """
    @goal   | retrieve list of all S&P 500 tickers
    @return | a list of all S&P 500 tickers, can throw exception
    """
    logger.info("getSP500() start retrieving S&P 500 list")
    tickers = []
    resp = requests.get(url=SP_URL)
    if resp.status_code != 200:
        logger.error("getSP500() could not reach {} response.status_code = {}".format(resp.url, resp.status_code))
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class" : "wikitable sortable"})
    for row in table.findAll("tr")[1:]:
        tickers.append(row.findAll("td")[0].text.strip())
    logger.info(tickers)
    if len(tickers) < 500:
        logging.error("Expected number of tickers not retrieved from {}".format(SP_URL))
        raise Exception("Unable to retrieve S&P 500 ticker list...")
    return tickers



def download(sess, tickers):
    """
    @goal   | retrieve data for S&P 500 companies and dump to text file
    @param  | sess - requests.Session() object
    @param  | tickers - list of all S&P 500 tickers
    @return | 0 if successful, -1 otherwise, can throw exception
    """
    logger.info("download() start retrieving S&P 500 data")
    spdata = []
    for i, t in enumerate(tickers):
        try:
            resp = sess.get(url=YAHOO_URL.format(ticker=t), headers=YAHOO_HEADER)
            logger.info("{}\t{}\t\t| response.status_code = {}".format(i, t, resp.status_code))
            spdata.append(resp.text)
        except Exception as e:
            logger.exception("download() exception occurred for {}: [{}]".format(t, e))
    with open(SPDATA_FILE, "w") as file:
        logger.info("download() start writing data to spdata.txt")
        for i in spdata:
            file.write(i)
    return 0



def evaluate(tickers):
    """
    @goal   | score each S&P 500 company
    @param  | tickers, list of S&P 500 tickers
    @return | 0 if successful, -1 otherwise, can throw exception
    """
    spdict = {k: None for k in tickers}

    with open(SPDATA_FILE, "r") as file:
        while True:
            line = file.readline()
            if not line:
                logging.info("Finished reading file...")
                return 0
            spdata = json.loads(line)

            pegRatio = s["defaultKeyStatistics"]["pegRatio"]["raw"]
            earningsQuarterlyGrowth = s["defaultKeyStatistics"]["earningsQuarterlyGrowth"]["raw"]
            profitMargins = s["defaultKeyStatistics"]["profitMargins"]["raw"]
            f2WeekChange = s["defaultKeyStatistics"]["52WeekChange"]["raw"]
            priceToBook = s["defaultKeyStatistics"]["priceToBook"]["raw"]
            forwardEps = s["defaultKeyStatistics"]["forwardEps"]["raw"]
            trailingEps = s["defaultKeyStatistics"]["trailingEps"]["raw"]
            forwardPE = s["defaultKeyStatistics"]["forwardPE"]["raw"]
            # sector = s["summaryProfile"]["sector"]

            profitable = pegRatio > 0 and earningsQuarterlyGrowth > 0 and profitMargins > .1 #and sector != "Financial Services"
            if profitable:
                print(s["symbol"])
                spdict[s["symbol"]] = [s]

            # Highly profitable but is also down
            profitable = earningsQuarterlyGrowth > 0 and f2WeekChange < -0.1

            # Book value is less than price
            giveaway = (priceToBook < 1 and
                        f2WeekChange < -0.1 and
                        profitMargins > .1 and
                        earningsQuarterlyGrowth > 0)

            # Brightest future
            bestfuture = (forwardEps / trailingEps > 1.25 and
                          profitMargins > 0.1 and
                          earningsQuarterlyGrowth > 0)

            # Bright future
            goodfuture = trailingEps <= forwardEps

            # Future is dark
            darkfuture = forwardEps < 0


            # Sort by forwardPE and rank each company
            spdict[s["symbol"]].append(forwardPE)
            # Sort by PEGratio and rank each company
            spdict[s["symbol"]].append(pegRatio)
            # Sort by 52WeekChange and rank each company
            spdict[s["symbol"]].append(f2WeekChange)
            # Sort by priceToBook and rank each company
            spdict[s["symbol"]].append(priceToBook)
            # Sort by earningsQuarterlyGrowth and rank each company
            spdict[s["symbol"]].append(earningsQuarterlyGrowth)

            # Sum all of these up to give the total score for the ticker, then sort all by total value

            header = "Symbol, Total Value, Profitable Value, Giveaway Value, Best Future Value, earningsQuarterlyGrowth, priceToBook, forwardPE, pegRatio, 52WeekChange, marketPrice, Industry, earningsDate, recommendation"
            logging.info(header)



if __name__ == "__main__":
    log_file_name = os.path.join(LOGPATH, LOGFILE_NAME)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M:%S")
    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="d", interval=1, backupCount=5)
    formatter = logging.Formatter("%(asctime)s[%(levelname)-8s]%(message)s")
    handler.setFormatter(formatter)
    logging.getLogger("").addHandler(handler)
    logging.info("========================================")
    logging.info("START")
    rc = -1
    with requests.Session() as sess:
        try:
            tickers = getSP500()
            # ret = download(sess, tickers)
            # logging.info("download() COMPLETE with ret = {}".format(ret))
            rc = evaluate(tickers)
            logging.info("evaluate() COMPLETE with ret = {}".format(rc))
        except Exception as e:
            logger.error("Exception: {}".format(e))
    logging.info("END rc = {}".format(rc))
    sys.exit(rc)
