# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


**Anomaly Volumes Detector** is a simple TG-bot for detecting anomaly volumes of Buyers and Sellers prices.

The bot monitors the volumes of Buyers and Sellers in the orders book (DOM), looks for anomalies in the number series
of volumes and notifies in Telegram. The notification contains: the current price and prices with anomaly volumes.

Bot doesn't contain the real trade operations.

**Acknowledgements**

* Idea and sponsorship: [Jolids](https://github.com/Jolids)
* Developer: [Timur Gilmullin](https://github.com/Tim55667757)
"""

# Copyright (c) 2023 Gilmillin Timur Mansurovich
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

import os
import sys
import traceback as tb
import yaml
import pycron
from time import sleep
from requests import get
from json import loads

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

# Main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger
from tksbrokerapi.TKSEnums import TKS_PRINT_DATE_TIME_FORMAT
from tksbrokerapi.TradeRoutines import *


# --- Common technical parameters:

CPU_COUNT = cpu_count()  # Real available Host CPU count
CPU_USAGES = CPU_COUNT - 1 if CPU_COUNT > 1 else 1  # How many CPUs will be used for parallel computing
SCENARIO_ID = "TKSAVDetector"  # Scenario identifier

# --- Templates:

EN_TEMPLATE = """Anomalous volumes detected of {}:
  - [{}] [{}] [{}]
  - Date and time:
    {} UTC
  - Is in portfolio: {}

- Current price/volume/value
  - Buy (1st seller price):
    [0] {}/{}/{}{}
  - Sell (1st buyer price):
    [0] {}/{}/{}{}

- Anomaly, price/volume/value
  - in sellers volumes: {}
  - in buyers volumes: {}

Generated by ⚙ TKSBrokerAPI"""

RU_TEMPLATE = """Обнаружены аномальные объёмы {}:
  - [{}] [{}] [{}]
  - Время обнаружения:
    {} UTC
  - Есть в портфеле: {}

- Текущая цена/объём/стоимость
  - Купить:
    [0] {}/{}/{}{}
  - Продать:
    [0] {}/{}/{}{}

- Аномалии
  - в объёмах продавцов: {}
  - в объёмах покупателей: {}

Сгенерировано ⚙ TKSBrokerAPI"""


class TradeScenario(TinkoffBrokerServer):
    """This class contains methods for implementing the trading scenario logic."""

    def __init__(self, **kwargs) -> None:
        """
        Initialization and parameterization of the trading scenario.

        **kwargs** parameters can be:
        * **userToken:** str, Tinkoff Invest API token. Or just use `TKS_API_TOKEN` environment variable.
        * **userAccount:** str, user account ID. Or just use `TKS_ACCOUNT_ID` environment variable.
        * **userName:** str, user name to identify in log.
        * **comment:** str, some additional comment to identify in log. Can be empty.
        * **pipelineId:** int, number id of the pipeline.
        * **botToken:** str, telegram bot token. Or just use `TKS_BOT_TOKEN` environment variable.
        * **chatId:** int, chat ID with authorized user for sending messages. How to find it, see in README.md.

        TKSBrokerAPI api-doc: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__
        """
        super().__init__(token=kwargs["userToken"], accountId=kwargs["userAccount"])  # Initialize main `__init__()` of `TinkoffBrokerServer()` class.
        self.userName = kwargs["userName"]  # Additional identifier for user.
        self.comment = kwargs["comment"]  # Additional comment in log.

        self.botToken = kwargs["botToken"]  # Telegram bot token. If empty string, then no messages will be sent.
        self.chatId = kwargs["chatId"]  # Telegram Chat ID with authorized user for sending messages.

        # Main trade parameters loaded from configuration files and replaced here:
        self.timeout = 30  # Server operations timeout in seconds.
        self.depth = 20  # How deep to request the Depth of Market to analyze current trading volumes, `1 <= depth <= 50`.
        self.msgLanguage = "en"  # Bot messages language: "en" / "ru" supported.
        self.windowHampel = 0  # Length of the sliding window in Hampel filter (0 mean max wide window is used), `1 <= windowHampel <= len(series)`.
        self.anomaliesMaxCount = 3  # Maximum anomalies that bot sending in one message.
        self.volumeIgnored = 0  # Volume less than this number will be ignored (0 mean that all values will use).

        # Some parameters calculated during the execution of the trading scenario (not for manual setting):
        self._pipelineId = kwargs["pipelineId"] if "pipelineId" in kwargs.keys() else "*"  # Pipeline ID number.
        self._curTicker = ""  # In `Run()` method we will save original ticker name, before run scenario steps.
        self._curFIGI = ""  # In `Run()` method we will get and save original FIGI identifier, before run scenario steps.
        self._portfolio = {}  # User's portfolio with all instruments is a dictionary with some sections: `{"raw": {...}, "stat": {...}, "analytics": {...}}`.
        self._rawIData = {}  # Raw data of one instrument from broker cache.
        self._iData = None  # Information about instrument if it presents in user portfolio.
        self._ordersBook = {"buy": [], "sell": [], "limitUp": 0, "limitDown": 0, "lastPrice": 0, "closePrice": 0}  # Actual broker prices for current instrument.
        self._curPriceToBuy = 0  # The first price in the orders list of Sellers is the current price at which you can buy the instrument (or put it for a sell).
        self._curPriceToSell = 0  # The first price in the orders list of Buyers is the current price at which you can sell the instrument (or put it for a buy).
        self._curVolumeToBuy = 0  # Volumes for the first price in the orders list of Sellers.
        self._curVolumeToSell = 0  # Volumes for the first price in the orders list of Buyers.
        self._curValueToBuy = 0  # Cost of the first Sellers offer.
        self._curValueToSell = 0  # Cost of the first Buyers offer.
        self._volumesOfBuyers = []  # Numerical series with volumes of Buyers in descending price order.
        self._volumesOfSellers = []  # Numerical series with volumes of Sellers in ascending price order.
        self._sumBuyers = 0  # The current volumes of Buyers in the DOM (you can sell to Buyers).
        self._sumSellers = 0  # The current volumes of Sellers in the DOM (you can buy from Sellers).
        self._currency = ""  # The current instrument currency.

        uLogger.debug("Pipeline [{}]: init completed".format(self._pipelineId))

    def _UpdateOrderBook(self) -> bool:
        """
        Receiving actual prices for current instrument, saving to the `_ordersBook` variable and re-calculating some volume parameters.

        :return: `True` if the order book has been successfully updated, and it is possible to trade (the order book is not empty).
        """
        self.ticker = self._curTicker  # Set current ticker to processing with TKSBrokerAPI.
        self.figi = self._curFIGI  # Set current FIGI ID to processing with TKSBrokerAPI.

        # Receiving DOM, TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetCurrentPrices
        self._ordersBook = self.GetCurrentPrices(show=False)

        if self._ordersBook["buy"] and self._ordersBook["sell"]:
            self._curPriceToBuy = self._ordersBook["buy"][0]["price"]  # The first price in the orders list of Sellers is the current price at which you can buy the instrument (or put it for a sell).
            self._curPriceToSell = self._ordersBook["sell"][0]["price"]  # The first price in the orders list of Buyers is the current price at which you can sell the instrument (or put it for a buy).
            self._curVolumeToBuy = self._ordersBook["buy"][0]["quantity"]  # Volumes for the first price in the orders list of Sellers.
            self._curVolumeToSell = self._ordersBook["sell"][0]["quantity"]  # Volumes for the first price in the orders list of Buyers.
            self._curValueToBuy = self._curPriceToBuy * self._curVolumeToBuy  # Cost of the first Sellers offer.
            self._curValueToSell = self._curPriceToSell * self._curVolumeToSell  # Cost of the first Buyers offer.
            self._volumesOfBuyers = [v["quantity"] for v in self._ordersBook["sell"]]  # Numerical series with volumes of Buyers in descending price order.
            self._volumesOfSellers = [v["quantity"] for v in self._ordersBook["buy"]]  # Numerical series with volumes of Sellers in ascending price order.
            self._sumBuyers = sum(self._volumesOfBuyers)  # The current volumes of Buyers in the DOM (you can sell to Buyers).
            self._sumSellers = sum(self._volumesOfSellers)  # The current volumes of Sellers in the DOM (you can buy from Sellers).
            self._currency = self._rawIData["currency"] if self._rawIData and "currency" in self._rawIData.keys() else ""  # The current instrument currency.

            uLogger.debug("[{}] Orders book was received success".format(self._curTicker))

            return True

        else:
            self._curPriceToBuy = 0
            self._curPriceToSell = 0
            self._curVolumeToBuy = 0
            self._curVolumeToSell = 0
            self._curValueToBuy = 0
            self._curValueToSell = 0
            self._volumesOfBuyers = []
            self._volumesOfSellers = []
            self._sumBuyers = 0
            self._sumSellers = 0
            self._currency = ""

            uLogger.debug("[{}] An empty orders book was returned or non-trading time".format(self._curTicker))

            return False

    def _CreateMessage(self, aBuyers: list[dict], aSellers: list[dict]) -> str:
        """
        Creates info message with found anomalies. Input lists contains dictionaries with anomalies data, for example:
        `[{'id': 5, 'price': 4.174, 'volume': 452481, 'value': 1888655.694}, ..., {...}, ...]`.

        :param aBuyers: list of dictionaries with anomalies in Buyers orders.
        :param aSellers: list of dictionaries with anomalies in Sellers orders.
        :return: str, Markdown formatted message.
        """
        if aBuyers or aSellers:
            # Whose anomalous volumes were detected:
            if aSellers and aBuyers:
                whom = "продавцов и покупателей" if self.msgLanguage == "ru" else "Sellers and Buyers"

            elif aSellers:
                whom = "продавцов" if self.msgLanguage == "ru" else "Sellers"

            else:
                whom = "покупателей" if self.msgLanguage == "ru" else "Buyers"

            # Is the instrument present in your portfolio:
            if self._iData:
                inPortfolio = "Да" if self.msgLanguage == "ru" else "Yes"

            else:
                inPortfolio = "Нет" if self.msgLanguage == "ru" else "No"

            # Current currency string for message:
            if self._currency:
                curr = " руб" if self.msgLanguage == "ru" and self._currency == "rub" else " {}".format(self._currency)

            else:
                curr = ""

            # Preparing some data about anomalies in Sellers offers:
            sellersOffers = ""
            if self.anomaliesMaxCount > 0 and aSellers:
                for i in range(min(self.anomaliesMaxCount, len(aSellers))):
                    sellersOffers += "\n    [{}] {}/{}/{}{}".format(
                        aSellers[i]["id"],  # Position of anomaly in Sellers orders, started from 0.
                        round(aSellers[i]["price"], 6), aSellers[i]["volume"], round(aSellers[i]["value"], 2), curr,
                    )

            else:
                sellersOffers = "Нет данных" if self.msgLanguage == "ru" else "No data"

            # Preparing some data about anomalies in Buyers offers:
            buyersOffers = ""
            if self.anomaliesMaxCount > 0 and aBuyers:
                for i in range(min(self.anomaliesMaxCount, len(aBuyers))):
                    buyersOffers += "\n    [{}] {}/{}/{}{}".format(
                        aBuyers[i]["id"],  # Position of anomaly in Buyers orders, started from 0.
                        round(aBuyers[i]["price"], 6), aBuyers[i]["volume"], round(aBuyers[i]["value"], 2), curr,
                    )

            else:
                buyersOffers = "Нет данных" if self.msgLanguage == "ru" else "No data"

            # Preparing final message. Russian/English templates switch:
            aData = [
                whom,  # Whose anomalous volumes were detected.
                self._curTicker, self._rawIData["type"], self._rawIData["name"],  # Stock ticker, Type of instrument and the company name.
                datetime.now().strftime(TKS_PRINT_DATE_TIME_FORMAT),  # Date and time of detected.
                inPortfolio,  # Is the instrument present in your portfolio.
                round(self._curPriceToBuy, 6), self._curVolumeToBuy, round(self._curValueToBuy, 2), curr,  # Current price / volume / value of Sellers in the order book.
                round(self._curPriceToSell, 6), self._curVolumeToSell, round(self._curValueToSell, 2), curr,  # Current price / volume / value of Buyers in the order book.
                sellersOffers, buyersOffers,  # Formatted strings with anomalies of Sellers and Buyers.
            ]
            message = RU_TEMPLATE.format(*aData) if self.msgLanguage == "ru" else EN_TEMPLATE.format(*aData)  # Formatting message.

            uLogger.debug("[{}] Message created:\n{}".format(self._curTicker, message))

        else:
            message = ""  # No Buyers nor Sellers anomalies.

        return message

    def _TGSender(self, msg: str) -> bool:
        """
        Telegram Bot Sender.

        :param msg: str, message to send.
        :return: bool, `True` if message success sent. If an errors occurred or not set value for `botToken`, then returns `False`.
        """
        success = False

        if self.botToken and msg:
            msgText = r"https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text=`{}`".format(self.botToken, self.chatId, msg)

            try:
                response = loads(get(msgText, timeout=self.timeout).text)

                uLogger.debug("[{}] Raw response from Telegram API-server:\n{}".format(self._curTicker, response))

            except Exception as e:
                uLogger.debug(tb.format_exc())
                uLogger.warning("[{}] An issue occurred when sending via Telegram API-server! See full debug log. Message: {}".format(self._curTicker, e))

                response = {}

            if "ok" in response.keys() and response["ok"]:
                success = True

            else:
                uLogger.warning("[{}] Telegram API-server returned an error! Message not sent. See full debug log.".format(self._curTicker))

        return success

    def Steps(self) -> dict:
        """
        Section for implementing the steps of the trading scenario for one current instrument.

        :return: Dictionary with trade results, e.g. `{"result": "success", "message": "All trade steps were finished success"}`.
        """
        self.ticker = self._curTicker  # Set current ticker to processing with TKSBrokerAPI.
        self.figi = self._curFIGI  # Set current FIGI ID to processing with TKSBrokerAPI.

        try:
            # --- Checking the common situation on the market or technical signals -------------------------------------

            # Checking the availability of the instrument in the portfolio.
            # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetInstrumentFromPortfolio
            self._iData = self.GetInstrumentFromPortfolio(self._portfolio)

            # --- Filtering anomalies:
            windowBuy = len(self._volumesOfBuyers) if self.windowHampel <= 0 or self.windowHampel >= len(self._volumesOfBuyers) else self.windowHampel
            aFilteredBuy = list(HampelFilter(self._volumesOfBuyers, window=windowBuy))  # Positions of volume anomalies in orders of Buyers.

            windowSell = len(self._volumesOfSellers) if self.windowHampel <= 0 or self.windowHampel >= len(self._volumesOfSellers) else self.windowHampel
            aFilteredSell = list(HampelFilter(self._volumesOfSellers, window=windowSell))  # Positions of volume anomalies in orders of Sellers.

            onlyAnomaliesOfBuyers = [{
                "id": i,
                "price": item["price"],
                "volume": item["quantity"],
                "value": item["price"] * item["quantity"],
            } for i, item in enumerate(self._ordersBook["sell"]) if aFilteredBuy[i]]

            onlyAnomaliesOfSellers = [{
                "id": i,
                "price": item["price"],
                "volume": item["quantity"],
                "value": item["price"] * item["quantity"],
            } for i, item in enumerate(self._ordersBook["buy"]) if aFilteredSell[i]]

            uLogger.debug("[{}] All volume anomalies in orders of Buyers: {}".format(self._curTicker, onlyAnomaliesOfBuyers))
            uLogger.debug("[{}] All volume anomalies in orders of Sellers: {}".format(self._curTicker, onlyAnomaliesOfSellers))

            if self.volumeIgnored > 0:
                uLogger.debug("`volumeIgnored = {}`, volume less than this number will be ignored!".format(self.volumeIgnored))

                onlyAnomaliesOfBuyers = [item for item in onlyAnomaliesOfBuyers if item["volume"] > self.volumeIgnored]
                onlyAnomaliesOfSellers = [item for item in onlyAnomaliesOfSellers if item["volume"] > self.volumeIgnored]

                uLogger.debug("[{}] Filtered volume anomalies in orders of Buyers: {}".format(self._curTicker, onlyAnomaliesOfBuyers))
                uLogger.debug("[{}] Filtered volume anomalies in orders of Sellers: {}".format(self._curTicker, onlyAnomaliesOfSellers))

            # --- Checking closing position rules if instrument already yet in portfolio -------------------------------

            pass

            # --- Checking opening position rules for an instrument ----------------------------------------------------

            pass

            # --- Final steps ------------------------------------------------------------------------------------------

            if onlyAnomaliesOfBuyers or onlyAnomaliesOfSellers:
                msg = self._CreateMessage(onlyAnomaliesOfBuyers, onlyAnomaliesOfSellers)

                if self._TGSender(msg):
                    result = {"result": "success", "message": "Anomalies found in volumes orders and sent via TG Bot"}

                else:
                    result = {"result": "partial", "message": "Anomalies found in volumes orders, but can not sent via TG Bot"}

            else:
                result = {"result": "cancel", "message": "Anomalies not found in volumes orders"}

        except Exception as e:
            uLogger.debug(tb.format_exc())
            result = {"result": "error", "message": "An error occurred during trade steps execution: {}".format(e)}

        return result

    def Run(self, instruments: list, portfolio: dict = None) -> list[dict]:
        """
        Runner of trade steps for all given instruments tickers.

        :param instruments: Tickers list for trading.
        :param portfolio: This is a dictionary with some sections: `{"raw": {...}, "stat": {...}, "analytics": {...}}`.
        :return: List of dictionaries with trade results for all instruments.
        """
        tag = "{}{}{}{}{}".format(
            "[{}] ".format(self._pipelineId) if self._pipelineId and self._pipelineId > 0 else "",
            "[{}] ".format(self.userName) if self.userName else "",
            "[{}] ".format(self.accountId) if self.accountId else "",
            "[{}] ".format(self.comment) if self.comment else "",
            "[{}] ".format(SCENARIO_ID) if SCENARIO_ID else "",
        )

        uLogger.debug("{}Processing tickers list: {}".format(tag, instruments))

        # --- Preparatory operations, before the main steps of the trade scenario --------------------------------------

        # Gets the user's portfolio once before start iteration by all instruments or using given `portfolio` if it is not empty.
        # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview
        self._portfolio = portfolio if portfolio else self.Overview(show=False)

        # --- Running the main steps of the scenario, in a loop for all given tickers ----------------------------------

        tradeResults = []  # Dictionaries like this: `{"result": "operation's result", "message": "some comments"}`.
        for ticker in instruments:
            uLogger.debug("{}[{}] ticker processing...".format(tag, ticker))

            self.ticker = ticker
            self._curTicker = ticker  # Saving original name of current ticker.

            # Getting raw instrument's data by its ticker from broker cache.
            # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SearchByTicker
            self._rawIData = self.SearchByTicker(requestPrice=False, show=False)

            self.figi = self._rawIData["figi"]
            self._curFIGI = self.figi  # Saving original FIGI ID.

            notEmptyBook = self._UpdateOrderBook()  # Receiving actual prices for current instrument and re-calculating some volume parameters.

            # --- Trying to run scenario steps for current ticker ------------------------------------------------------

            try:
                if notEmptyBook:
                    tradeResults.append(self.Steps())

                else:
                    tradeResults.append({"result": "failure", "message": "Operations are not possible at the moment, try again later"})

                uLogger.info("{}[{}] [{}] {}".format(tag, self._curTicker, tradeResults[-1]["result"], tradeResults[-1]["message"]))

            except Exception as e:
                uLogger.debug(tb.format_exc())
                uLogger.error("{}An error occurred in Trader: {}".format(tag, e))
                tradeResults.append({"result": "error", "message": "An error occurred in Trader"})

            self.ticker = self._curTicker  # Reload current ticker in base class.
            self.figi = self._curFIGI  # Reload current FIGI ID in base class.

            uLogger.debug("{}[{}] ticker processed".format(tag, ticker))

        return tradeResults


def IRunner(**kwargs) -> dict:
    """Runner for one instance of `TradeScenario()` class with all parameters of one instrument."""
    return kwargs["trader"].Run(instruments=kwargs["tasks"], portfolio=kwargs["portfolio"] if "portfolio" in kwargs.keys() else None)


def _IWrapper(kwargs):
    """
    Wrapper to parallelize scenario for all instruments on all pipelines.
    """
    return IRunner(**kwargs)


def ConfigDecorator(func):
    """Some technical operations before scenario runs."""

    def Wrapper(**kwargs):
        if not os.path.exists(kwargs["config"]):
            uLogger.error("Config file not found! Check the path: [{}]".format(os.path.abspath(kwargs["config"])))

            raise Exception("Config file not found")

        if not os.path.exists(kwargs["secrets"]):
            uLogger.error("User account file not found! Check the path: [{}]".format(os.path.abspath(kwargs["secrets"])))

            raise Exception("User account file not found")

        params = yaml.safe_load(open(kwargs["config"], encoding="UTF-8"))  # Loading main config file.
        userData = yaml.safe_load(open(kwargs["secrets"], encoding="UTF-8"))  # Loading config file with user secrets.
        params.update(userData)  # Merging main parameters and secrets.

        uLogger.level = 10  # Log level for TKSBrokerAPI, DEBUG (10) recommended by default.
        uLogger.handlers[0].level = params["consoleVerbosity"]  # Console log level, INFO (20) recommended by default.
        uLogger.handlers[1].level = params["logfileVerbosity"]  # TKSBrokerAPI.log file log level, DEBUG (10) recommended by default.

        # Detect bot token:
        params["botToken"] = params["botToken"] if "botToken" in params.keys() and params["botToken"] else ""
        if not params["botToken"]:
            try:
                params["botToken"] = r"{}".format(os.environ["TKS_BOT_TOKEN"])

                uLogger.debug("Telegram bot token set up from environment variable `TKS_BOT_TOKEN`. See https://core.telegram.org/bots/api#authorizing-your-bot")

            except KeyError:
                params["botToken"] = ""

                uLogger.warning("`botToken` key in `secrets.yaml` file or environment variable `TKS_BOT_TOKEN` is required if you want to send messages via Telegram bot")

        else:
            uLogger.debug("Telegram bot token set up from `botToken` variable")

        # Telegram Chat ID for sending messages:
        if "chatId" in params.keys() and params["chatId"]:
            uLogger.debug("Telegram Chat ID for sending messages was set up from `chatId` variable")

        else:
            params["chatId"] = None

            uLogger.warning("`chatId` variable in `secrets.yaml` file is required if you want to send messages via Telegram bot")

        timeToWork = params["timeToWorkWeekdays"]  # Allowed working period in crontab format, e.g. "*/2 10-21 * * 1-5" mean "From 10:00AM to 22:00PM (including) at weekdays, every 2 minutes".

        uLogger.debug("Real available Host CPU count: {}".format(CPU_COUNT))
        uLogger.debug("How many CPUs will be used for parallel computing: {}".format(CPU_USAGES))
        uLogger.info("{} just started. Crontab: [{}]. Waiting for the next working period...".format(SCENARIO_ID, timeToWork))

        if params["infiniteWorkMode"]:
            iteration = 0  # Iteration counter (1 iteration = trade operations by all instruments were finished).
            executed = False  # At first no finished iteration.

            while True:
                if pycron.is_now(timeToWork):
                    iteration += 1

                    uLogger.info("--- Trade iteration: [{}]".format(iteration))

                    try:
                        func(**params)  # Executing trade operations by all instruments at once.

                    except Exception as e:
                        uLogger.debug(tb.format_exc())
                        uLogger.error("An error occurred: {}".format(e))
                        uLogger.warning("Technical pause {} seconds after failure...".format(params["waitAfterCrash"]))

                        sleep(params["waitAfterCrash"])

                    executed = True  # For the current period, one trading iteration has been completed, we need to wait for the next one.

                    uLogger.info("--- Trade iteration completed: [{}]".format(iteration))

                    uLogger.info("Technical pause {} seconds at the end of each iteration...".format(params["waitAfterIteration"]))

                    sleep(params["waitAfterIteration"])

                else:
                    if executed:
                        uLogger.info("Crontab: [{}]. Waiting for the next working period...".format(timeToWork))
                        executed = False

                    sleep(params["waitNext"])

        else:
            if pycron.is_now(timeToWork):
                uLogger.info("{} runs once, during the allowed working period. Crontab: [{}]".format(SCENARIO_ID, timeToWork))

            else:
                uLogger.warning("{} launches one time during non-working period! Crontab: [{}]".format(SCENARIO_ID, timeToWork))

            try:
                func(**params)  # Executing trade operations by all instruments at once only one time.

            except Exception as e:
                uLogger.debug(tb.format_exc())
                uLogger.error("An error occurred: {}".format(e))

    return Wrapper


@ConfigDecorator
def TradeManager(**kwargs) -> None:
    """
    Runner for a trade scenario. Initialization of an instance of the trading scenario class and parameterization
    of the main trading parameters.

    Release API documentation of TKSBrokerAPI module (release version):
    - en: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html

    The latest documentation on the TKSBrokerAPI platform:
    - en: https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md
    - ru: https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README.md

    The `@ConfigDecorator` received:
    - **config:** str, e.g. `config.yaml`, path to the main configuration YAML-file.
    - **secrets:** str, e.g. `secrets.yaml`, path to the configuration YAML-file with secrets.

    After loading configurations the `@ConfigDecorator` push to the `TradeManager()` next parameters:
    - **kwargs:** dict with all parameters and secrets from YAML-files:
      - **userName:** str, user name for identification in log;
      - **userAccount:** str, `accountId`, also it can set up from `TKS_ACCOUNT_ID` environment variable;
      - **userToken:** str, api-token, also it can set up from `TKS_API_TOKEN` environment variable;
      - **comment:** str, some comment for the user account, can be empty;
      - all other variables from `config.yaml` to parametrize trade scenario.
    """
    # --- Section of operations performed before the main trading iteration --------------------------------------------

    tag = "{}{}{}{}".format(
        "[{}] ".format(kwargs["userName"]) if kwargs["userName"] else "",
        "[{}] ".format(kwargs["userAccount"]) if kwargs["userAccount"] else "",
        "[{}] ".format(kwargs["comment"]) if kwargs["comment"] else "",
        "[{}] ".format(SCENARIO_ID) if SCENARIO_ID else "",
    )

    uLogger.info(">>> Scenario runs: {}".format(tag))

    # Trade Reporter initialization. It also updates the instruments cache once.
    # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer
    reporter = TinkoffBrokerServer(token=kwargs["userToken"], accountId=kwargs["userAccount"])

    # Gets the user's portfolio once before start iteration throw all instruments.
    # This is a dictionary with some sections: `{"raw": {...}, "stat": {...}, "analytics": {...}}`
    # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview
    overview = reporter.Overview(show=False)

    # --- The main section with trade iteration ------------------------------------------------------------------------

    # Splitting list of tickers by equal parts. Parts count is equal to the available CPU for usages:
    pieces = SeparateByEqualParts(elements=kwargs["tickers"], parts=CPU_USAGES, union=True)

    traders = []  # All pipeline is an instance of `TradeScenario()` class and everyone will have their own set of tickers to work with

    # We create a pool of pipelines, the maximum number of which can be equal to CPU_USAGES (the number of processors, minus one).
    # Then we pass own list of tasks to each pipeline, contains tickers of instruments that need to be processed.
    for i, piece in enumerate(pieces):
        traders.append(
            {
                "trader": TradeScenario(
                    userToken=kwargs["userToken"],
                    userAccount=kwargs["userAccount"],
                    userName=kwargs["userName"],
                    comment=kwargs["comment"],
                    pipelineId=i + 1,
                    botToken=kwargs["botToken"],
                    chatId=kwargs["chatId"],
                ),
                "tasks": piece,
                "portfolio": overview,
            }
        )

        # Setting trading parameters from the configuration file for each pipeline:
        UpdateClassFields(traders[-1]["trader"], kwargs["fields"])

    if traders:  # If the pipelines are initialized and parameterized successes, then we launch trade operations in parallel on all pipelines:
        uLogger.info("{}All pipelines initialized, count: [{}], tickers for trading:\n{}".format(
            tag, len(pieces), "\n".join(["[{}]: {}".format(i + 1, pieces[i]) for i, piece in enumerate(pieces)]),
        ))

        with ThreadPool(processes=CPU_USAGES) as poolSteps:  # Create a pool for multiprocessing pipeline
            poolSteps.map(_IWrapper, traders)  # We execute the trading script in parallel mode for all instruments

        poolSteps.join()  # We are waiting for the end of the work of all threads in the pool

    # --- Section of operations performed after the trading iteration --------------------------------------------------

    uLogger.info(">>> Scenario operations completed for all instruments: {}".format(tag))


if __name__ == "__main__":
    try:
        # Initialization, parametrization and run trading scenario for each instrument:
        if len(sys.argv) >= 3:
            TradeManager(config=sys.argv[1], secrets=sys.argv[2])

        else:
            TradeManager(config="config.yaml", secrets="secrets.yaml")

    except KeyboardInterrupt:
        uLogger.warning("TradeManager interrupted by user")

    except BaseException as eMsg:
        uLogger.debug(tb.format_exc())
        uLogger.error("TradeManager error: {}".format(eMsg))
