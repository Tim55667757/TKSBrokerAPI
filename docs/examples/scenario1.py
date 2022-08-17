# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
This is simple trade scenario using TKSBrokerAPI module, without using additional technical analysis.
See: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Abstract-scenario-implementation-example

The actions will be the following:

- request the client's current portfolio and determining funds available for trading;
- request for a Depth of Market with a depth of 20 for the selected instruments, e.g. shares with the tickers
  `YNDX`, `IBM` and `GOOGLE`;
- if the instrument was not purchased earlier, then checking:
  - if the reserve of funds (free cash) in the currency of the instrument more than 5% of the total value
    of all instruments in this currency, then check:
    - if the buyers volumes in the DOM are at least 10% higher than the sellers volumes, then buy 1 share on the market
      and place the take profit as a stop order 3% higher than the current buy price with expire in 1 hour;
- if the instrument is in the list of open positions, then checking:
   - if the current price is 2.5% already higher than the average position price, then place pending limit order
     with all volumes 0.1% higher than the current price so that the position is closed with a profit with a high
     probability during the current session.
- request the current user's portfolio after all trades and show changes.

To understand the example, just save and run this script. Before doing this, don't forget to get a token and find out
your accountId and set up their as environment variables (see the section "Auth" in README_EN.md).
"""

# Copyright (c) 2022 Gilmillin Timur Mansurovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# --- Import, constants and variables initialization section -----------------------------------------------------------

from datetime import datetime, timedelta
from dateutil.tz import tzlocal, tzutc
from math import ceil
from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger  # main module for trading operations

uLogger.level = 10  # DEBUG (10) log level recommended by default for file `TKSBrokerAPI.log
uLogger.handlers[0].level = 20  # log level for STDOUT, INFO (20) recommended by default

start = datetime.now(tzutc())

uLogger.debug("=--=" * 20)
uLogger.debug("Trading scenario started at: [{}] (UTC), it is [{}] local time".format(
    start.strftime("%Y-%m-%d %H:%M:%S"),
    start.astimezone(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
))

# Set here any constants you need for trading:
TICKERS_LIST_FOR_TRADING = ["YNDX", "IBM", "GOOGL"]  # You can define the list of instruments in any way: by enumeration directly or as a result of a filtering function according to some analytic algorithm
RESERVED_MONEY = 0.05  # We reserve some money when open positions, 5% by default
LOTS = 1  # Minimum lots to buy or sell
TP_STOP_DIFF = 0.03  # 3% TP by default for stop-orders
TP_LIMIT_DIFF = 0.025  # 2.5% TP by default for pending limit-orders
TOLERANCE = 0.001  # Tolerance for price deviation around target orders prices, 0.1% by default
DEPTH_OF_MARKET = 20  # How deep to request a list of current prices for an instruments to analyze volumes, >= 1
VOLUME_DIFF = 0.1  # Enough volumes difference to open position, 10% by default

# Main trader object init, TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__
trader = TinkoffBrokerServer(
    token="",  # Attention! Set your token here or use environment variable `TKS_API_TOKEN`
    accountId="",  # Attention! Set your accountId here or use environment variable `TKS_ACCOUNT_ID`
    iList=None,  # Do not use previous saved dictionaries with instruments from broker server
    useCache=True,  # Use auto-updated local cache from `dump.json`
)


# --- Trading scenario section -----------------------------------------------------------------------------------------

for ticker in TICKERS_LIST_FOR_TRADING:
    uLogger.info("--- Ticker [{}], data analysis...".format(ticker))

    # - Step 1: request the client's current portfolio and determining funds available for trading

    # User's portfolio is a dictionary with some sections: {"raw": {...}, "stat": {...}, "analytics": {...}}
    portfolio = trader.Overview(showStatistics=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview

    uLogger.info("Total portfolio cost: {:.2f} rub; blocked: {:.2f} rub; changes: {}{:.2f} rub ({}{:.2f}%)".format(
        portfolio["stat"]["portfolioCostRUB"],
        portfolio["stat"]["blockedRUB"],
        "+" if portfolio["stat"]["totalChangesRUB"] >= 0 else "-", portfolio["stat"]["totalChangesRUB"],
        "+" if portfolio["stat"]["totalChangesPercentRUB"] >= 0 else "-", portfolio["stat"]["totalChangesPercentRUB"],
    ))

    # How much money in different currencies do we have (total - blocked)?
    funds = portfolio["stat"]["funds"]  # dict, e.g. {"rub": {"total": 10000.99, "totalCostRUB": 10000.99, "free": 1234.56, "freeCostRUB": 1234.56}, "usd": {"total": 250.55, "totalCostRUB": 15375.80, "free": 125.05, "freeCostRUB": 7687.50}, ...}

    uLogger.info("Available funds free for trading: {}".format("; ".join(["{:.2f} {}".format(funds[currency]["free"], currency) for currency in funds.keys()])))

    # - Step 2: request a Depth of Market for the selected instruments

    trader.ticker = ticker
    trader.figi = ""  # We don't know FIGI for every ticker, so empty string means to determine it automatically
    trader.depth = DEPTH_OF_MARKET

    # Getting broker's prices on that instrument:
    ordersBook = trader.GetCurrentPrices(showPrice=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetCurrentPrices

    if not (ordersBook["buy"] and ordersBook["sell"]):
        uLogger.warning("Not possible to trade an instrument with the ticker [{}]! Try again later.".format(trader.ticker))

    else:

        # - Step 3: if the instrument was not purchased earlier, then checking:
        #   - if the reserve of funds (free cash) in the currency of the instrument more than 5% of the total value
        #     of all instruments in this currency, then check:
        #     - if the buyers volumes in the DOM are at least 10% higher than the sellers volumes, then buy 1 share on the market
        #       and place the take profit as a stop order 3% higher than the current buy price with expire in 1 hour;

        # Checks if instrument is in portfolio:
        isInPortfolio = trader.IsInPortfolio(portfolio)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.IsInPortfolio

        if not isInPortfolio:
            uLogger.info("Ticker [{}]: no open positions with that instrument, checking opens rules...".format(trader.ticker))

            # Getting instrument's data and it currency:
            rawIData = trader.SearchByTicker(requestPrice=False, showInfo=False, debug=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SearchByTicker
            iCurr = rawIData["currency"]  # currency of current instrument

            # Getting distribution by currencies, cost of previously purchased assets and free money in that currency:
            distrByCurr = portfolio["analytics"]["distrByCurrencies"]  # asset distribution by currencies, cost in rub
            assetsCostInRuble = distrByCurr[iCurr]["cost"]  # cost of all assets in that currency recalc in rub
            currencyFreeCostInRuble = funds[iCurr]["freeCostRUB"]  # free money in that currency recalc in rub

            # Checking reserve and volumes diff before buy:
            if currencyFreeCostInRuble / assetsCostInRuble >= RESERVED_MONEY:
                sumSellers = sum([x["quantity"] for x in ordersBook["buy"]])  # current sellers volumes in the DOM
                sumBuyers = sum([x["quantity"] for x in ordersBook["sell"]])  # current buyers volumes in the DOM

                if sumBuyers >= sumSellers * (1 + VOLUME_DIFF):
                    # Getting current price, then calculating take profit price and validity for stop-order:
                    currentPriceToBuy = ordersBook["buy"][0]["price"]  # 1st price in the list of sellers orders is the actual price that you can buy
                    target = currentPriceToBuy * (1 + TP_STOP_DIFF)  # take profit price target
                    targetStop = ceil(target / rawIData["step"]) * rawIData["step"]  # real target for placing stop-order
                    aliveTo = (datetime.now(tzutc()) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")  # current time + 1 hour

                    uLogger.info("Opening BUY position... (Buyers volumes [{}] >= {} * sellers volumes [{}] and current price to buy: [{:.2f} {}])".format(
                        sumBuyers, 1 + VOLUME_DIFF, sumSellers, currentPriceToBuy, iCurr,
                    ))

                    # Opening BUY market position and creating take profit stop-order:
                    trader.Buy(lots=LOTS, tp=targetStop, sl=0, expDate=aliveTo)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Buy

                else:
                    uLogger.info("BUY position not opened, because buyers volumes [{}] < {} * sellers volumes [{}]".format(sumBuyers, 1 + VOLUME_DIFF, sumSellers))

            else:
                uLogger.info("BUY position not opened, because the reserves in [{}] will be less than {:.2f}% of free funds".format(iCurr, RESERVED_MONEY * 100))

        else:

            # - Step 4: if the instrument is in the list of open positions, then checking:
            #   - if the current price is 2.5% already higher than the average position price, then place pending
            #     limit order with all volumes 0.1% higher than the current price so that the position is closed
            #     with a profit with a high probability during the current session.

            uLogger.info("Ticker [{}]: there is an open position with that instrument, checking closure rules...".format(trader.ticker))

            # Getting instrument from list of instruments in user portfolio:
            iData = trader.GetInstrumentFromPortfolio(portfolio)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetInstrumentFromPortfolio

            # Calculating available lots for sell, average price and current price of instrument:
            lotsToSell = iData["volume"] - iData["blocked"]  # not blocked lots of current instrument, available for trading
            averagePrice = iData["average"]  # average price by all lots
            curPriceToSell = ordersBook["sell"][0]["price"]  # 1st price in the list of buyers orders is the actual price that you can sell

            # Calculating price to close position without waiting for the take profit:
            target = curPriceToSell * (1 + TOLERANCE)  # enough price target to sell
            targetLimit = ceil(target / iData["step"]) * iData["step"]  # real target for placing pending limit order

            # Checking for a sufficient price difference:
            if (curPriceToSell - averagePrice) / averagePrice >= TP_LIMIT_DIFF:
                uLogger.info("The current price is [{:.2f} {}] and enough price target is [{:.2f} {}], so profit more than target +{:.2f}%. Opening SELL pending limit order...".format(
                    curPriceToSell, iData["currency"],
                    targetLimit, iData["currency"],
                    TP_LIMIT_DIFF * 100,
                ))

                # Opening SELL pending limit order:
                trader.SellLimit(lots=lotsToSell, targetPrice=targetLimit)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SellLimit

            else:
                uLogger.info("The price did not reach enough price target [{} {}]. Current price is [{:.2f} {}], so profit less than target +{:.2f}%.".format(
                    targetLimit, iData["currency"],
                    curPriceToSell, iData["currency"],
                    TP_LIMIT_DIFF * 100,
                ))

# - Step 5: request the current user's portfolio after all trades and show changes

uLogger.info("--- All trade operations finished. Let's show what we got in the user's portfolio after all trades.")

# Showing detailed user portfolio information:
trader.Overview(showStatistics=True)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview


# --- Operations finalization section ----------------------------------------------------------------------------------

finish = datetime.now(tzutc())
uLogger.debug("Trading scenario work duration: [{}]".format(finish - start))
uLogger.debug("Trading scenario finished: [{}] (UTC), it is [{}] local time".format(
    finish.strftime("%Y-%m-%d %H:%M:%S"),
    finish.astimezone(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
))
uLogger.debug("=--=" * 20)
