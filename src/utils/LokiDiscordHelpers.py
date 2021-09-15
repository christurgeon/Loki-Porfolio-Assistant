import re


class Usage:
    Overview = r"""
    Loki is an investment assistant bot designed to provide you
    configurable updates as well as requested information on 
    the markets at anytime.

    -short <low/high> <number_of_stocks>
      | Retrieve a list of stocks at a specified size 
      | with the highest or lowest daily short interest 
    
    - 
    """
    ShortInterest         = "-short <low/high> <number_of_stocks>"
    AlphaVantage          = "TODO"
    Ark                   = "TODO"
    FinancialModelingPrep = "TODO"
    Futures               = "TODO"
    Twitter               = "TODO"
    Default               = "Sorry! I couldn't complete that command... something went wrong :("


class Files:
    ShortInterest     = "shortinterest.jpg"
    AlphaVantageCsv   = "alphavantage.csv"
    AlphaVantageJpeg  = "alphavantage.jpg"
    Futures           = "futures.jpg"


class Regex:

  ###################################
  # AlphaVantage                    # 
  ###################################

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

  ###################################
  # ArkInvest                       # 
  ###################################

  # i.e. <h/holdings ARKK>
  ArkHoldings                 = re.compile(r"^\s*(h|holdings)\s+[a-zA-Z]+$", re.IGNORECASE)
  # i.e. <p/purchases ARKK top*>
  ArkPurchases                = re.compile(r"^\s*(p|purchases)\s+[a-zA-Z]+(\s+\d+|\s*)$", re.IGNORECASE)

  ###################################
  # FinancialModelingPrep           # 
  ###################################

  ### TODO

  ###################################
  # Twitter                         # 
  ###################################

  # i.e. <q/query count*>
  TweetsWithSymbol            = re.compile(r"^\s*(q|query)\s+\$[a-zA-Z]+(\s*|\s+\d*)$", re.IGNORECASE) 
  # i.e. <u/user count*>
  TweetsFromUser              = re.compile(r"^\s*(u|user)\s+[a-zA-Z0-9]+(\s*|\s+\d*)$", re.IGNORECASE)