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
import platform
import shutil
import sys

import yaml
from dateutil.tz import tzlocal
from math import ceil

import pycron
from time import sleep
from datetime import datetime

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger  # Main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSEnums import TKS_PRINT_DATE_TIME_FORMAT, TKS_TICKER_ALIASES, TKS_ORDER_DIRECTIONS, TKS_STOP_ORDER_DIRECTIONS
from tksbrokerapi.TradeRoutines import *


# --- Common technical parameters:

CPU_COUNT = cpu_count()  # Real available Host CPU count
CPU_USAGES = CPU_COUNT - 1 if CPU_COUNT > 1 else 1  # How many CPUs will be used for parallel computing
SCENARIO_ID = "TKSAVDetector"  # Scenario identifier


def ConfigDecorator(func):
    """Some technical operations before scenario runs."""

    def Wrapper(**kwargs):
        if not os.path.exists(kwargs["config"]):
            uLogger.error("Config file not found! Check the path: [{}]".format(os.path.abspath(kwargs["config"])))
            raise Exception("Config file not found")

        if not os.path.exists(kwargs["secrets"]):
            uLogger.error("User account file not found! Check the path: [{}]".format(os.path.abspath(kwargs["secrets"])))
            raise Exception("User account file not found")

        params = yaml.safe_load(open(kwargs["config"], encoding="UTF-8"))  # Loading main config file
        userData = yaml.safe_load(open(kwargs["secrets"], encoding="UTF-8"))  # Loading config file with user secrets
        params.update(userData)  # Merging main parameters and secrets

        uLogger.level = 10  # Log level for TKSBrokerAPI, DEBUG (10) recommended by default
        uLogger.handlers[0].level = params["consoleVerbosity"]  # Console log level, INFO (20) recommended by default
        uLogger.handlers[1].level = params["logfileVerbosity"]  # TKSBrokerAPI.log file log level, DEBUG (10) recommended by default
        timeToWork = params["timeToWorkWeekdays"]  # Allowed working period in crontab format, e.g. "*/2 10-21 * * 1-5" mean "From 10:00AM to 22:00PM (including) at weekdays, every 2 minutes".

        uLogger.debug("Real available Host CPU count: {}".format(CPU_COUNT))
        uLogger.debug("How many CPUs will be used for parallel computing: {}".format(CPU_USAGES))
        uLogger.info("{} just started. Crontab: [{}]. Waiting for the next working period...".format(SCENARIO_ID, timeToWork))

        if params["infiniteWorkMode"]:
            iteration = 0  # Iteration counter (1 iteration = trade operations by all instruments were finished)
            executed = False  # At first no finished iteration

            while True:
                if pycron.is_now(timeToWork):
                    iteration += 1

                    uLogger.info("--- Trade iteration: [{}]".format(iteration))

                    try:
                        func(**params)  # Executing trade operations by all instruments at once

                    except Exception as e:
                        uLogger.error("An error occurred: {}".format(e))
                        uLogger.warning("Technical pause {} seconds after failure...".format(params["waitAfterCrash"]))

                        sleep(params["waitAfterCrash"])

                    executed = True  # For the current period, one trading iteration has been completed, we need to wait for the next one

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
                func(**params)  # Executing trade operations by all instruments at once only one time

            except Exception as e:
                uLogger.error("An error occurred: {}".format(e))

    return Wrapper


@ConfigDecorator
def TradeManager(**kwargs) -> None:
    """
    Runner for a trade scenario. Initialization of an instance of the trading scenario class and parameterization
    of the main trading parameters.

    Release API documentation of TKSBrokerAPI module (release version):
    - en: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html

    TKSBrokerAPI platform latest documentation:
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

    uLogger.debug("--- Scenario runs: {}".format(tag))

    # Trade Reporter initialization. It also updates the instruments cache once.
    # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer
    reporter = TinkoffBrokerServer(token=kwargs["userToken"], accountId=kwargs["userAccount"])

    # Gets the user's portfolio once before start iteration throw all instruments.
    # This is a dictionary with some sections: `{"raw": {...}, "stat": {...}, "analytics": {...}}
    # TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview
    overview = reporter.Overview(show=False)

    # --- The main section with trade iteration ------------------------------------------------------------------------

    # Splitting list of tickers by equal parts. Parts count is equal to the available CPU for usages:
    pieces = SeparateByEqualParts(elements=kwargs["tickers"], parts=CPU_USAGES, union=True)

    uLogger.debug("Split list of tickers: {}".format(pieces))

    traders = []  # All pipeline is an instance of `TradeScenario()` class and everyone will have their own set of tickers to work with

    uLogger.debug("... DO SOME TRADE JOBS WITH ALL TICKERS ...")

    # --- Section of operations performed after the trading iteration --------------------------------------------------

    uLogger.debug("--- Operations completed for all instruments: {}".format(tag))


if __name__ == "__main__":
    # Initialization, parametrization and run trading scenario for each instrument:
    if len(sys.argv) >= 3:
        TradeManager(config=sys.argv[1], secrets=sys.argv[2])

    else:
        TradeManager(config="config.yaml", secrets="secrets.yaml")
