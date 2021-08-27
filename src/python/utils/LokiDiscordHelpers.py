import re


class Usage:
    Overview = r"""
    Loki is an investment assitant bot designed to provide you
    configurable updates as well as requested information on 
    the markets at anytime.

    -short <low/high> <number_of_stocks>
      | Retrieve a list of stocks at a specified size 
      | woth the highest or lowest daily short interest 
    
    - 
    """
    ShortInterest = "-short <low/high> <number_of_stocks>"
    AlphaVantage  = "TODO"
    Default       = "Sorry! I couldn't complete that command... something went wrong :("


class Files:
    ShortInterest = "shortinterest.jpg"
    AlphaVantage  = "alphavantage.jpg"

class Regex:

  # i.e. <q/quote AAPL>
  AlphaQuote                  = re.compile(r"^\s*(q|quote)\s+[a-zA-Z]+$", re.IGNORECASE)
  # i.e. <e/earnings AAPL>
  AlphaEarnings               = re.compile(r"^\s*(e|earnings)\s+[a-zA-Z]+$", re.IGNORECASE)
  # i.e. <ipo>
  AlphaIPO                    = re.compile(r"^\s*ipo$", re.IGNORECASE)
  # i.e. <fx JPY USD>
  AlphaFXRate                 = re.compile(r"^\s*fx\s+[a-zA-Z]+\s+[a-zA-Z]+$", re.IGNORECASE)
  # i.e. <crypto BTC>
  AlphaCryptoRating           = re.compile(r"^\s*crypto\s+[a-zA-Z]+$", re.IGNORECASE)
  # i.e. <gdp annual/quarterly asof*>
  AlphaGDP                    = re.compile(r"^\s*gdp\s+(annual|quarterly)(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <gdpcapita asof*>
  AlphaGDPPerCapita           = re.compile(r"^\s*gdpcapita(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <yield asof*>
  AlphaTreasuryYield          = re.compile(r"^\s*yield(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <fedrate asof*>
  AlphaFedRate                = re.compile(r"^\s*fedrate(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <cpi asof*>
  AlphaCPI                    = re.compile(r"^\s*cpi(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <inflation asof*>
  AlphaInflation              = re.compile(r"^\s*inflation(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <inflationexp asof*>
  AlphaInflationExpectation   = re.compile(r"^\s*inflationexp(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <durablegoods asof*>
  AlphaDurableGoods           = re.compile(r"^\s*durablegoods(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <unemployment asof*>
  AlphaUnemployment           = re.compile(r"^\s*unemployment(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)
  # i.e. <nonfarmpayroll asof*>
  AlphaNonfarmPayroll         = re.compile(r"^\s*nonfarmpayroll(\s+\d{8}|\s+\d{4}-\d{2}-\d{2}|\s*)$", re.IGNORECASE)