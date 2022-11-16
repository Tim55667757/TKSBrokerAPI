# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
Example 1a: using object-oriented programming instead imperative programming paradigm as in 1st example:
https://github.com/Tim55667757/TKSBrokerAPI/blob/master/docs/examples/scenario1.py

In this case, it is better to create a class `TradeScenario(TinkoffBrokerServer)` inherited from the main API class
`TinkoffBrokerServer()`. As class fields, you can take the names of constants from the first example, write separate
methods for each step and logical checks, and then combine the call of all conditions and trading operations in the
`run()` method. In the main block `if __name__ == "__main__:"` when running the script, it will be enough to create
an instance of the class and initialize it with constants from the first example, and then just call the `run()` method.

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
your accountId and set up their as environment variables (see the section "Auth" in `README_EN.md`).

# In russian (на русском)
Пример 1a: используем ООП парадигму, вместо императивного программирования торгового сценария, как в 1-м примере:
https://github.com/Tim55667757/TKSBrokerAPI/blob/master/docs/examples/scenario1.py

В этом случае лучше создать унаследованный от основного API-класса `TinkoffBrokerServer()` класс
`TradeScenario(TinkoffBrokerServer)`. В качестве полей класса можно взять имена констант из первого примера, написать
отдельные методы для каждого шага и логических проверок, и затем объединить вызов всех условий и торговых операций
в методе `run()`. В основном блоке `if __name__ == "__main__:"` при запуске скрипта будет достаточно создать экземпляр
класса-сценария и параметризовать его константами из первого примера, а затем вызвать метод `run()`.

Давайте рассмотрим один простой сценарий, основанный на сравнении объёмов текущих покупок и продаж, и реализуем его
при помощи модуля TKSBrokerAPI, без использования дополнительных методов технического анализа. Смотрите также:
https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md#Пример-реализации-абстрактного-сценария

Действия будут следующие:

- запросить текущий портфель клиента и определить доступные для торговли средства;
- запросить стакан цен с глубиной 20 для выбранных инструментов, например, акции с тикерами `YNDX`, `IBM` and `GOOGLE`;
- если инструмент ранее ещё не был куплен, то проверить:
  - если резерв денежных средств (свободный кеш) в валюте инструмента больше, чем 5% от общей стоимости всех
    инструментов в этой валюте, то проверить:
    - если в стакане объёмы на покупку больше объёмов на продажу минимум на 10%, то купить 1 акцию по рынку и выставить
      тейк-профит как стоп-ордер на 3% выше текущей цены покупки со сроком действия 1 час;
- если инструмент имеется в списке открытых позиций, то проверить:
   - если текущая цена уже выше средней цены позиции хотя бы на 2.5%, то выставить отложенный лимитный ордер
     на весь объём, но ещё чуть-чуть выше (на 0.1%) от текущей цены, чтобы позиция закрылась с профитом
     с большой вероятностью в течении текущей сессии.
- после всех торговых операций напечатать в консоль текущее состояние портфеля пользователя.

Для понимания примера сохраните и запустите этот скрипт. Не забудьте перед этим подставить свой token и accountId
в разделе инициализации в коде (см. раздел "Аутентификация" в `README.md`).

Комментарии к коду на русском можно найти в документации под спойлерами:
https://github.com/Tim55667757/TKSBrokerAPI#Пример-реализации-абстрактного-сценария
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

from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger  # main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSEnums import TKS_PRINT_DATE_TIME_FORMAT


class TradeScenario(TinkoffBrokerServer):
    """This class describe methods with trading logic."""

    def __init__(self, userToken: str, userAccount: str = None) -> None:
        """
        Trade scenario init and parametrize.

        :param userToken: Bearer token for Tinkoff Invest API. Or use environment variable `TKS_API_TOKEN`.
        :param userAccount: string with numeric user account ID in Tinkoff Broker. Or use environment variable `TKS_ACCOUNT_ID`.

        See TKSBrokerAPI api-doc: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__
        """
        super().__init__(token=userToken, accountId=userAccount)  # call parent initialize section `__init__()`

        # Additional trade variables for current scenario:
        self.tickers = []  # You can define the list of instruments in any way: by enumeration directly or as a result of a filtering function according to some analytic algorithm
        self.reserve = 0.05  # We reserve some money when open positions, 5% by default
        self.lots = 1  # Minimum lots to buy or sell
        self.tpStopDiff = 0.03  # 3% TP by default for stop-orders
        self.tpLimitDiff = 0.025  # 2.5% TP by default for pending limit-orders
        self.tolerance = 0.001  # Tolerance for price deviation around target orders prices, 0.1% by default
        self.depth = 20  # How deep to request a list of current prices for an instruments to analyze volumes, >= 1
        self.volDiff = 0.1  # Enough volumes difference to open position, 10% by default

        # Self-calculated parameters during the trade process (not for manual setting):
        self._portfolio = {}  # User portfolio is a dictionary with some sections: {"raw": {...}, "stat": {...}, "analytics": {...}}
        self._funds = {}  # How much money in different currencies do we have (total - blocked)?
        self._ordersBook = {"buy": [], "sell": [], "limitUp": 0, "limitDown": 0, "lastPrice": 0, "closePrice": 0}  # Current prices
        self._rawIData = {}  # Raw instruments data
        self._sumSellers = 0  # current sellers volumes in the DOM
        self._sumBuyers = 0  # current buyers volumes in the DOM
        self._iCurr = ""  # Currency of current instrument
        self._distrByCurr = {}  # Asset distribution by currencies, cost in rub
        self._assetsCostInRuble = 0  # Cost of all assets in that currency recalc in rub
        self._currencyFreeCostInRuble = 0  # Free money in that currency recalc in rub
        self._iData = {}  # Current instrument data from the user's portfolio if it presents there
        self._lotsToSell = 0  # Not blocked lots of current instrument, available for trading
        self._averagePrice = 0  # Average price by all lots
        self._curPriceToSell = 0  # 1st price in the list of buyers orders is the actual price that you can sell
        self._curProfit = 0  # Changes between current price and average price of instrument
        self._targetLimit = 0  # Real target + tolerance for placing pending limit order
        self._changes = False  # True if was changes in the user portfolio

    def _GetPortfolio(self) -> None:
        """
        Gets user's portfolio as a dictionary with some sections: `self._portfolio = {"raw": {...}, "stat": {...}, "analytics": {...}}`
        """
        self._portfolio = self.Overview(show=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview

        uLogger.info("Total portfolio cost: {:.2f} rub; blocked: {:.2f} rub; changes: {}{:.2f} rub ({}{:.2f}%)".format(
            self._portfolio["stat"]["portfolioCostRUB"],
            self._portfolio["stat"]["blockedRUB"],
            "+" if self._portfolio["stat"]["totalChangesRUB"] > 0 else "", self._portfolio["stat"]["totalChangesRUB"],
            "+" if self._portfolio["stat"]["totalChangesPercentRUB"] > 0 else "", self._portfolio["stat"]["totalChangesPercentRUB"],
        ))

    def _CalculateFreeFunds(self) -> None:
        """
        How much money in different currencies do we have (total - blocked)?

        Example: `self._funds = {"rub": {"total": 10000.99, "totalCostRUB": 10000.99, "free": 1234.56, "freeCostRUB": 1234.56},
                                 "usd": {"total": 250.55, "totalCostRUB": 15375.80, "free": 125.05, "freeCostRUB": 7687.50}, ...}`
        """
        self._funds = self._portfolio["stat"]["funds"]

        uLogger.info("Available funds free for trading: {}".format("; ".join(["{:.2f} {}".format(self._funds[currency]["free"], currency) for currency in self._funds.keys()])))

    def _GetOrderBook(self, currentTicker: str) -> bool:
        """
        Gets broker's prices on current instrument.

        :param currentTicker: Depth of Market requests for instrument with this ticker.
        :return: `True` if it is possible to trade (order book not empty).
        """
        emptyBook = True
        self.ticker = currentTicker
        self.figi = ""  # We don't know FIGI for every ticker, so empty string means to determine it automatically

        self._ordersBook = self.GetCurrentPrices(show=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetCurrentPrices

        if not (self._ordersBook["buy"] and self._ordersBook["sell"]):
            uLogger.warning("Not possible to trade an instrument with the ticker [{}]! Try again later.".format(self.ticker))

        else:
            emptyBook = False

        return emptyBook

    def _CalculateDataForOpenRules(self):
        """
        Gets instrument's data and its currency. And then gets distribution by currencies, cost of previously
        purchased assets and free money in that currency.
        """
        uLogger.info("Ticker [{}]: no current open positions with that instrument, checking opens rules...".format(self.ticker))

        self._rawIData = self.SearchByTicker(requestPrice=False, show=False)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SearchByTicker
        self._iCurr = self._rawIData["currency"]  # currency of current instrument
        self._distrByCurr = self._portfolio["analytics"]["distrByCurrencies"]  # asset distribution by currencies, cost in rub
        self._assetsCostInRuble = self._distrByCurr[self._iCurr]["cost"]  # cost of all assets in that currency recalc in rub
        self._currencyFreeCostInRuble = self._funds[self._iCurr]["freeCostRUB"]  # free money in that currency recalc in rub

    def _CalculateDOMSums(self):
        """Calculates current sellers and buyers volumes in the DOM"""
        self._sumSellers = sum([x["quantity"] for x in self._ordersBook["buy"]])  # current sellers volumes in the DOM
        self._sumBuyers = sum([x["quantity"] for x in self._ordersBook["sell"]])  # current buyers volumes in the DOM

    def _OpenBuyMarketPosition(self):
        """
        Gets current price, then calculates take profit price and validity for stop-order.
        And then opening BUY market position and creating take profit stop-order.
        """
        currentPriceToBuy = self._ordersBook["buy"][0]["price"]  # 1st price in the list of sellers orders is the actual price that you can buy
        target = currentPriceToBuy * (1 + self.tpStopDiff)  # take profit price target
        targetStop = ceil(target / self._rawIData["step"]) * self._rawIData["step"]  # real target for placing stop-order
        localAliveTo = (datetime.now() + timedelta(hours=1)).strftime(TKS_PRINT_DATE_TIME_FORMAT)  # current local time + 1 hour

        uLogger.info("Opening BUY position... (Buyers volumes [{}] >= {} * sellers volumes [{}] and current price to buy: [{:.2f} {}])".format(
            self._sumBuyers, 1 + self.volDiff, self._sumSellers, currentPriceToBuy, self._iCurr,
        ))

        buyResponse = self.Buy(lots=self.lots, tp=targetStop, sl=0, expDate=localAliveTo)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Buy

        if "message" in buyResponse.keys():
            uLogger.warning("Server message: {}".format(buyResponse["message"]))

        else:
            self._changes = True

    def _Step3(self):
        """
        Implementation of Step 3: if the instrument was not purchased earlier, then checking:
        - if the reserve of funds (free cash) in the currency of the instrument more than 5% of the total value
          of all instruments in this currency, then check:
          - if the buyers volumes in the DOM are at least 10% higher than the sellers volumes, then buy 1 share on the market
            and place the take profit as a stop order 3% higher than the current buy price with expire in 1 hour.
        """
        # Also, checking reserve and volumes diff before buy:
        if self._currencyFreeCostInRuble / self._assetsCostInRuble >= self.reserve:
            self._CalculateDOMSums()

            if self._sumBuyers >= self._sumSellers * (1 + self.volDiff):
                self._OpenBuyMarketPosition()

            else:
                uLogger.info("BUY position not opened, because buyers volumes [{}] < {} * sellers volumes [{}]".format(self._sumBuyers, 1 + self.volDiff, self._sumSellers))

        else:
            uLogger.info("BUY position not opened, because the reserves in [{}] will be less than {:.2f}% of free funds".format(self._iCurr, self.reserve * 100))

    def _CalculateDataForCloseRules(self):
        """
        Gets instrument from list of instruments in user portfolio. And then calculates available lots for sale, average price
        and current price of instrument. And then calculating price to close position without waiting for the take profit.
        """
        uLogger.info("Ticker [{}]: there is an open position with that instrument, checking close rules...".format(self.ticker))

        self._iData = self.GetInstrumentFromPortfolio(self._portfolio)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetInstrumentFromPortfolio

        self._lotsToSell = self._iData["volume"] - self._iData["blocked"]  # not blocked lots of current instrument, available for trading
        self._averagePrice = self._iData["average"]  # average price by all lots
        self._curPriceToSell = self._ordersBook["sell"][0]["price"]  # 1st price in the list of buyers orders is the actual price that you can sell

        self._curProfit = (self._curPriceToSell - self._averagePrice) / self._averagePrice  # changes between current price and average price of instrument
        target = self._curPriceToSell * (1 + self.tolerance)  # enough price target to sell
        self._targetLimit = ceil(target / self._iData["step"]) * self._iData["step"]  # real target + tolerance for placing pending limit order

    def _OpenSellMarketPosition(self):
        """Opening sell market order if enough profit."""
        uLogger.info(
            "The current price is [{:.2f} {}], average price is [{:.2f} {}], so profit {:.2f}% more than {:.2f}%. Opening SELL pending limit order...".format(
                self._curPriceToSell, self._iData["currency"], self._averagePrice, self._iData["currency"],
                self._curProfit * 100, self.tpLimitDiff * 100,
            ))

        # Opening SELL pending limit order:
        sellResponse = self.SellLimit(lots=self._lotsToSell, targetPrice=self._targetLimit)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SellLimit

        if "message" in sellResponse.keys():
            uLogger.warning("Server message: {}".format(sellResponse["message"]))

        else:
            self._changes = True

    def _Step4(self):
        """
        Implementation of Step 4: if the instrument is in the list of open positions, then checking:
        - if the current price is 2.5% already higher than the average position price, then place pending
          limit order with all volumes 0.1% higher than the current price so that the position is closed
          with a profit with a high probability during the current session.
        """
        # Also, checking for a sufficient price difference before sell:
        if self._curProfit >= self.tpLimitDiff:
            self._OpenSellMarketPosition()

        else:
            uLogger.info("SELL order not created, because the current price is [{:.2f} {}], average price is [{:.2f} {}], so profit {:.2f}% less than {:.2f}% target.".format(
                self._curPriceToSell, self._iData["currency"], self._averagePrice, self._iData["currency"],
                self._curProfit * 100, self.tpLimitDiff * 100,
            ))

    def Run(self):
        """Trading scenario section. Implementation of one trade iteration."""
        self._changes = False  # Setting no changes in user portfolio before trade iteration

        for ticker in self.tickers:
            uLogger.info("--- Ticker [{}], data analysis...".format(ticker))

            # - Step 1: request the client's current portfolio and determining funds available for trading
            self._GetPortfolio()
            self._CalculateFreeFunds()

            # - Step 2: request a Depth of Market for the selected instruments
            emptyBook = self._GetOrderBook(currentTicker=ticker)

            if emptyBook:
                continue

            # Checks if instrument (defined by its `ticker`) is in portfolio:
            isInPortfolio = self.IsInPortfolio(self._portfolio)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.IsInPortfolio

            if not isInPortfolio:

                # - Step 3: if the instrument was not purchased earlier, then checking:
                #   - if the reserve of funds (free cash) in the currency of the instrument more than 5% of the total value
                #     of all instruments in this currency, then check:
                #     - if the buyers volumes in the DOM are at least 10% higher than the sellers volumes, then buy 1 share on the market
                #       and place the take profit as a stop order 3% higher than the current buy price with expire in 1 hour;

                self._CalculateDataForOpenRules()
                self._Step3()

            else:

                # - Step 4: if the instrument is in the list of open positions, then checking:
                #   - if the current price is 2.5% already higher than the average position price, then place pending
                #     limit order with all volumes 0.1% higher than the current price so that the position is closed
                #     with a profit with a high probability during the current session.

                self._CalculateDataForCloseRules()
                self._Step4()

        # - Step 5: request the current user's portfolio after all trades and show changes

        uLogger.info("--- All trade operations finished.{}".format(" Let's show what we got in the user's portfolio after all trades." if self._changes else ""))

        # Showing detailed user portfolio information if it was changes:
        if self._changes:
            self.Overview(show=True)  # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview


def TimerDecorator(func):
    """Some technical operations before main scenario started and then after main scenario finished."""

    def Wrapper():
        uLogger.level = 10  # DEBUG (10) log level recommended by default for file `TKSBrokerAPI.log`
        uLogger.handlers[0].level = 20  # log level for STDOUT, INFO (20) recommended by default

        start = datetime.now(tzutc())

        uLogger.debug("=--=" * 25)
        uLogger.debug("Trading scenario started at: [{}] UTC, it is [{}] local time".format(start.strftime(TKS_PRINT_DATE_TIME_FORMAT), start.astimezone(tzlocal()).strftime(TKS_PRINT_DATE_TIME_FORMAT)))

        func()

        finish = datetime.now(tzutc())

        uLogger.debug("Trading scenario work duration: [{}]".format(finish - start))
        uLogger.debug("Trading scenario finished: [{}] UTC, it is [{}] local time".format(finish.strftime(TKS_PRINT_DATE_TIME_FORMAT), finish.astimezone(tzlocal()).strftime(TKS_PRINT_DATE_TIME_FORMAT)))
        uLogger.debug("=--=" * 25)

    return Wrapper


@TimerDecorator
def Trade():
    """
    Initialization of a class instance for a trading scenario and parameterization of the main trading parameters.

    TKSBrokerAPI module documentation:
    - in english: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html

    TKSBrokerAPI platform documentation:
    - in english: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md
    - in russian: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md
    """
    # --- Main trader object init:
    trader = TradeScenario(
        userToken="",  # Attention! Set your token here or use environment variable `TKS_API_TOKEN`
        userAccount="",  # Attention! Set your accountId here or use environment variable `TKS_ACCOUNT_ID`
    )

    # --- Set here any parameters you need for trading:
    trader.tickers = ["YNDX", "IBM", "GOOGL"]  # You can define the list of instruments in any way: by enumeration directly or as a result of a filtering function according to some analytic algorithm
    trader.reserve = 0.05  # We reserve some money when open positions, 5% by default
    trader.lots = 1  # Minimum lots to buy or sell
    trader.tpStopDiff = 0.03  # 3% TP by default for stop-orders
    trader.tpLimitDiff = 0.025  # 2.5% TP by default for pending limit-orders
    trader.tolerance = 0.001  # Tolerance for price deviation around target orders prices, 0.1% by default
    trader.depth = 20  # How deep to request a list of current prices for an instruments to analyze volumes, >= 1
    trader.volDiff = 0.1  # Enough volumes difference to open position, 10% by default

    trader.moreDebug = False  # Set to `True` if you need more debug information, such as headers, requests and responses

    trader.Run()  # Starting one iteration of trade with all instruments


if __name__ == "__main__":
    Trade()  # Initialization, parametrization and run trading scenario
