# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


**Orders Grid Setter** is a simple script demonstrate how to use TKSBrokerAPI platform to set grid of limit or stop orders.
Just run this script with yours parameters in `config.yaml` and `secrets.yaml`.

This script can be set up a grid of orders (limit or stop, buy or sell) with defined steps and lots for a lot of instruments by its
tickers in parallel mode conveyor.

See also, how to parametrize and open a pending limit or stop order using TKSBrokerAPI platform:
https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md#open-a-pending-limit-or-stop-order
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

import os
import sys
import traceback as tb
import yaml

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

# Main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger
from tksbrokerapi.TradeRoutines import *


# --- Common technical parameters:

CPU_COUNT = cpu_count()  # Real available Host CPU count
CPU_USAGES = CPU_COUNT - 1 if CPU_COUNT > 1 else 1  # How many CPUs will be used for parallel computing
SCENARIO_ID = "TKSOrdersGridSetter"  # Scenario identifier


class TradeScenario(TinkoffBrokerServer):
    """This class contains methods for implementing the trading scenario logic."""

    def __init__(self, **kwargs) -> None:
        """
        Initialization and parameterization of the trading scenario.

        **kwargs** parameters can be:
        * **userToken:** str, Tinkoff Invest API token. Or just use `TKS_API_TOKEN` environment variable.
        * **userAccount:** str, user account ID. Or just use `TKS_ACCOUNT_ID` environment variable.
        * **userName:** str, username to identify in log.
        * **comment:** str, some additional comment to identify in log. Can be empty.
        * **pipelineId:** int, number id of the pipeline.

        TKSBrokerAPI api-doc: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__
        """
        super().__init__(token=kwargs["userToken"], accountId=kwargs["userAccount"])  # Initialize main `__init__()` of `TinkoffBrokerServer()` class.
        self.userName = kwargs["userName"]  # Additional identifier for user.
        self.comment = kwargs["comment"]  # Additional comment in log.

        # Main trade parameters loaded from configuration files and replaced here:
        self.testMode = True  # If test mode is `True` then orders will not be opened, only show grid's and orders parameters. If test mode is `False` then orders will be created.
        self.timeout = 30  # Server operations timeout in seconds.
        self.depth = 1  # How deep to request the Depth of Market to analyze current trading volumes, `1 <= depth <= 50`.
        self.target = -1.0  # Start price target to open orders from current price in percent. It can be `> 0` (upper from current price), `< 0` (lower from current price) or `= 0` (target is current price).
        self.gridStep = 0.1  # Grid step from target price in percent. It can be `> 0` (new orders will be upper from target price), `< 0` (new orders will be lower from target price). Step cannot be equal to 0.
        self.count = 10  # Count of orders in grid. It can be `> 0`.
        self.direction = "Buy"  # Direction of orders: `Buy` or `Sell`.
        self.type = "Limit"  # Order type: `Limit` (valid until the end of the trading session) or `Stop` (valid until canceled or until the specified date).
        self.volume = 1  # Volume of instrument in lots, integer `>= 1`.
        self.execType = "Limit"  # This is an optional parameter and only for stop orders. Type of order opened upon reaching the trigger price of the initial stop order, by default it is the string `Limit` or you can specify `SL`, `TP` to open a stop loss or take profit order.
        self.expiration = "Undefined"  # Date of cancellation of orders, by default the string `Undefined` (in this case orders will be valid until canceled) or you can set the local date in the future in format: `%Y-%m-%d %H:%M:%S`.

        # Some parameters calculated during the execution of the trading scenario (not for manual setting):
        self._pipelineId = kwargs["pipelineId"] if "pipelineId" in kwargs.keys() else "*"  # Pipeline ID number.
        self._curTicker = ""  # In `Run()` method we will save original ticker name, before run scenario steps.
        self._curFIGI = ""  # In `Run()` method we will get and save original FIGI identifier, before run scenario steps.
        self._rawIData = {}  # Raw data of one instrument from broker cache.
        self._iData = None  # Information about instrument if it presents in user portfolio.
        self._ordersBook = {"buy": [], "sell": [], "limitUp": 0, "limitDown": 0, "lastPrice": 0, "closePrice": 0}  # Actual broker prices for current instrument.
        self._curPriceToBuy = 0  # The first price in the orders list of Sellers is the current price at which you can buy the instrument (or put it for a sell).
        self._curPriceToSell = 0  # The first price in the orders list of Buyers is the current price at which you can sell the instrument (or put it for a buy).
        self._currency = ""  # The current instrument currency.

        uLogger.debug("Pipeline [{}]: init completed".format(self._pipelineId))

    def _UpdateOrderBook(self) -> bool:
        """
        Receiving actual prices for current instrument, saving to the `_ordersBook` variable and re-calculating some parameters.

        :return: `True` if the order book has been successfully updated, and it is possible to trade (the order book is not empty).
        """
        self.ticker = self._curTicker  # Set current ticker to processing with TKSBrokerAPI.
        self.figi = self._curFIGI  # Set current FIGI ID to processing with TKSBrokerAPI.

        # Receiving DOM, TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetCurrentPrices
        self._ordersBook = self.GetCurrentPrices(show=False)

        if self._ordersBook["buy"] and self._ordersBook["sell"]:
            self._curPriceToBuy = self._ordersBook["buy"][0]["price"]  # The first price in the orders list of Sellers is the current price at which you can buy the instrument (or put it for a sell).
            self._curPriceToSell = self._ordersBook["sell"][0]["price"]  # The first price in the orders list of Buyers is the current price at which you can sell the instrument (or put it for a buy).
            self._currency = self._rawIData["currency"] if self._rawIData and "currency" in self._rawIData.keys() else ""  # The current instrument currency.
            self._step = self._rawIData["step"] if self._rawIData and "step" in self._rawIData.keys() else 1  # The price step of the current instrument.

            uLogger.debug("[{}] Orders book was received success".format(self._curTicker))

            return True

        else:
            self._curPriceToBuy = 0
            self._curPriceToSell = 0
            self._currency = ""
            self._step = 1

            uLogger.debug("[{}] An empty orders book was returned or non-trading time".format(self._curTicker))

            return False

    def Steps(self) -> dict:
        """
        Section for implementing the steps of the trading scenario for one current instrument.

        :return: Dictionary with trade results, e.g. `{"result": "success", "message": "All trade steps were finished success"}`.
        """
        self.ticker = self._curTicker  # Set current ticker to processing with TKSBrokerAPI.
        self.figi = self._curFIGI  # Set current FIGI ID to processing with TKSBrokerAPI.

        try:
            # --- Calculating orders grid parameters -------------------------------------------------------------------
            # List of task looks like dictionary with input parameters for Order() method:
            # {"operation": str, "orderType": str, "lots": int, "targetPrice": float, "limitPrice": float, "stopType": str, "expDate": str}
            # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Order

            tasks = []
            infoText = "Prepared tasks for opening orders grid:\n"
            infoText += "| No. | Operation | orderType | lots   | targetPrice  | limitPrice | stopType | expDate             |\n".format(self._currency)
            infoText += "|-----|-----------|-----------|--------|--------------|------------|----------|---------------------|"

            curPrice = self._curPriceToBuy if self.direction == "Sell" else self._curPriceToSell

            debugText = "{}[{}] Grid parameters:\n".format("[Test mode] " if self.testMode else "", self.ticker)
            debugText += "Current price, curPrice = {}\n".format(curPrice)
            debugText += "Current price step, self._step = {}\n".format(self._step)
            debugText += "Target price change, target = {}%\n".format(self.target)
            debugText += "Grid step from target price, gridStep = {}%\n".format(self.gridStep)
            debugText += "Count of orders in grid, count = {}".format(self.count)
            uLogger.debug(debugText)

            for n in range(self.count):
                # Real target for the next order:
                realTarget = curPrice * (1 + (self.target + n * self.gridStep) / 100)

                # The order target must be a multiple of the instrument price step:
                iteratedPrice = round(self._step * (abs(realTarget - curPrice) // self._step), 6)
                sign = 1 if self.target >= 0 else -1
                orderTarget = round(curPrice + sign * iteratedPrice, 6)

                task = {
                    "operation": self.direction,
                    "orderType": self.type,
                    "lots": self.volume,
                    "targetPrice": orderTarget,
                    "limitPrice": 0,  # Always open limit order by current target price.
                    "stopType": self.execType,
                    "expDate": self.expiration,
                }
                tasks.append(task)

                infoText += "\n| {:<3} | {:<9} | {:<9} | {:<6} | {:<12} | {:<10} | {:<8} | {:<19} |".format(n + 1, *list(task.values()))

            if self.testMode:
                uLogger.info("[Test mode] [{}] {}".format(self._curTicker, infoText))

            else:
                uLogger.debug("[{}] {}".format(self._curTicker, infoText))

            # --- Opening orders for current instrument ---------------------------------------------------------------

            if not self.testMode:
                for task in tasks:
                    self.Order(**task)

            # --- Final steps ------------------------------------------------------------------------------------------

            if self.testMode:
                result = {"result": "success", "message": "[Test mode] Only orders parameters were calculated. Real orders do not opening!"}

            else:
                result = {"result": "success", "message": "All orders were placed"}

        except Exception as e:
            uLogger.debug(tb.format_exc())
            result = {"result": "error", "message": "An error occurred during trade steps execution: {}".format(e)}

        return result

    def Run(self, instruments: list) -> list[dict]:
        """
        Runner of trade steps for all given instruments tickers.

        :param instruments: Tickers list for trading.
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

            notEmptyBook = self._UpdateOrderBook()  # Receiving actual prices for current instrument and re-calculating some parameters.

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
    return kwargs["trader"].Run(instruments=kwargs["tasks"])


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

        uLogger.debug("Real available Host CPU count: {}".format(CPU_COUNT))
        uLogger.debug("How many CPUs will be used for parallel computing: {}".format(CPU_USAGES))

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
      - **userName:** str, username for identification in log;
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
                ),
                "tasks": piece,
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

    # Gets the user's portfolio and new orders after all operations.
    # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview
    if not kwargs["fields"]["testMode"]:
        reporter.Overview(show=True, details="orders")

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
