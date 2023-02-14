# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)

**TKSBrokerAPI** is the trading platform for automation and simplifying the implementation of trading scenarios,
as well as working with Tinkoff Invest API server via the REST protocol. The TKSBrokerAPI platform may be used in two ways:
from the console, it has a rich keys and commands, or you can use it as Python module with `python import`.

TKSBrokerAPI allows you to automate routine trading operations and implement your trading scenarios, or just receive
the necessary information from the broker. It is easy enough to integrate into various CI/CD automation systems.

See also:
- **Open account for trading:** https://tinkoff.ru/sl/AaX1Et1omnH
- **TKSBrokerAPI module documentation:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
- **CLI examples:** https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Usage-examples
- **Used constants are in the TKSEnums module:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSEnums.html
- **About Tinkoff Invest API:** https://tinkoff.github.io/investAPI/
- **Tinkoff Invest API documentation:** https://tinkoff.github.io/investAPI/swagger-ui/
- **How to implement trading scenario in Python:** https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Module-import

[Using the TKSBrokerAPI module](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Module-import),
you can implement any trading scenario in Python. Many system used for making trading decisions about buying or selling
(technical analysis, neural networks, parsing reports or tracking other traders’ transactions), but you still need
to perform trading operations: place orders, open and close transactions. The `TKSBrokerAPI` module will act as an
intermediary between the code with the trading logic and services infrastructure of the Tinkoff Investments broker,
as well as perform routine tasks on your behalf in [brokerage account](https://tinkoff.ru/sl/AaX1Et1omnH).

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/docs/media/TKSBrokerAPI-flow.png?raw=true" alt="TKSBrokerAPI-flow" width="780" /></a>

The scheme of trade scenario automation with TKSBrokerAPI is very simple:
1. You come up with a brilliant trading algorithm.
2. Write it down step by step in the form of some kind of plan or trading scenario.
3. Automate scenario as a Python script using TKSBrokerAPI.
4. TKSBrokerAPI takes care of all the work with the Tinkoff Investments broker infrastructure.
5. Profit!

But where to get this "brilliant trading algorithm"? The TKSBrokerAPI platform will also help you solve the problem
of obtaining primary, "raw" data on trading instruments (shares, bonds, funds, futures and currencies) from the broker
server, for their future analysis in any analytical tool convenient for you. To do this, the methods of the TKSBrokerAPI
module provide the ability to extend and save data in classic formats: XLSX and CSV (for analysis in spreadsheet editors),
Markdown (for readability), and Pandas DataFrame (for data scientists and stock analysts).

The "raw" data can be anything that [can be obtained](https://tinkoff.github.io/investAPI/swagger-ui/) from the broker's
server. After extends, this data can be used to build, for example, a [consolidated payment calendar](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Build-a-bond-payment-calendar)
for bonds and calculate their [coupon and current yields](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Get-extended-bonds-data),
or you can generate analytics about the status of the user's portfolio and the [distribution of assets](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Get-the-current-portfolio-and-asset-allocation-statistics)
by types, companies, industries, currencies, and countries. In addition, you can download [historical data](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Download-historical-data-in-OHLCV-candles-format)
on the prices of any instrument as OHLCV-candlesticks.

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/docs/media/TKSBrokerAPI-extend-data-flow.png?raw=true" alt="TKSBrokerAPI-extend-data-flow" width="780" /></a>

How data is extended and used in TKSBrokerAPI:
1. You request the data you need from the Tinkoff Investments broker server using the TKSBrokerAPI module:
   - in this module, almost all methods return "raw" data from the server in the form of a Python dictionary.
2. Then they are processed and extended:
   - with various statistics, parameters and some analytical reports.
3. After that, the data is stored in a form suitable for further analysis:
   - most of the methods return extended data in the form of a Python dictionary or Pandas DataFrame;
   - if you launched the TKSBrokerAPI platform in the console, then the data will be saved in XLSX, CSV or Markdown formats.
4. Next, you can load the data into analytical system and use various data analysis methods to find and highlight
   dependencies, correlations, make predictions and suggest hypothesis.
5. Further, based on data analysis, you come up with the same "brilliant trading algorithm".
6. Automate the trading scenario (according to the previous scheme).
7. Profit!
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


import sys
import os
from argparse import ArgumentParser
from importlib.metadata import version

from dateutil.tz import tzlocal
from time import sleep

import re
import json
import requests
import traceback as tb

from multiprocessing import cpu_count, Lock
from multiprocessing.pool import ThreadPool

from mako.template import Template  # Mako Templates for Python (https://www.makotemplates.org/). Mako is a template library provides simple syntax and maximum performance.
from Templates import *  # Some html-templates used by reporting methods in TKSBrokerAPI module
from TKSEnums import *  # A lot of constants from enums sections: https://tinkoff.github.io/investAPI/swagger-ui/
from TradeRoutines import *  # This library contains some methods used by trade scenarios implemented with TKSBrokerAPI module

from pricegenerator.PriceGenerator import PriceGenerator, uLogger  # This module has a lot of instruments to work with candles data (https://github.com/Tim55667757/PriceGenerator)
from pricegenerator.UniLogger import DisableLogger as PGDisLog  # Method for disable log from PriceGenerator

import UniLogger as uLog  # Logger for TKSBrokerAPI


# --- Common technical parameters:

PGDisLog(uLogger.handlers[0])  # Disable 3-rd party logging from PriceGenerator
uLogger = uLog.UniLogger  # init logger for TKSBrokerAPI
uLogger.level = 10  # debug level by default for TKSBrokerAPI module
uLogger.handlers[0].level = 20  # info level by default for STDOUT of TKSBrokerAPI module

__version__ = "1.6"  # The "major.minor" version setup here, but build number define at the build-server only

CPU_COUNT = cpu_count()  # host's real CPU count
CPU_USAGES = CPU_COUNT - 1 if CPU_COUNT > 1 else 1  # how many CPUs will be used for parallel calculations


class TinkoffBrokerServer:
    """
    This class implements methods to work with Tinkoff broker server.

    Examples to work with API: https://tinkoff.github.io/investAPI/swagger-ui/

    About `token`: https://tinkoff.github.io/investAPI/token/
    """
    def __init__(self, token: str, accountId: str = None, useCache: bool = True, defaultCache: str = "dump.json") -> None:
        """
        Main class init.

        :param token: Bearer token for Tinkoff Invest API. It can be set from environment variable `TKS_API_TOKEN`.
        :param accountId: string with numeric user account ID in Tinkoff Broker. It can be found in broker's reports.
                          Also, this variable can be set from environment variable `TKS_ACCOUNT_ID`.
        :param useCache: use default cache file with raw data to use instead of `iList`.
                         True by default. Cache is auto-update if new day has come.
                         If you don't want to use cache and always updates raw data then set `useCache=False`.
        :param defaultCache: path to default cache file. `dump.json` by default.
        """
        if token is None or not token:
            try:
                self.token = r"{}".format(os.environ["TKS_API_TOKEN"])
                uLogger.debug("Bearer token for Tinkoff OpenAPI set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/")

            except KeyError:
                uLogger.error("`--token` key or environment variable `TKS_API_TOKEN` is required! See https://tinkoff.github.io/investAPI/token/")
                raise Exception("Token required")

        else:
            self.token = token  # highly priority than environment variable 'TKS_API_TOKEN'
            uLogger.debug("Bearer token for Tinkoff OpenAPI set up from class variable `token`")

        if accountId is None or not accountId:
            try:
                self.accountId = r"{}".format(os.environ["TKS_ACCOUNT_ID"])
                uLogger.debug("Main account ID [{}] set up from environment variable `TKS_ACCOUNT_ID`".format(self.accountId))

            except KeyError:
                uLogger.warning("`--account-id` key or environment variable `TKS_ACCOUNT_ID` undefined! Some of operations may be unavailable (overview, trading etc).")

        else:
            self.accountId = accountId  # highly priority than environment variable 'TKS_ACCOUNT_ID'
            uLogger.debug("Main account ID [{}] set up from class variable `accountId`".format(self.accountId))

        self.version = __version__  # duplicate here used TKSBrokerAPI main version
        """Current TKSBrokerAPI version: major.minor, but the build number define at the build-server only.

        Latest version: https://pypi.org/project/tksbrokerapi/
        """

        self._tag = ""
        """Identification TKSBrokerAPI tag in log messages to simplify debugging when platform instances runs in parallel mode. Default: `""` (empty string)."""

        self.__lock = Lock()  # initialize multiprocessing mutex lock

        self._precision = 4  # precision, signs after comma, e.g. 2 for instruments like PLZL, 4 for instruments like USDRUB, if -1 then auto detect it when load data-file

        self.aliases = TKS_TICKER_ALIASES
        """Some aliases instead official tickers.

        See also: `TKSEnums.TKS_TICKER_ALIASES`
        """

        self.aliasesKeys = self.aliases.keys()  # re-calc only first time at class init

        self.exclude = TKS_TICKERS_OR_FIGI_EXCLUDED  # some tickers or FIGIs raised exception earlier when it sends to server, that is why we exclude there

        self._ticker = ""
        """String with ticker, e.g. `GOOGL`. Tickers may be upper case only.

        Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR` etc.
        More tickers aliases here: `TKSEnums.TKS_TICKER_ALIASES`.

        See also: `SearchByTicker()`, `SearchInstruments()`.
        """

        self._figi = ""
        """String with FIGI, e.g. ticker `GOOGL` has FIGI `BBG009S39JX6`. FIGIs may be upper case only.

        See also: `SearchByFIGI()`, `SearchInstruments()`.
        """

        self.depth = 1
        """Depth of Market (DOM) can be >= 1. Default: 1. It used with `--price` key to showing DOM with current prices for givens ticker or FIGI.

        See also: `GetCurrentPrices()`.
        """

        self.server = r"https://invest-public-api.tinkoff.ru/rest"
        """Tinkoff REST API server for real trade operations. Default: https://invest-public-api.tinkoff.ru/rest

        See also: API method https://tinkoff.github.io/investAPI/#tinkoff-invest-api_1 and `SendAPIRequest()`.
        """

        uLogger.debug("Broker API server: {}".format(self.server))

        self.timeout = 15
        """Server operations timeout in seconds. Default: `15`.

        See also: `SendAPIRequest()`.
        """

        self.retry = 3
        """
        How many times retry after first request if a 5xx server errors occurred. If set to 0, then only first main
        request will be sent without retries. This allows you to reduce the number of calls to the server API for all methods.

        3 times of retries by default.

        See also: `SendAPIRequest()`.
        """

        self.pause = 5
        """Sleep time in seconds between retries, in all network requests 5 seconds by default.

        See also: `SendAPIRequest()`.
        """

        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": "Bearer {}".format(self.token),
            "x-app-name": "Tim55667757.TKSBrokerAPI",
        }
        """
        Headers which send in every request to broker server. Please, do not change it!
        Default: `{"Content-Type": "application/json", "accept": "application/json", "Authorization": "Bearer {your_token}", "x-app-name": "Tim55667757.TKSBrokerAPI"}`.

        See also: `SendAPIRequest()`.
        """

        self.body = None
        """Request body which send to broker server. Default: `None`.

        See also: `SendAPIRequest()`.
        """

        self.moreDebug = False
        """Enables more debug information in this class, such as net request and response headers in all methods. `False` by default."""

        self.useHTMLReports = False
        """
        If `True` then TKSBrokerAPI generate also HTML reports from Markdown. `False` by default.
        
        See also: Mako Templates for Python (https://www.makotemplates.org/). Mako is a template library provides simple syntax and maximum performance.
        """

        self.historyFile = None
        """Full path to the output file where history candles will be saved or updated. Default: `None`, it mean that returns only Pandas DataFrame.

        See also: `History()`.
        """

        self.htmlHistoryFile = "index.html"
        """Full path to the html file where rendered candles chart stored. Default: `index.html`.

        See also: `ShowHistoryChart()`.
        """

        self.instrumentsFile = "instruments.md"
        """Filename where full available to user instruments list will be saved. Default: `instruments.md`.

        See also: `ShowInstrumentsInfo()`.
        """

        self.searchResultsFile = "search-results.md"
        """Filename with all found instruments searched by part of its ticker, FIGI or name. Default: `search-results.md`.

        See also: `SearchInstruments()`.
        """

        self.pricesFile = "prices.md"
        """Filename where prices of selected instruments will be saved. Default: `prices.md`.

        See also: `GetListOfPrices()`.
        """

        self.infoFile = "info.md"
        """Filename where prices of selected instruments will be saved. Default: `prices.md`.

        See also: `ShowInstrumentsInfo()`, `RequestBondCoupons()` and `RequestTradingStatus()`.
        """

        self.bondsXLSXFile = "ext-bonds.xlsx"
        """Filename where wider Pandas DataFrame with more information about bonds: main info, current prices, 
        bonds payment calendar, some statistics will be stored. Default: `ext-bonds.xlsx`.

        See also: `ExtendBondsData()`.
        """

        self.calendarFile = "calendar.md"
        """Filename where bonds payment calendar will be saved. Default: `calendar.md`.
        
        Pandas dataframe with only bonds payment calendar also will be stored to default file `calendar.xlsx`.

        See also: `CreateBondsCalendar()`, `ShowBondsCalendar()`, `ShowInstrumentInfo()`, `RequestBondCoupons()` and `ExtendBondsData()`.
        """

        self.overviewFile = "overview.md"
        """Filename where current portfolio, open trades and orders will be saved. Default: `overview.md`.

        See also: `Overview()`, `RequestPortfolio()`, `RequestPositions()`, `RequestPendingOrders()` and `RequestStopOrders()`.
        """

        self.overviewDigestFile = "overview-digest.md"
        """Filename where short digest of the portfolio status will be saved. Default: `overview-digest.md`.

        See also: `Overview()` with parameter `details="digest"`.
        """

        self.overviewPositionsFile = "overview-positions.md"
        """Filename where only open positions, without everything else will be saved. Default: `overview-positions.md`.

        See also: `Overview()` with parameter `details="positions"`.
        """

        self.overviewOrdersFile = "overview-orders.md"
        """Filename where open limits and stop orders will be saved. Default: `overview-orders.md`.

        See also: `Overview()` with parameter `details="orders"`.
        """

        self.overviewAnalyticsFile = "overview-analytics.md"
        """Filename where only the analytics section and the distribution of the portfolio by various categories will be saved. Default: `overview-analytics.md`.

        See also: `Overview()` with parameter `details="analytics"`.
        """

        self.overviewBondsCalendarFile = "overview-calendar.md"
        """Filename where only the bonds calendar section will be saved. Default: `overview-calendar.md`.

        See also: `Overview()` with parameter `details="calendar"`.
        """

        self.reportFile = "deals.md"
        """Filename where history of deals and trade statistics will be saved. Default: `deals.md`.

        See also: `Deals()`.
        """

        self.withdrawalLimitsFile = "limits.md"
        """Filename where table of funds available for withdrawal will be saved. Default: `limits.md`.

        See also: `OverviewLimits()` and `RequestLimits()`.
        """

        self.userInfoFile = "user-info.md"
        """Filename where all available user's data (`accountId`s, common user information, margin status and tariff connections limit) will be saved. Default: `user-info.md`.

        See also: `OverviewUserInfo()`, `RequestAccounts()`, `RequestUserInfo()`, `RequestMarginStatus()` and `RequestTariffLimits()`.
        """

        self.userAccountsFile = "accounts.md"
        """Filename where simple table with all available user accounts (`accountId`s) will be saved. Default: `accounts.md`.

        See also: `OverviewAccounts()`, `RequestAccounts()`.
        """

        self.iListDumpFile = "dump.json" if defaultCache is None or not isinstance(defaultCache, str) or not defaultCache else defaultCache
        """Filename where raw data about shares, currencies, bonds, etfs and futures will be stored. Default: `dump.json`.

        Pandas dataframe with raw instruments data also will be stored to default file `dump.xlsx`.

        See also: `DumpInstruments()` and `DumpInstrumentsAsXLSX()`.
        """

        self.iList = None  # init iList for raw instruments data
        """Dictionary with raw data about shares, currencies, bonds, etfs and futures from broker server. Auto-updating and saving dump to the `iListDumpFile`.
        
        See also: `Listing()`, `DumpInstruments()`.
        """

        # trying to re-load raw instruments data from file `iListDumpFile` or try to update it from server:
        if useCache:
            if os.path.exists(self.iListDumpFile):
                dumpTime = datetime.fromtimestamp(os.path.getmtime(self.iListDumpFile)).astimezone(tzutc())  # dump modification date and time
                curTime = datetime.now(tzutc())

                if (curTime.day > dumpTime.day) or (curTime.month > dumpTime.month) or (curTime.year > dumpTime.year):
                    uLogger.warning("Local cache may be outdated! It has last modified [{}] UTC. Updating from broker server, wait, please...".format(dumpTime.strftime(TKS_PRINT_DATE_TIME_FORMAT)))

                    self.DumpInstruments(forceUpdate=True)  # updating self.iList and dump file

                else:
                    self.iList = json.load(open(self.iListDumpFile, mode="r", encoding="UTF-8"))  # load iList from dump

                    uLogger.debug("Local cache with raw instruments data is used: [{}]. Last modified: [{}] UTC".format(
                        os.path.abspath(self.iListDumpFile),
                        dumpTime.strftime(TKS_PRINT_DATE_TIME_FORMAT),
                    ))

            else:
                uLogger.warning("Local cache with raw instruments data not exists! Creating new dump, wait, please...")
                self.DumpInstruments(forceUpdate=True)  # updating self.iList and creating default dump file

        else:
            self.iList = self.Listing()  # request new raw instruments data from broker server
            self.DumpInstruments(forceUpdate=False)  # save raw instrument's data to default dump file `iListDumpFile`

        self.priceModel = PriceGenerator()  # init PriceGenerator object to work with candles data
        """PriceGenerator object to work with candles data: load, render interact and non-interact charts and so on.

        See also: `LoadHistory()`, `ShowHistoryChart()` and the PriceGenerator project: https://github.com/Tim55667757/PriceGenerator
        """

    @property
    def tag(self) -> str:
        """Identification TKSBrokerAPI tag in log messages to simplify debugging when platform instances runs in parallel mode. Default: `""` (empty string)."""
        return self._tag

    @tag.setter
    def tag(self, value):
        """Setter for Identification TKSBrokerAPI tag in log messages to simplify debugging when platform instances runs in parallel mode. Default: `""` (empty string)."""
        self._tag = str(value)

        if self._tag:
            for handler in uLogger.handlers:
                handler.setFormatter(uLog.logging.Formatter(uLog.formatStringWithTag.format(tag=self._tag)))

            uLogger.debug("Custom TKSBrokerAPI tag was set: {}".format(self._tag))

        else:
            for handler in uLogger.handlers:
                handler.setFormatter(uLog.logging.Formatter(uLog.formatString))

            uLogger.debug("Default logger format is used")

    @property
    def ticker(self) -> str:
        """String with ticker, e.g. `GOOGL`. Tickers may be upper case only.

        Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR` etc.
        More tickers aliases here: `TKSEnums.TKS_TICKER_ALIASES`.

        See also: `SearchByTicker()`, `SearchInstruments()`.
        """
        return self._ticker

    @ticker.setter
    def ticker(self, value):
        """Setter for string with ticker, e.g. `GOOGL`. Tickers may be upper case only.

        Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR` etc.
        More tickers aliases here: `TKSEnums.TKS_TICKER_ALIASES`.

        See also: `SearchByTicker()`, `SearchInstruments()`.
        """
        self._ticker = str(value).upper()  # Tickers may be upper case only

    @property
    def figi(self) -> str:
        """String with FIGI, e.g. ticker `GOOGL` has FIGI `BBG009S39JX6`. FIGIs may be upper case only.

        See also: `SearchByFIGI()`, `SearchInstruments()`.
        """
        return self._figi

    @figi.setter
    def figi(self, value):
        """Setter for string with FIGI, e.g. ticker `GOOGL` has FIGI `BBG009S39JX6`. FIGIs may be upper case only.

        See also: `SearchByFIGI()`, `SearchInstruments()`.
        """
        self._figi = str(value).upper()  # FIGI may be upper case only

    def _ParseJSON(self, rawData="{}") -> dict:
        """
        Parse JSON from response string.

        :param rawData: this is a string with JSON-formatted text.
        :return: JSON (dictionary), parsed from server response string. If an error occurred, then returns empty dict `{}`.
        """
        try:
            responseJSON = json.loads(rawData) if rawData else {}

            if self.moreDebug:
                uLogger.debug("JSON formatted raw body data of response:\n{}".format(json.dumps(responseJSON, indent=4)))

            return responseJSON

        except Exception as e:
            uLogger.debug(tb.format_exc())
            uLogger.error("An empty dict will be return, because an error occurred in `_ParseJSON()` method with comment: {}".format(e))

            return {}

    def SendAPIRequest(self, url: str, reqType: str = "GET") -> dict:
        """
        Send GET or POST request to broker server and receive JSON object.

        self.header: must be defining with dictionary of headers.
        self.body: if define then used as request body. None by default.
        self.timeout: global request timeout, 15 seconds by default.
        :param url: url with REST request.
        :param reqType: send "GET" or "POST" request. "GET" by default.
        :return: response JSON (dictionary) from broker.
        """
        if reqType.upper() not in ("GET", "POST"):
            uLogger.error("You can define request type: `GET` or `POST`!")
            raise Exception("Incorrect value")

        if self.moreDebug:
            uLogger.debug("Request parameters:")
            uLogger.debug("    - REST API URL: {}".format(url))
            uLogger.debug("    - request type: {}".format(reqType))
            uLogger.debug("    - headers:\n{}".format(str(self.headers).replace(self.token, "*** request token ***")))
            uLogger.debug("    - body:\n{}".format(self.body))

        # fast hack to avoid all operations with some tickers/FIGI
        responseJSON = {}
        oK = True
        for item in self.exclude:
            if item in url:
                if self.moreDebug:
                    uLogger.warning("Do not execute operations with list of this tickers/FIGI: {}".format(str(self.exclude)))

                oK = False
                break

        if oK:
            with self.__lock:  # acquire the mutex lock
                counter = 0
                response = None
                errMsg = ""

                while not response and counter <= self.retry:
                    if reqType == "GET":
                        response = requests.get(url, headers=self.headers, data=self.body, timeout=self.timeout)

                    if reqType == "POST":
                        response = requests.post(url, headers=self.headers, data=self.body, timeout=self.timeout)

                    if self.moreDebug:
                        uLogger.debug("Response:")
                        uLogger.debug("    - status code: {}".format(response.status_code))
                        uLogger.debug("    - reason: {}".format(response.reason))
                        uLogger.debug("    - body length: {}".format(len(response.text)))
                        uLogger.debug("    - headers:\n{}".format(response.headers))

                    # Server returns some headers:
                    # - `x-ratelimit-limit` — shows the settings of the current user limit for this method.
                    # - `x-ratelimit-remaining` — the number of remaining requests of this type per minute.
                    # - `x-ratelimit-reset` — time in seconds before resetting the request counter.
                    # See: https://tinkoff.github.io/investAPI/grpc/#kreya
                    if "x-ratelimit-remaining" in response.headers.keys() and response.headers["x-ratelimit-remaining"] == "0":
                        rateLimitWait = int(response.headers["x-ratelimit-reset"])
                        uLogger.debug("Rate limit exceeded. Waiting {} sec. for reset rate limit and then repeat again...".format(rateLimitWait))
                        sleep(rateLimitWait)

                    # Error status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                    if 400 <= response.status_code < 500:
                        msg = "status code: [{}], response body: {}".format(response.status_code, response.text)
                        uLogger.debug("    - not oK, but do not retry for 4xx errors, {}".format(msg))

                        if "code" in response.text and "message" in response.text:
                            msgDict = self._ParseJSON(rawData=response.text)
                            uLogger.warning("HTTP-status code [{}], server message: {}".format(response.status_code, msgDict["message"]))

                        counter = self.retry + 1  # do not retry for 4xx errors

                    if 500 <= response.status_code < 600:
                        errMsg = "status code: [{}], response body: {}".format(response.status_code, response.text)
                        uLogger.debug("    - not oK, {}".format(errMsg))

                        if "code" in response.text and "message" in response.text:
                            errMsgDict = self._ParseJSON(rawData=response.text)
                            uLogger.warning("HTTP-status code [{}], error message: {}".format(response.status_code, errMsgDict["message"]))

                        counter += 1

                        if counter <= self.retry:
                            uLogger.debug("Retry: [{}]. Wait {} sec. and try again...".format(counter, self.pause))
                            sleep(self.pause)

                responseJSON = self._ParseJSON(rawData=response.text)

                if errMsg:
                    uLogger.error("Server returns not `oK` status! See: https://tinkoff.github.io/investAPI/errors/")
                    uLogger.error("    - not oK, {}".format(errMsg))

        return responseJSON

    def _IUpdater(self, iType: str) -> tuple:
        """
        Request instrument by type from server. See available API methods for instruments:
        Currencies: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_Currencies
        Shares: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_Shares
        Bonds: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_Bonds
        Etfs: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_Etfs
        Futures: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_Futures

        :param iType: type of the instrument, it must be one of supported types in TKS_INSTRUMENTS list.
        :return: tuple with iType name and list of available instruments of current type for defined user token.
        """
        result = []

        if iType in TKS_INSTRUMENTS:
            uLogger.debug("Requesting available [{}] list. Wait, please...".format(iType))

            # all instruments have the same body in API v2 requests:
            self.body = str({"instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"})  # Enum: [INSTRUMENT_STATUS_UNSPECIFIED, INSTRUMENT_STATUS_BASE, INSTRUMENT_STATUS_ALL]
            instrumentURL = self.server + r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/{}".format(iType)
            result = self.SendAPIRequest(instrumentURL, reqType="POST")["instruments"]

        return iType, result

    def _IWrapper(self, kwargs):
        """
        Wrapper runs instrument's update method `_IUpdater()`.
        It's a workaround for using multiprocessing with kwargs. See: https://stackoverflow.com/a/36799206
        """
        return self._IUpdater(**kwargs)

    def Listing(self) -> dict:
        """
        Gets JSON with raw data about shares, currencies, bonds, etfs and futures from broker server.

        :return: Dictionary with all available broker instruments: currencies, shares, bonds, etfs and futures.
        """
        uLogger.debug("Requesting all available instruments for current account. Wait, please...")
        uLogger.debug("CPU usages for parallel requests: [{}]".format(CPU_USAGES))

        # this parameters insert to requests: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService
        # iType is type of instrument, it must be one of supported types in TKS_INSTRUMENTS list.
        iParams = [{"iType": iType} for iType in TKS_INSTRUMENTS]

        poolUpdater = ThreadPool(processes=CPU_USAGES)  # create pool for update instruments in parallel mode
        listing = poolUpdater.map(self._IWrapper, iParams)  # execute update operations
        poolUpdater.close()  # close the thread pool
        poolUpdater.join()  # wait a moment until all data returns from threads

        # Dictionary with all broker instruments: shares, currencies, bonds, etfs and futures.
        # Next in this code: item[0] is "iType" and item[1] is list of available instruments from the result of _IUpdater() method
        iList = {item[0]: {instrument["ticker"]: instrument for instrument in item[1]} for item in listing}

        # calculate minimum price increment (step) for all instruments and set up instrument's type:
        for iType in iList.keys():
            for ticker in iList[iType]:
                iList[iType][ticker]["type"] = iType

                if "minPriceIncrement" in iList[iType][ticker].keys():
                    iList[iType][ticker]["step"] = NanoToFloat(
                        iList[iType][ticker]["minPriceIncrement"]["units"],
                        iList[iType][ticker]["minPriceIncrement"]["nano"],
                    )

                else:
                    iList[iType][ticker]["step"] = 0  # hack to avoid empty value in some instruments, e.g. futures

        return iList

    def DumpInstrumentsAsXLSX(self, forceUpdate: bool = False) -> None:
        """
        Creates XLSX-formatted dump file with raw data of instruments to further used by data scientists or stock analytics.

        See also: `DumpInstruments()`, `Listing()`.

        :param forceUpdate: if `True` then at first updates data with `Listing()` method,
                            otherwise just saves exist `iList` as XLSX-file (default: `dump.xlsx`) .
        """
        if self.iListDumpFile is None or not self.iListDumpFile:
            uLogger.error("Output name of dump file must be defined!")
            raise Exception("Filename required")

        if not self.iList or forceUpdate:
            self.iList = self.Listing()

        xlsxDumpFile = self.iListDumpFile.replace(".json", ".xlsx") if self.iListDumpFile.endswith(".json") else self.iListDumpFile + ".xlsx"

        # Save as XLSX with separated sheets for every type of instruments:
        with pd.ExcelWriter(
                path=xlsxDumpFile,
                date_format=TKS_DATE_FORMAT,
                datetime_format=TKS_DATE_TIME_FORMAT,
                mode="w",
        ) as writer:
            for iType in TKS_INSTRUMENTS:
                df = pd.DataFrame.from_dict(data=self.iList[iType], orient="index")  # generate pandas object from self.iList dictionary
                df = df[sorted(df)]  # sorted by column names
                df = df.applymap(
                    lambda item: NanoToFloat(item["units"], item["nano"]) if isinstance(item, dict) and "units" in item.keys() and "nano" in item.keys() else item,
                    na_action="ignore",
                )  # converting numbers from nano-type to float in every cell
                df.to_excel(
                    writer,
                    sheet_name=iType,
                    encoding="UTF-8",
                    freeze_panes=(1, 1),
                )  # saving as XLSX-file with freeze first row and column as headers

        uLogger.info("XLSX-file for further used by data scientists or stock analytics: [{}]".format(os.path.abspath(xlsxDumpFile)))

    def DumpInstruments(self, forceUpdate: bool = True) -> str:
        """
        Receives and returns actual raw data about shares, currencies, bonds, etfs and futures from broker server
        using `Listing()` method. If `iListDumpFile` string is not empty then also save information to this file.

        See also: `DumpInstrumentsAsXLSX()`, `Listing()`.

        :param forceUpdate: if `True` then at first updates data with `Listing()` method,
                            otherwise just saves exist `iList` as JSON-file (default: `dump.json`).
        :return: serialized JSON formatted `str` with full data of instruments, also saved to the `--output` JSON-file.
        """
        if self.iListDumpFile is None or not self.iListDumpFile:
            uLogger.error("Output name of dump file must be defined!")
            raise Exception("Filename required")

        if not self.iList or forceUpdate:
            self.iList = self.Listing()

        jsonDump = json.dumps(self.iList, indent=4, sort_keys=False)  # create JSON object as string
        with open(self.iListDumpFile, mode="w", encoding="UTF-8") as fH:
            fH.write(jsonDump)

        uLogger.info("New cache of instruments data was created: [{}]".format(os.path.abspath(self.iListDumpFile)))

        return jsonDump

    def ShowInstrumentInfo(self, iJSON: dict, show: bool = True, onlyFiles=False) -> str:
        """
        Show information about one instrument defined by json data and prints it in Markdown format.

        See also: `SearchByTicker()`, `SearchByFIGI()`, `RequestBondCoupons()`, `ExtendBondsData()`, `ShowBondsCalendar()` and `RequestTradingStatus()`.

        :param iJSON: json data of instrument, example: `iJSON = self.iList["Shares"][self._ticker]`
        :param show: if `True` then also printing information about instrument and its current price.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: multilines text in Markdown format with information about one instrument.
        """
        splitLine = "|                                                             |                                                        |\n"
        infoText = ""

        if iJSON is not None and iJSON and isinstance(iJSON, dict):
            info = [
                "# Main information\n\n",
                "* **Actual on date:** [{} UTC]\n\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
                "| Parameters                                                  | Values                                                 |\n",
                "|-------------------------------------------------------------|--------------------------------------------------------|\n",
                "| Ticker:                                                     | {:<54} |\n".format(iJSON["ticker"]),
                "| Full name:                                                  | {:<54} |\n".format(iJSON["name"]),
            ]

            if "sector" in iJSON.keys() and iJSON["sector"]:
                info.append("| Sector:                                                     | {:<54} |\n".format(iJSON["sector"]))

            if "countryOfRisk" in iJSON.keys() and iJSON["countryOfRisk"] and "countryOfRiskName" in iJSON.keys() and iJSON["countryOfRiskName"]:
                info.append("| Country of instrument:                                      | {:<54} |\n".format("({}) {}".format(iJSON["countryOfRisk"], iJSON["countryOfRiskName"])))

            info.extend([
                splitLine,
                "| FIGI (Financial Instrument Global Identifier):              | {:<54} |\n".format(iJSON["figi"]),
                "| Real exchange [Exchange section]:                           | {:<54} |\n".format("{} [{}]".format(TKS_REAL_EXCHANGES[iJSON["realExchange"]], iJSON["exchange"])),
            ])

            if "isin" in iJSON.keys() and iJSON["isin"]:
                info.append("| ISIN (International Securities Identification Number):      | {:<54} |\n".format(iJSON["isin"]))

            if "classCode" in iJSON.keys():
                info.append("| Class Code (exchange section where instrument is traded):   | {:<54} |\n".format(iJSON["classCode"]))

            info.extend([
                splitLine,
                "| Current broker security trading status:                     | {:<54} |\n".format(TKS_TRADING_STATUSES[iJSON["tradingStatus"]]),
                splitLine,
                "| Buy operations allowed:                                     | {:<54} |\n".format("Yes" if iJSON["buyAvailableFlag"] else "No"),
                "| Sale operations allowed:                                    | {:<54} |\n".format("Yes" if iJSON["sellAvailableFlag"] else "No"),
                "| Short positions allowed:                                    | {:<54} |\n".format("Yes" if iJSON["shortEnabledFlag"] else "No"),
            ])

            if iJSON["figi"]:
                self._figi = iJSON["figi"]
                iJSON = iJSON | self.RequestTradingStatus()

                info.extend([
                    splitLine,
                    "| Limit orders allowed:                                       | {:<54} |\n".format("Yes" if iJSON["limitOrderAvailableFlag"] else "No"),
                    "| Market orders allowed:                                      | {:<54} |\n".format("Yes" if iJSON["marketOrderAvailableFlag"] else "No"),
                    "| API trade allowed:                                          | {:<54} |\n".format("Yes" if iJSON["apiTradeAvailableFlag"] else "No"),
                ])

            info.append(splitLine)

            if "type" in iJSON.keys() and iJSON["type"]:
                info.append("| Type of the instrument:                                     | {:<54} |\n".format(iJSON["type"]))

                if "shareType" in iJSON.keys() and iJSON["shareType"]:
                    info.append("| Share type:                                                 | {:<54} |\n".format(TKS_SHARE_TYPES[iJSON["shareType"]]))

            if "futuresType" in iJSON.keys() and iJSON["futuresType"]:
                info.append("| Futures type:                                               | {:<54} |\n".format(iJSON["futuresType"]))

            if "ipoDate" in iJSON.keys() and iJSON["ipoDate"]:
                info.append("| IPO date:                                                   | {:<54} |\n".format(iJSON["ipoDate"].replace("T", " ").replace("Z", "")))

            if "releasedDate" in iJSON.keys() and iJSON["releasedDate"]:
                info.append("| Released date:                                              | {:<54} |\n".format(iJSON["releasedDate"].replace("T", " ").replace("Z", "")))

            if "rebalancingFreq" in iJSON.keys() and iJSON["rebalancingFreq"]:
                info.append("| Rebalancing frequency:                                      | {:<54} |\n".format(iJSON["rebalancingFreq"]))

            if "focusType" in iJSON.keys() and iJSON["focusType"]:
                info.append("| Focusing type:                                              | {:<54} |\n".format(iJSON["focusType"]))

            if "assetType" in iJSON.keys() and iJSON["assetType"]:
                info.append("| Asset type:                                                 | {:<54} |\n".format(iJSON["assetType"]))

            if "basicAsset" in iJSON.keys() and iJSON["basicAsset"]:
                info.append("| Basic asset:                                                | {:<54} |\n".format(iJSON["basicAsset"]))

            if "basicAssetSize" in iJSON.keys() and iJSON["basicAssetSize"]:
                info.append("| Basic asset size:                                           | {:<54} |\n".format("{:.2f}".format(NanoToFloat(str(iJSON["basicAssetSize"]["units"]), iJSON["basicAssetSize"]["nano"]))))

            if "isoCurrencyName" in iJSON.keys() and iJSON["isoCurrencyName"]:
                info.append("| ISO currency name:                                          | {:<54} |\n".format(iJSON["isoCurrencyName"]))

            if "currency" in iJSON.keys():
                info.append("| Payment currency:                                           | {:<54} |\n".format(iJSON["currency"]))

            if iJSON["type"] == "Bonds" and "nominal" in iJSON.keys() and "currency" in iJSON["nominal"].keys():
                info.append("| Nominal currency:                                           | {:<54} |\n".format(iJSON["nominal"]["currency"]))

            if "firstTradeDate" in iJSON.keys() and iJSON["firstTradeDate"]:
                info.append("| First trade date:                                           | {:<54} |\n".format(iJSON["firstTradeDate"].replace("T", " ").replace("Z", "")))

            if "lastTradeDate" in iJSON.keys() and iJSON["lastTradeDate"]:
                info.append("| Last trade date:                                            | {:<54} |\n".format(iJSON["lastTradeDate"].replace("T", " ").replace("Z", "")))

            if "expirationDate" in iJSON.keys() and iJSON["expirationDate"]:
                info.append("| Date of expiration:                                         | {:<54} |\n".format(iJSON["expirationDate"].replace("T", " ").replace("Z", "")))

            if "stateRegDate" in iJSON.keys() and iJSON["stateRegDate"]:
                info.append("| State registration date:                                    | {:<54} |\n".format(iJSON["stateRegDate"].replace("T", " ").replace("Z", "")))

            if "placementDate" in iJSON.keys() and iJSON["placementDate"]:
                info.append("| Placement date:                                             | {:<54} |\n".format(iJSON["placementDate"].replace("T", " ").replace("Z", "")))

            if "maturityDate" in iJSON.keys() and iJSON["maturityDate"]:
                info.append("| Maturity date:                                              | {:<54} |\n".format(iJSON["maturityDate"].replace("T", " ").replace("Z", "")))

            if "perpetualFlag" in iJSON.keys() and iJSON["perpetualFlag"]:
                info.append("| Perpetual bond:                                             | Yes                                                    |\n")

            if "otcFlag" in iJSON.keys() and iJSON["otcFlag"]:
                info.append("| Over-the-counter (OTC) securities:                          | Yes                                                    |\n")

            iExt = None
            if iJSON["type"] == "Bonds":
                info.extend([
                    splitLine,
                    "| Bond issue (size / plan):                                   | {:<54} |\n".format("{} / {}".format(iJSON["issueSize"], iJSON["issueSizePlan"])),
                    "| Nominal price (100%):                                       | {:<54} |\n".format("{} {}".format(
                        "{:.2f}".format(NanoToFloat(str(iJSON["nominal"]["units"]), iJSON["nominal"]["nano"])).rstrip("0").rstrip("."),
                        iJSON["nominal"]["currency"],
                    )),
                ])

                if "floatingCouponFlag" in iJSON.keys():
                    info.append("| Floating coupon:                                            | {:<54} |\n".format("Yes" if iJSON["floatingCouponFlag"] else "No"))

                if "amortizationFlag" in iJSON.keys():
                    info.append("| Amortization:                                               | {:<54} |\n".format("Yes" if iJSON["amortizationFlag"] else "No"))

                info.append(splitLine)

                if "couponQuantityPerYear" in iJSON.keys() and iJSON["couponQuantityPerYear"]:
                    info.append("| Number of coupon payments per year:                         | {:<54} |\n".format(iJSON["couponQuantityPerYear"]))

                if iJSON["figi"]:
                    iExt = self.ExtendBondsData(instruments=iJSON["figi"], xlsx=False)  # extended bonds data

                    info.extend([
                        "| Days last to maturity date:                                 | {:<54} |\n".format(iExt["daysToMaturity"][0]),
                        "| Coupons yield (average coupon daily yield * 365):           | {:<54} |\n".format("{:.2f}%".format(iExt["couponsYield"][0])),
                        "| Current price yield (average daily yield * 365):            | {:<54} |\n".format("{:.2f}%".format(iExt["currentYield"][0])),
                    ])

                if "aciValue" in iJSON.keys() and iJSON["aciValue"]:
                    info.append("| Current accumulated coupon income (ACI):                    | {:<54} |\n".format("{:.2f} {}".format(
                        NanoToFloat(str(iJSON["aciValue"]["units"]), iJSON["aciValue"]["nano"]),
                        iJSON["aciValue"]["currency"]
                    )))

            if "currentPrice" in iJSON.keys():
                info.append(splitLine)

                currency = iJSON["currency"] if "currency" in iJSON.keys() else ""  # nominal currency for bonds, otherwise currency of instrument
                aciCurrency = iExt["aciCurrency"][0] if iJSON["type"] == "Bonds" and iExt is not None and "aciCurrency" in iExt.keys() else ""  # payment currency

                bondPrevClose = iExt["closePrice"][0] if iJSON["type"] == "Bonds" and iExt is not None and "closePrice" in iExt.keys() else 0  # previous close price of bond
                bondLastPrice = iExt["lastPrice"][0] if iJSON["type"] == "Bonds" and iExt is not None and "lastPrice" in iExt.keys() else 0  # last price of bond
                bondLimitUp = iExt["limitUp"][0] if iJSON["type"] == "Bonds" and iExt is not None and "limitUp" in iExt.keys() else 0  # max price of bond
                bondLimitDown = iExt["limitDown"][0] if iJSON["type"] == "Bonds" and iExt is not None and "limitDown" in iExt.keys() else 0  # min price of bond
                bondChangesDelta = iExt["changesDelta"][0] if iJSON["type"] == "Bonds" and iExt is not None and "changesDelta" in iExt.keys() else 0  # delta between last deal price and last close

                curPriceSell = iJSON["currentPrice"]["sell"][0]["price"] if iJSON["currentPrice"]["sell"] else 0
                curPriceBuy = iJSON["currentPrice"]["buy"][0]["price"] if iJSON["currentPrice"]["buy"] else 0

                info.extend([
                    "| Previous close price of the instrument:                     | {:<54} |\n".format("{}{}".format(
                        "{}".format(iJSON["currentPrice"]["closePrice"]).rstrip("0").rstrip(".") if iJSON["currentPrice"]["closePrice"] is not None else "N/A",
                        "% of nominal price ({:.2f} {})".format(bondPrevClose, aciCurrency) if iJSON["type"] == "Bonds" else " {}".format(currency),
                    )),
                    "| Last deal price of the instrument:                          | {:<54} |\n".format("{}{}".format(
                        "{}".format(iJSON["currentPrice"]["lastPrice"]).rstrip("0").rstrip(".") if iJSON["currentPrice"]["lastPrice"] is not None else "N/A",
                        "% of nominal price ({:.2f} {})".format(bondLastPrice, aciCurrency) if iJSON["type"] == "Bonds" else " {}".format(currency),
                    )),
                    "| Changes between last deal price and last close              | {:<54} |\n".format(
                        "{:.2f}%{}".format(
                            iJSON["currentPrice"]["changes"],
                            " ({}{:.2f} {})".format(
                                "+" if bondChangesDelta > 0 else "",
                                bondChangesDelta,
                                aciCurrency
                            ) if iJSON["type"] == "Bonds" else " ({}{:.2f} {})".format(
                                "+" if iJSON["currentPrice"]["lastPrice"] > iJSON["currentPrice"]["closePrice"] else "",
                                iJSON["currentPrice"]["lastPrice"] - iJSON["currentPrice"]["closePrice"],
                                currency
                            ),
                        )
                    ),
                    "| Current limit price, min / max:                             | {:<54} |\n".format("{}{} / {}{}{}".format(
                        "{}".format(iJSON["currentPrice"]["limitDown"]).rstrip("0").rstrip(".") if iJSON["currentPrice"]["limitDown"] is not None else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(currency),
                        "{}".format(iJSON["currentPrice"]["limitUp"]).rstrip("0").rstrip(".") if iJSON["currentPrice"]["limitUp"] is not None else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(currency),
                        " ({:.2f} {} / {:.2f} {})".format(bondLimitDown, aciCurrency, bondLimitUp, aciCurrency) if iJSON["type"] == "Bonds" else ""
                    )),
                    "| Actual price, sell / buy:                                   | {:<54} |\n".format("{}{} / {}{}{}".format(
                        "{}".format(curPriceSell).rstrip("0").rstrip(".") if curPriceSell != 0 else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(currency),
                        "{}".format(curPriceBuy).rstrip("0").rstrip(".") if curPriceBuy != 0 else "N/A",
                        "%" if iJSON["type"] == "Bonds" else" {}".format(currency),
                        " ({:.2f} {} / {:.2f} {})".format(curPriceSell, aciCurrency, curPriceBuy, aciCurrency) if iJSON["type"] == "Bonds" else ""
                    )),
                ])

            if "lot" in iJSON.keys():
                info.append("| Minimum lot to buy:                                         | {:<54} |\n".format(iJSON["lot"]))

            if "step" in iJSON.keys() and iJSON["step"] != 0:
                info.append("| Minimum price increment (step):                             | {:<54} |\n".format("{} {}".format(iJSON["step"], iJSON["currency"] if "currency" in iJSON.keys() else "")))

            # Add bond payment calendar:
            if iJSON["type"] == "Bonds":
                strCalendar = self.ShowBondsCalendar(extBonds=iExt, show=False)   # bond payment calendar
                info.extend(["\n#", strCalendar])

            infoText += "".join(info)

            if show and not onlyFiles:
                uLogger.info("{}".format(infoText))

            if self.infoFile is not None and (show or onlyFiles):
                with open(self.infoFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Info about instrument with ticker [{}] and FIGI [{}] was saved to file: [{}]".format(iJSON["ticker"], iJSON["figi"], os.path.abspath(self.infoFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.infoFile.replace(".md", ".html") if self.infoFile.endswith(".md") else self.infoFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Main information", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return infoText

    def SearchByTicker(self, requestPrice: bool = False, show: bool = False) -> dict:
        """
        Search and return raw broker's information about instrument by its ticker. Variable `ticker` must be defined!

        :param requestPrice: if `False` then do not request current price of instrument (because this is long operation).
        :param show: if `False` then do not run `ShowInstrumentInfo()` method and do not print info to the console.
        :return: JSON formatted data with information about instrument.
        """
        tickerJSON = {}
        if self.moreDebug:
            uLogger.debug("Searching information about instrument by it's ticker [{}] ...".format(self._ticker))

        if not self._ticker:
            uLogger.warning("self._ticker variable is not be empty!")

        else:
            if self._ticker in TKS_TICKERS_OR_FIGI_EXCLUDED:
                uLogger.warning("Instrument with ticker [{}] not allowed for trading!".format(self._ticker))
                raise Exception("Instrument not allowed")

            if not self.iList:
                self.iList = self.Listing()

            if self._ticker in self.iList["Shares"].keys():
                tickerJSON = self.iList["Shares"][self._ticker]
                if self.moreDebug:
                    uLogger.debug("Ticker [{}] found in shares list".format(self._ticker))

            elif self._ticker in self.iList["Currencies"].keys():
                tickerJSON = self.iList["Currencies"][self._ticker]
                if self.moreDebug:
                    uLogger.debug("Ticker [{}] found in currencies list".format(self._ticker))

            elif self._ticker in self.iList["Bonds"].keys():
                tickerJSON = self.iList["Bonds"][self._ticker]
                if self.moreDebug:
                    uLogger.debug("Ticker [{}] found in bonds list".format(self._ticker))

            elif self._ticker in self.iList["Etfs"].keys():
                tickerJSON = self.iList["Etfs"][self._ticker]
                if self.moreDebug:
                    uLogger.debug("Ticker [{}] found in etfs list".format(self._ticker))

            elif self._ticker in self.iList["Futures"].keys():
                tickerJSON = self.iList["Futures"][self._ticker]
                if self.moreDebug:
                    uLogger.debug("Ticker [{}] found in futures list".format(self._ticker))

        if tickerJSON:
            self._figi = tickerJSON["figi"]

            if requestPrice:
                tickerJSON["currentPrice"] = self.GetCurrentPrices(show=False)

                if tickerJSON["currentPrice"]["closePrice"] is not None and tickerJSON["currentPrice"]["closePrice"] != 0 and tickerJSON["currentPrice"]["lastPrice"] is not None:
                    tickerJSON["currentPrice"]["changes"] = 100 * (tickerJSON["currentPrice"]["lastPrice"] - tickerJSON["currentPrice"]["closePrice"]) / tickerJSON["currentPrice"]["closePrice"]

                else:
                    tickerJSON["currentPrice"]["changes"] = 0

            if show:
                self.ShowInstrumentInfo(iJSON=tickerJSON, show=True)  # print info as Markdown text

        else:
            if show:
                uLogger.warning("Ticker [{}] not found in available broker instrument's list!".format(self._ticker))

        return tickerJSON

    def SearchByFIGI(self, requestPrice: bool = False, show: bool = False) -> dict:
        """
        Search and return raw broker's information about instrument by its FIGI. Variable `figi` must be defined!

        :param requestPrice: if `False` then do not request current price of instrument (it's long operation).
        :param show: if `False` then do not run `ShowInstrumentInfo()` method and do not print info to the console.
        :return: JSON formatted data with information about instrument.
        """
        figiJSON = {}
        if self.moreDebug:
            uLogger.debug("Searching information about instrument by it's FIGI [{}] ...".format(self._figi))

        if not self._figi:
            uLogger.warning("self._figi variable is not be empty!")

        else:
            if self._figi in TKS_TICKERS_OR_FIGI_EXCLUDED:
                uLogger.warning("Instrument with figi [{}] not allowed for trading!".format(self._figi))
                raise Exception("Instrument not allowed")

            if not self.iList:
                self.iList = self.Listing()

            for item in self.iList["Shares"].keys():
                if self._figi == self.iList["Shares"][item]["figi"]:
                    figiJSON = self.iList["Shares"][item]

                    if self.moreDebug:
                        uLogger.debug("FIGI [{}] found in shares list".format(self._figi))

                    break

            if not figiJSON:
                for item in self.iList["Currencies"].keys():
                    if self._figi == self.iList["Currencies"][item]["figi"]:
                        figiJSON = self.iList["Currencies"][item]

                        if self.moreDebug:
                            uLogger.debug("FIGI [{}] found in currencies list".format(self._figi))

                        break

            if not figiJSON:
                for item in self.iList["Bonds"].keys():
                    if self._figi == self.iList["Bonds"][item]["figi"]:
                        figiJSON = self.iList["Bonds"][item]

                        if self.moreDebug:
                            uLogger.debug("FIGI [{}] found in bonds list".format(self._figi))

                        break

            if not figiJSON:
                for item in self.iList["Etfs"].keys():
                    if self._figi == self.iList["Etfs"][item]["figi"]:
                        figiJSON = self.iList["Etfs"][item]

                        if self.moreDebug:
                            uLogger.debug("FIGI [{}] found in etfs list".format(self._figi))

                        break

            if not figiJSON:
                for item in self.iList["Futures"].keys():
                    if self._figi == self.iList["Futures"][item]["figi"]:
                        figiJSON = self.iList["Futures"][item]

                        if self.moreDebug:
                            uLogger.debug("FIGI [{}] found in futures list".format(self._figi))

                        break

        if figiJSON:
            self._figi = figiJSON["figi"]
            self._ticker = figiJSON["ticker"]

            if requestPrice:
                figiJSON["currentPrice"] = self.GetCurrentPrices(show=False)

                if figiJSON["currentPrice"]["closePrice"] is not None and figiJSON["currentPrice"]["closePrice"] != 0 and figiJSON["currentPrice"]["lastPrice"] is not None:
                    figiJSON["currentPrice"]["changes"] = 100 * (figiJSON["currentPrice"]["lastPrice"] - figiJSON["currentPrice"]["closePrice"]) / figiJSON["currentPrice"]["closePrice"]

                else:
                    figiJSON["currentPrice"]["changes"] = 0

            if show:
                self.ShowInstrumentInfo(iJSON=figiJSON, show=True)  # print info as Markdown text

        else:
            if show:
                uLogger.warning("FIGI [{}] not found in available broker instrument's list!".format(self._figi))

        return figiJSON

    def GetCurrentPrices(self, show: bool = True) -> dict:
        """
        Get and show Depth of Market with current prices of the instrument as dictionary. Result example with `depth` 5:
        `{"buy": [{"price": 1243.8, "quantity": 193},
                  {"price": 1244.0, "quantity": 168},
                  {"price": 1244.8, "quantity": 5},
                  {"price": 1245.0, "quantity": 61},
                  {"price": 1245.4, "quantity": 60}],
          "sell": [{"price": 1243.6, "quantity": 8},
                   {"price": 1242.6, "quantity": 10},
                   {"price": 1242.4, "quantity": 18},
                   {"price": 1242.2, "quantity": 50},
                   {"price": 1242.0, "quantity": 113}],
          "limitUp": 1619.0, "limitDown": 903.4, "lastPrice": 1243.8, "closePrice": 1263.0}`, where parameters mean:
        - buy: list of dicts with Sellers prices, see also: https://tinkoff.github.io/investAPI/marketdata/#order
        - sell: list of dicts with Buyers prices,
            - price: price of 1 instrument (to get the cost of the lot, you need to multiply it by the lot of size of the instrument),
            - quantity: volume value by current price in lots,
        - limitUp: current trade session limit price, maximum,
        - limitDown: current trade session limit price, minimum,
        - lastPrice: last deal price of the instrument,
        - closePrice: previous trade session close price of the instrument.

        See also: `SearchByTicker()` and `SearchByFIGI()`.
        REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetOrderBook
        Response fields: https://tinkoff.github.io/investAPI/marketdata/#getorderbookresponse

        :param show: if `True` then print DOM to log and console.
        :return: orders book dict with lists of current buy and sell prices: `{"buy": [{"price": x1, "quantity": y1, ...}], "sell": [....]}`.
                 If an error occurred then returns an empty record:
                 `{"buy": [], "sell": [], "limitUp": None, "limitDown": None, "lastPrice": None, "closePrice": None}`.
        """
        prices = {"buy": [], "sell": [], "limitUp": 0, "limitDown": 0, "lastPrice": 0, "closePrice": 0}

        if self.depth < 1:
            uLogger.error("Depth of Market (DOM) must be >=1!")
            raise Exception("Incorrect value")

        if not (self._ticker or self._figi):
            uLogger.error("self._ticker or self._figi variables must be defined!")
            raise Exception("Ticker or FIGI required")

        if self._ticker and not self._figi:
            instrumentByTicker = self.SearchByTicker(requestPrice=False)  # WARNING! requestPrice=False to avoid recursion!
            self._figi = instrumentByTicker["figi"] if instrumentByTicker else ""

        if not self._ticker and self._figi:
            instrumentByFigi = self.SearchByFIGI(requestPrice=False)  # WARNING! requestPrice=False to avoid recursion!
            self._ticker = instrumentByFigi["ticker"] if instrumentByFigi else ""

        if not self._figi:
            uLogger.error("FIGI is not defined!")
            raise Exception("Ticker or FIGI required")

        else:
            uLogger.debug("Requesting current prices: ticker [{}], FIGI [{}]. Wait, please...".format(self._ticker, self._figi))

            # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetOrderBook
            priceURL = self.server + r"/tinkoff.public.invest.api.contract.v1.MarketDataService/GetOrderBook"
            self.body = str({"figi": self._figi, "depth": self.depth})
            pricesResponse = self.SendAPIRequest(priceURL, reqType="POST")  # Response fields: https://tinkoff.github.io/investAPI/marketdata/#getorderbookresponse

            if pricesResponse and not ("code" in pricesResponse.keys() or "message" in pricesResponse.keys() or "description" in pricesResponse.keys()):
                # list of dicts with sellers orders:
                prices["buy"] = [{"price": round(NanoToFloat(item["price"]["units"], item["price"]["nano"]), 6), "quantity": int(item["quantity"])} for item in pricesResponse["asks"]]

                # list of dicts with buyers orders:
                prices["sell"] = [{"price": round(NanoToFloat(item["price"]["units"], item["price"]["nano"]), 6), "quantity": int(item["quantity"])} for item in pricesResponse["bids"]]

                # max price of instrument at this time:
                prices["limitUp"] = round(NanoToFloat(pricesResponse["limitUp"]["units"], pricesResponse["limitUp"]["nano"]), 6) if "limitUp" in pricesResponse.keys() else None

                # min price of instrument at this time:
                prices["limitDown"] = round(NanoToFloat(pricesResponse["limitDown"]["units"], pricesResponse["limitDown"]["nano"]), 6) if "limitDown" in pricesResponse.keys() else None

                # last price of deal with instrument:
                prices["lastPrice"] = round(NanoToFloat(pricesResponse["lastPrice"]["units"], pricesResponse["lastPrice"]["nano"]), 6) if "lastPrice" in pricesResponse.keys() else 0

                # last close price of instrument:
                prices["closePrice"] = round(NanoToFloat(pricesResponse["closePrice"]["units"], pricesResponse["closePrice"]["nano"]), 6) if "closePrice" in pricesResponse.keys() else 0

            else:
                uLogger.warning("Server return an empty or error response! See full log. Instrument: ticker [{}], FIGI [{}]".format(self._ticker, self._figi))
                uLogger.debug("Server response: {}".format(pricesResponse))

            if show:
                if prices["buy"] or prices["sell"]:
                    info = [
                        "Orders book actual at [{}] (UTC)\nTicker: [{}], FIGI: [{}], Depth of Market: [{}]\n".format(
                            datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT),
                            self._ticker,
                            self._figi,
                            self.depth,
                        ),
                        "-" * 60, "\n",
                        "             Orders of Buyers | Orders of Sellers\n",
                        "-" * 60, "\n",
                        "        Sell prices (volumes) | Buy prices (volumes)\n",
                        "-" * 60, "\n",
                    ]

                    if not prices["buy"]:
                        info.append("                              | No orders!\n")
                        sumBuy = 0

                    else:
                        sumBuy = sum([x["quantity"] for x in prices["buy"]])
                        maxMinSorted = sorted(prices["buy"], key=lambda k: k["price"], reverse=True)
                        for item in maxMinSorted:
                            info.append("                              | {} ({})\n".format(item["price"], item["quantity"]))

                    if not prices["sell"]:
                        info.append("No orders!                    |\n")
                        sumSell = 0

                    else:
                        sumSell = sum([x["quantity"] for x in prices["sell"]])
                        for item in prices["sell"]:
                            info.append("{:>29} |\n".format("{} ({})".format(item["price"], item["quantity"])))

                    info.extend([
                        "-" * 60, "\n",
                        "{:>29} | {}\n".format("Total sell: {}".format(sumSell), "Total buy: {}".format(sumBuy)),
                        "-" * 60, "\n",
                    ])

                    infoText = "".join(info)

                    uLogger.info("Current prices in order book:\n\n{}".format(infoText))

                else:
                    uLogger.warning("Orders book is empty at this time! Instrument: ticker [{}], FIGI [{}]".format(self._ticker, self._figi))

        return prices

    def ShowInstrumentsInfo(self, show: bool = True, onlyFiles=False) -> str:
        """
        This method get and show information about all available broker instruments for current user account.
        If `instrumentsFile` string is not empty then also save information to this file.

        :param show: if `True` then print results to console, if `False` — print only to file.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: multi-lines string with all available broker instruments.
        """
        if not self.iList:
            self.iList = self.Listing()

        info = [
            "# All available instruments from Tinkoff Broker server for current user token\n\n",
            "* **Actual on date:** [{} UTC]\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
        ]

        # add instruments count by type:
        for iType in self.iList.keys():
            info.append("* **{}:** [{}]\n".format(iType, len(self.iList[iType])))

        headerLine = "| Ticker       | Full name                                                 | FIGI         | Cur | Lot     | Step       |\n"
        splitLine = "|--------------|-----------------------------------------------------------|--------------|-----|---------|------------|\n"

        # generating info tables with all instruments by type:
        for iType in self.iList.keys():
            info.extend(["\n\n## {} available. Total: [{}]\n\n".format(iType, len(self.iList[iType])), headerLine, splitLine])

            for instrument in self.iList[iType].keys():
                iName = self.iList[iType][instrument]["name"]  # instrument's name
                if len(iName) > 57:
                    iName = "{}...".format(iName[:54])  # right trim for a long string

                info.append("| {:<12} | {:<57} | {:<12} | {:<3} | {:<7} | {:<10} |\n".format(
                    self.iList[iType][instrument]["ticker"],
                    iName,
                    self.iList[iType][instrument]["figi"],
                    self.iList[iType][instrument]["currency"],
                    self.iList[iType][instrument]["lot"],
                    "{:.10f}".format(self.iList[iType][instrument]["step"]).rstrip("0").rstrip(".") if self.iList[iType][instrument]["step"] > 0 else 0,
                ))

        infoText = "".join(info)

        if show and not onlyFiles:
            uLogger.info(infoText)

        if self.instrumentsFile and (show or onlyFiles):
            with open(self.instrumentsFile, "w", encoding="UTF-8") as fH:
                fH.write(infoText)

            uLogger.info("All available instruments are saved to file: [{}]".format(os.path.abspath(self.instrumentsFile)))

            if self.useHTMLReports:
                htmlFilePath = self.instrumentsFile.replace(".md", ".html") if self.instrumentsFile.endswith(".md") else self.instrumentsFile + ".html"
                with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                    fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="List of instruments", commonCSS=COMMON_CSS, markdown=infoText))

                uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return infoText

    def SearchInstruments(self, pattern: str, show: bool = True, onlyFiles=False) -> dict:
        """
        This method search and show information about instruments by part of its ticker, FIGI or name.
        If `searchResultsFile` string is not empty then also save information to this file.

        :param pattern: string with part of ticker, FIGI or instrument's name.
        :param show: if `True` then print results to console, if `False` — return list of result only.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: list of dictionaries with all found instruments.
        """
        if not self.iList:
            self.iList = self.Listing()

        searchResults = {iType: {} for iType in self.iList}  # same as iList but will contain only filtered instruments
        compiledPattern = re.compile(pattern, re.IGNORECASE)

        for iType in self.iList:
            for instrument in self.iList[iType].values():
                searchResult = compiledPattern.search(" ".join(
                    [instrument["ticker"], instrument["figi"], instrument["name"]]
                ))

                if searchResult:
                    searchResults[iType][instrument["ticker"]] = instrument

        resultsLen = sum([len(searchResults[iType]) for iType in searchResults])
        info = [
            "# Search results\n\n",
            "* **Actual on date:** [{} UTC]\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
            "* **Search pattern:** [{}]\n".format(pattern),
            "* **Found instruments:** [{}]\n\n".format(resultsLen),
            '**Note:** you can view info about found instruments with key "--info", e.g.: "tksbrokerapi -t TICKER --info" or "tksbrokerapi -f FIGI --info".\n'
        ]
        infoShort = info[:]

        headerLine = "| Type       | Ticker       | Full name                                                      | FIGI         |\n"
        splitLine = "|------------|--------------|----------------------------------------------------------------|--------------|\n"
        skippedLine = "| ...        | ...          | ...                                                            | ...          |\n"

        if resultsLen == 0:
            info.append("\nNo results\n")
            infoShort.append("\nNo results\n")
            uLogger.warning("No results. Try changing your search pattern.")

        else:
            for iType in searchResults:
                iTypeValuesCount = len(searchResults[iType].values())
                if iTypeValuesCount > 0:
                    info.extend(["\n## {}: [{}]\n\n".format(iType, iTypeValuesCount), headerLine, splitLine])
                    infoShort.extend(["\n### {}: [{}]\n\n".format(iType, iTypeValuesCount), headerLine, splitLine])

                    for instrument in searchResults[iType].values():
                        info.append("| {:<10} | {:<12} | {:<63}| {:<13}|\n".format(
                            instrument["type"],
                            instrument["ticker"],
                            "{}...".format(instrument["name"][:60]) if len(instrument["name"]) > 63 else instrument["name"],  # right trim for a long string
                            instrument["figi"],
                        ))

                    if iTypeValuesCount <= 5:
                        infoShort.extend(info[-iTypeValuesCount:])

                    else:
                        infoShort.extend(info[-5:])
                        infoShort.append(skippedLine)

        infoText = "".join(info)
        infoTextShort = "".join(infoShort)

        if show and not onlyFiles:
            uLogger.info(infoTextShort)
            uLogger.info("You can view info about found instruments with key `--info`, e.g.: `tksbrokerapi -t IBM --info` or `tksbrokerapi -f BBG000BLNNH6 --info`")

        if self.searchResultsFile and (show or onlyFiles):
            with open(self.searchResultsFile, "w", encoding="UTF-8") as fH:
                fH.write(infoText)

            uLogger.info("Full search results were saved to file: [{}]".format(os.path.abspath(self.searchResultsFile)))

            if self.useHTMLReports:
                htmlFilePath = self.searchResultsFile.replace(".md", ".html") if self.searchResultsFile.endswith(".md") else self.searchResultsFile + ".html"
                with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                    fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Search results", commonCSS=COMMON_CSS, markdown=infoText))

                uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return searchResults

    def GetUniqueFIGIs(self, instruments: list[str]) -> list:
        """
        Creating list with unique instrument FIGIs from input list of tickers (priority) or FIGIs.

        :param instruments: list of strings with tickers or FIGIs.
        :return: list with unique instrument FIGIs only.
        """
        requestedInstruments = []
        for iName in instruments:
            if iName not in self.aliases.keys():
                if iName not in requestedInstruments:
                    requestedInstruments.append(iName)

            else:
                if iName not in requestedInstruments:
                    if self.aliases[iName] not in requestedInstruments:
                        requestedInstruments.append(self.aliases[iName])

        uLogger.debug("Requested instruments without duplicates of tickers or FIGIs: {}".format(requestedInstruments))

        onlyUniqueFIGIs = []
        for iName in requestedInstruments:
            if iName in TKS_TICKERS_OR_FIGI_EXCLUDED:
                continue

            self._ticker = iName
            iData = self.SearchByTicker(requestPrice=False)  # trying to find instrument by ticker

            if not iData:
                self._ticker = ""
                self._figi = iName

                iData = self.SearchByFIGI(requestPrice=False)  # trying to find instrument by FIGI

                if not iData:
                    self._figi = ""
                    uLogger.warning("Instrument [{}] not in list of available instruments for current token!".format(iName))

            if iData and iData["figi"] not in onlyUniqueFIGIs:
                onlyUniqueFIGIs.append(iData["figi"])

        uLogger.debug("Unique list of FIGIs: {}".format(onlyUniqueFIGIs))

        return onlyUniqueFIGIs

    def GetListOfPrices(self, instruments: list[str], show: bool = False, onlyFiles=False) -> list[dict]:
        """
        This method get, maybe show and return prices of list of instruments. WARNING! This is potential long operation!

        See limits: https://tinkoff.github.io/investAPI/limits/

        If `pricesFile` string is not empty then also save information to this file.

        :param instruments: list of strings with tickers or FIGIs.
        :param show: if `True` then prints prices to console, if `False` — prints only to file `pricesFile`.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: list of instruments looks like `[{some ticker info, "currentPrice": {current prices}}, {...}, ...]`.
                 One item is dict returned by `SearchByTicker()` or `SearchByFIGI()` methods.
        """
        if instruments is None or not instruments:
            uLogger.error("You must define some of tickers or FIGIs to request it's actual prices!")
            raise Exception("Ticker or FIGI required")

        onlyUniqueFIGIs = self.GetUniqueFIGIs(instruments)

        uLogger.debug("Requesting current prices from Tinkoff Broker server...")

        iList = []  # trying to get info and current prices about all unique instruments:
        for self._figi in onlyUniqueFIGIs:
            iData = self.SearchByFIGI(requestPrice=True, show=False)
            iList.append(iData)

        self.ShowListOfPrices(iList, show, onlyFiles)

        return iList

    def ShowListOfPrices(self, iList: list, show: bool = True, onlyFiles=False) -> str:
        """
        Show table contains current prices of given instruments.

        :param iList: list of instruments looks like `[{some ticker info, "currentPrice": {current prices}}, {...}, ...]`.
                      One item is dict returned by `SearchByTicker(requestPrice=True)` or by `SearchByFIGI(requestPrice=True)` methods.
        :param show: if `True` then prints prices to console, if `False` — prints only to file `pricesFile`.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: multilines text in Markdown format as a table contains current prices.
        """
        infoText = ""

        if show or self.pricesFile or onlyFiles:
            info = [
                "# Current prices\n\n* **Actual on date:** [{} UTC]\n\n".format(datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M")),
                "| Ticker       | FIGI         | Type       | Prev. close | Last price  | Chg. %   | Day limits min/max  | Actual sell / buy   | Curr. |\n",
                "|--------------|--------------|------------|-------------|-------------|----------|---------------------|---------------------|-------|\n",
            ]

            for item in iList:
                info.append("| {:<12} | {:<12} | {:<10} | {:>11} | {:>11} | {:>7}% | {:>19} | {:>19} | {:<5} |\n".format(
                    item["ticker"],
                    item["figi"],
                    item["type"],
                    "{:.2f}".format(float(item["currentPrice"]["closePrice"])),
                    "{:.2f}".format(float(item["currentPrice"]["lastPrice"])),
                    "{}{:.2f}".format("+" if item["currentPrice"]["changes"] > 0 else "", float(item["currentPrice"]["changes"])),
                    "{} / {}".format(
                        item["currentPrice"]["limitDown"] if item["currentPrice"]["limitDown"] is not None else "N/A",
                        item["currentPrice"]["limitUp"] if item["currentPrice"]["limitUp"] is not None else "N/A",
                    ),
                    "{} / {}".format(
                        item["currentPrice"]["sell"][0]["price"] if item["currentPrice"]["sell"] else "N/A",
                        item["currentPrice"]["buy"][0]["price"] if item["currentPrice"]["buy"] else "N/A",
                    ),
                    item["currency"],
                ))

            infoText = "".join(info)

            if show and not onlyFiles:
                uLogger.info("Only instruments with unique FIGIs are shown:\n{}".format(infoText))

            if self.pricesFile and (show or onlyFiles):
                with open(self.pricesFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Price list for all instruments saved to file: [{}]".format(os.path.abspath(self.pricesFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.pricesFile.replace(".md", ".html") if self.pricesFile.endswith(".md") else self.pricesFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Current prices", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return infoText

    def RequestTradingStatus(self) -> dict:
        """
        Requesting trading status for the instrument defined by `figi` variable.

        REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetTradingStatus

        Documentation: https://tinkoff.github.io/investAPI/marketdata/#gettradingstatusrequest

        :return: dictionary with trading status attributes. Response example:
                 `{"figi": "TCS00A103X66", "tradingStatus": "SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING",
                  "limitOrderAvailableFlag": false, "marketOrderAvailableFlag": false, "apiTradeAvailableFlag": true}`
        """
        if self._figi is None or not self._figi:
            uLogger.error("Variable `figi` must be defined for using this method!")
            raise Exception("FIGI required")

        uLogger.debug("Requesting current trading status, FIGI: [{}]. Wait, please...".format(self._figi))

        self.body = str({"figi": self._figi, "instrumentId": self._figi})
        tradingStatusURL = self.server + r"/tinkoff.public.invest.api.contract.v1.MarketDataService/GetTradingStatus"
        tradingStatus = self.SendAPIRequest(tradingStatusURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about current trading status successfully received")

        return tradingStatus

    def RequestPortfolio(self) -> dict:
        """
        Requesting actual user's portfolio for current `accountId`.

        REST API for user portfolio: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetPortfolio

        Documentation: https://tinkoff.github.io/investAPI/operations/#portfoliorequest

        :return: dictionary with user's portfolio.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        uLogger.debug("Requesting current actual user's portfolio. Wait, please...")

        self.body = str({"accountId": self.accountId})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio"
        rawPortfolio = self.SendAPIRequest(portfolioURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about user's portfolio successfully received")

        return rawPortfolio

    def RequestPositions(self) -> dict:
        """
        Requesting open positions by currencies and instruments for current `accountId`.

        REST API for open positions: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetPositions

        Documentation: https://tinkoff.github.io/investAPI/operations/#positionsrequest

        :return: dictionary with open positions by instruments.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        uLogger.debug("Requesting current open positions in currencies and instruments. Wait, please...")

        self.body = str({"accountId": self.accountId})
        positionsURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetPositions"
        rawPositions = self.SendAPIRequest(positionsURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about current open positions successfully received")

        return rawPositions

    def RequestPendingOrders(self) -> list:
        """
        Requesting current actual pending limit orders for current `accountId`.

        REST API for pending (market) orders: https://tinkoff.github.io/investAPI/swagger-ui/#/OrdersService/OrdersService_GetOrders

        Documentation: https://tinkoff.github.io/investAPI/orders/#getordersrequest

        :return: list of dictionaries with pending limit orders.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        uLogger.debug("Requesting current actual pending limit orders. Wait, please...")

        self.body = str({"accountId": self.accountId})
        ordersURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/GetOrders"
        rawResponse = self.SendAPIRequest(ordersURL, reqType="POST")

        if "orders" in rawResponse.keys():
            rawOrders = rawResponse["orders"]
            uLogger.debug("[{}] records about pending limit orders received".format(len(rawOrders)))

        else:
            rawOrders = []
            uLogger.debug("No pending limit orders returned! rawResponse = {}".format(rawResponse))

        return rawOrders

    def RequestStopOrders(self) -> list:
        """
        Requesting current actual stop orders for current `accountId`.

        REST API for opened stop-orders: https://tinkoff.github.io/investAPI/swagger-ui/#/StopOrdersService/StopOrdersService_GetStopOrders

        Documentation: https://tinkoff.github.io/investAPI/stoporders/#getstopordersrequest

        :return: list of dictionaries with stop orders.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        uLogger.debug("Requesting current actual stop orders. Wait, please...")

        self.body = str({"accountId": self.accountId})
        stopOrdersURL = self.server + r"/tinkoff.public.invest.api.contract.v1.StopOrdersService/GetStopOrders"
        rawResponse = self.SendAPIRequest(stopOrdersURL, reqType="POST")

        if "stopOrders" in rawResponse.keys():
            rawStopOrders = rawResponse["stopOrders"]
            uLogger.debug("[{}] records about stop orders received".format(len(rawStopOrders)))

        else:
            rawStopOrders = []
            uLogger.debug("No stop orders returned! rawResponse = {}".format(rawResponse))

        return rawStopOrders

    # noinspection PyTypeChecker
    def Overview(self, show: bool = False, details: str = "full", onlyFiles=False) -> dict:
        """
        Get portfolio: all open positions, orders and some statistics for current `accountId`.
        If `overviewFile`, `overviewDigestFile`, `overviewPositionsFile`, `overviewOrdersFile`, `overviewAnalyticsFile`
        and `overviewBondsCalendarFile` are defined then also save information to file.

        WARNING! It is not recommended to run this method too many times in a loop! The server receives
        many requests about the state of the portfolio, and then, based on the received data, a large number
        of calculation and statistics are collected.

        :param show: if `False` then only dictionary returns, if `True` then show more debug information.
        :param details: how detailed should the information be?
        - `full` — shows full available information about portfolio status (by default),
        - `positions` — shows only open positions,
        - `orders` — shows only sections of open limits and stop orders.
        - `digest` — show a short digest of the portfolio status,
        - `analytics` — shows only the analytics section and the distribution of the portfolio by various categories,
        - `calendar` — shows only the bonds calendar section (if these present in portfolio).
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: dictionary with client's raw portfolio and some statistics.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        view = {
            "raw": {  # --- raw portfolio responses from broker with user portfolio data:
                "headers": {},  # list of dictionaries, response headers without "positions" section
                "Currencies": [],  # list of dictionaries, open trades with currencies from "positions" section
                "Shares": [],  # list of dictionaries, open trades with shares from "positions" section
                "Bonds": [],  # list of dictionaries, open trades with bonds from "positions" section
                "Etfs": [],  # list of dictionaries, open trades with etfs from "positions" section
                "Futures": [],  # list of dictionaries, open trades with futures from "positions" section
                "positions": {},  # raw response from broker: dictionary with current available or blocked currencies and instruments for client
                "orders": [],  # raw response from broker: list of dictionaries with all pending (market) orders
                "stopOrders": [],  # raw response from broker: list of dictionaries with all stop orders
                "currenciesCurrentPrices": {"rub": {"name": "Российский рубль", "currentPrice": 1.}},  # dict with prices of all currencies in RUB
            },
            "stat": {  # --- some statistics calculated using "raw" sections:
                "portfolioCostRUB": 0.,  # portfolio cost in RUB (Russian Rouble)
                "availableRUB": 0.,  # available rubles (without other currencies)
                "blockedRUB": 0.,  # blocked sum in Russian Rouble
                "totalChangesRUB": 0.,  # changes for all open trades in RUB
                "totalChangesPercentRUB": 0.,  # changes for all open trades in percents
                "allCurrenciesCostRUB": 0.,  # costs of all currencies (include rubles) in RUB
                "sharesCostRUB": 0.,  # costs of all shares in RUB
                "bondsCostRUB": 0.,  # costs of all bonds in RUB
                "etfsCostRUB": 0.,  # costs of all etfs in RUB
                "futuresCostRUB": 0.,  # costs of all futures in RUB
                "Currencies": [],  # list of dictionaries of all currencies statistics
                "Shares": [],  # list of dictionaries of all shares statistics
                "Bonds": [],  # list of dictionaries of all bonds statistics
                "Etfs": [],  # list of dictionaries of all etfs statistics
                "Futures": [],  # list of dictionaries of all futures statistics
                "orders": [],  # list of dictionaries of all pending (market) orders and it's parameters
                "stopOrders": [],  # list of dictionaries of all stop orders and it's parameters
                "blockedCurrencies": {},  # dict with blocked instruments and currencies, e.g. {"rub": 1291.87, "usd": 6.21}
                "blockedInstruments": {},  # dict with blocked  by FIGI, e.g. {}
                "funds": {},  # dict with free funds for trading (total - blocked), by all currencies, e.g. {"rub": {"total": 10000.99, "totalCostRUB": 10000.99, "free": 1234.56, "freeCostRUB": 1234.56}, "usd": {"total": 250.55, "totalCostRUB": 15375.80, "free": 125.05, "freeCostRUB": 7687.50}}
            },
            "analytics": {  # --- some analytics of portfolio:
                "distrByAssets": {},  # portfolio distribution by assets
                "distrByCompanies": {},  # portfolio distribution by companies
                "distrBySectors": {},  # portfolio distribution by sectors
                "distrByCurrencies": {},  # portfolio distribution by currencies
                "distrByCountries": {},  # portfolio distribution by countries
                "bondsCalendar": None,  # bonds payment calendar as Pandas DataFrame (if these present in portfolio)
            }
        }

        details = details.lower()
        availableDetails = ["full", "positions", "orders", "analytics", "calendar", "digest"]
        if details not in availableDetails:
            details = "full"
            uLogger.debug("Requested incorrect details! The `details` must be one of this strings: {}. Details parameter set to `full` be default.".format(availableDetails))

        uLogger.debug("Requesting portfolio of a client. Wait, please...")

        portfolioResponse = self.RequestPortfolio()  # current user's portfolio (dict)
        view["raw"]["positions"] = self.RequestPositions()  # current open positions by instruments (dict)
        view["raw"]["orders"] = self.RequestPendingOrders()  # current actual pending limit orders (list)
        view["raw"]["stopOrders"] = self.RequestStopOrders()  # current actual stop orders (list)

        # save response headers without "positions" section:
        for key in portfolioResponse.keys():
            if key != "positions":
                view["raw"]["headers"][key] = portfolioResponse[key]

            else:
                continue

        # Re-sorting and separating given raw instruments and currencies by type: https://tinkoff.github.io/investAPI/operations/#operation
        # Type of instrument must be only one of supported types in TKS_INSTRUMENTS
        for item in portfolioResponse["positions"]:
            if item["instrumentType"] == "currency":
                self._figi = item["figi"]
                if not self._figi and item["ticker"]:
                    self._ticker = item["ticker"]
                    self._figi = self.SearchByTicker()["figi"]  # Get FIGI to avoid warnings

                curr = self.SearchByFIGI(requestPrice=False)

                # current price of currency in RUB:
                view["raw"]["currenciesCurrentPrices"][curr["nominal"]["currency"]] = {
                    "name": curr["name"],
                    "currentPrice": NanoToFloat(
                        item["currentPrice"]["units"],
                        item["currentPrice"]["nano"]
                    ),
                }

                view["raw"]["Currencies"].append(item)

            elif item["instrumentType"] == "share":
                view["raw"]["Shares"].append(item)

            elif item["instrumentType"] == "bond":
                view["raw"]["Bonds"].append(item)

            elif item["instrumentType"] == "etf":
                view["raw"]["Etfs"].append(item)

            elif item["instrumentType"] == "futures":
                view["raw"]["Futures"].append(item)

            else:
                continue

        # how many volume of currencies (by ISO currency name) are blocked:
        for item in view["raw"]["positions"]["blocked"]:
            blocked = NanoToFloat(item["units"], item["nano"])
            if blocked > 0:
                view["stat"]["blockedCurrencies"][item["currency"]] = blocked

        # how many volume of instruments (by FIGI) are blocked:
        for item in view["raw"]["positions"]["securities"]:
            blocked = int(item["blocked"])
            if blocked > 0:
                view["stat"]["blockedInstruments"][item["figi"]] = blocked

        allBlocked = {**view["stat"]["blockedCurrencies"], **view["stat"]["blockedInstruments"]}

        if "rub" in allBlocked.keys():
            view["stat"]["blockedRUB"] = allBlocked["rub"]  # blocked rubles

        # --- saving current total amount in RUB of all currencies (with ruble), shares, bonds, etfs, futures and currencies:
        view["stat"]["allCurrenciesCostRUB"] = NanoToFloat(portfolioResponse["totalAmountCurrencies"]["units"], portfolioResponse["totalAmountCurrencies"]["nano"])
        view["stat"]["sharesCostRUB"] = NanoToFloat(portfolioResponse["totalAmountShares"]["units"], portfolioResponse["totalAmountShares"]["nano"])
        view["stat"]["bondsCostRUB"] = NanoToFloat(portfolioResponse["totalAmountBonds"]["units"], portfolioResponse["totalAmountBonds"]["nano"])
        view["stat"]["etfsCostRUB"] = NanoToFloat(portfolioResponse["totalAmountEtf"]["units"], portfolioResponse["totalAmountEtf"]["nano"])
        view["stat"]["futuresCostRUB"] = NanoToFloat(portfolioResponse["totalAmountFutures"]["units"], portfolioResponse["totalAmountFutures"]["nano"])
        view["stat"]["portfolioCostRUB"] = sum([
            view["stat"]["allCurrenciesCostRUB"],
            view["stat"]["sharesCostRUB"],
            view["stat"]["bondsCostRUB"],
            view["stat"]["etfsCostRUB"],
            view["stat"]["futuresCostRUB"],
        ])

        # --- calculating some portfolio statistics:
        byComp = {}  # distribution by companies
        bySect = {}  # distribution by sectors
        byCurr = {}  # distribution by currencies (include RUB)
        unknownCountryName = "All other countries"  # default name for instruments without "countryOfRisk" and "countryOfRiskName"
        byCountry = {unknownCountryName: {"cost": 0, "percent": 0.}}  # distribution by countries (currencies are included in their countries)

        for item in portfolioResponse["positions"]:
            self._figi = item["figi"]
            if not self._figi and item["ticker"]:
                self._ticker = item["ticker"]
                self._figi = self.SearchByTicker()["figi"]  # Get FIGI to avoid warnings

            instrument = self.SearchByFIGI(requestPrice=False)  # full raw info about instrument by FIGI

            if instrument:
                if item["instrumentType"] == "currency" and instrument["nominal"]["currency"] in allBlocked.keys():
                    blocked = allBlocked[instrument["nominal"]["currency"]]  # blocked volume of currency

                elif item["instrumentType"] != "currency" and item["figi"] in allBlocked.keys():
                    blocked = allBlocked[item["figi"]]  # blocked volume of other instruments

                else:
                    blocked = 0

                volume = NanoToFloat(item["quantity"]["units"], item["quantity"]["nano"])  # available volume of instrument
                lots = NanoToFloat(item["quantityLots"]["units"], item["quantityLots"]["nano"])  # available volume in lots of instrument
                direction = "Long" if lots >= 0 else "Short"  # direction of an instrument's position: short or long
                curPrice = NanoToFloat(item["currentPrice"]["units"], item["currentPrice"]["nano"])  # current instrument's price
                average = NanoToFloat(item["averagePositionPriceFifo"]["units"], item["averagePositionPriceFifo"]["nano"])  # current average position price
                profit = NanoToFloat(item["expectedYield"]["units"], item["expectedYield"]["nano"])  # expected profit at current moment
                currency = instrument["currency"] if (item["instrumentType"] == "share" or item["instrumentType"] == "etf" or item["instrumentType"] == "future") else instrument["nominal"]["currency"]  # currency name rub, usd, eur etc.
                cost = curPrice if "currentNkd" not in item.keys() else (curPrice + NanoToFloat(item["currentNkd"]["units"], item["currentNkd"]["nano"])) * volume  # current cost of all volume of instrument in basic asset
                baseCurrencyName = item["currentPrice"]["currency"]  # name of base currency (rub)
                countryName = "[{}] {}".format(instrument["countryOfRisk"], instrument["countryOfRiskName"]) if "countryOfRisk" in instrument.keys() and "countryOfRiskName" in instrument.keys() and instrument["countryOfRisk"] and instrument["countryOfRiskName"] else unknownCountryName
                costRUB = cost if item["instrumentType"] == "currency" else cost * view["raw"]["currenciesCurrentPrices"][currency]["currentPrice"]  # cost in rubles
                percentCostRUB = 100 * costRUB / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.  # instrument's part in percent of full portfolio cost

                statData = {
                    "figi": item["figi"],  # FIGI from REST API "GetPortfolio" method
                    "ticker": instrument["ticker"],  # ticker by FIGI
                    "currency": currency,  # currency name rub, usd, eur etc. for instrument price
                    "volume": volume,  # available volume of instrument
                    "lots": lots,  # volume in lots of instrument
                    "direction": direction,  # direction of an instrument's position: short or long
                    "blocked": blocked,  # blocked volume of currency or instrument
                    "currentPrice": curPrice,  # current instrument's price in basic asset
                    "average": average,  # current average position price
                    "cost": cost,  # current cost of all volume of instrument in basic asset
                    "baseCurrencyName": baseCurrencyName,  # name of base currency (rub)
                    "costRUB": costRUB,  # cost of instrument in ruble
                    "percentCostRUB": percentCostRUB,  # instrument's part in percent of full portfolio cost in RUB
                    "profit": profit,  # expected profit at current moment
                    "percentProfit": 100 * profit / (average * volume) if average != 0 and volume != 0 else 0,  # expected percents of profit at current moment for this instrument
                    "sector": instrument["sector"] if "sector" in instrument.keys() and instrument["sector"] else "other",
                    "name": instrument["name"] if "name" in instrument.keys() else "",  # human-readable names of instruments
                    "isoCurrencyName": instrument["isoCurrencyName"] if "isoCurrencyName" in instrument.keys() else "",  # ISO name for currencies only
                    "country": countryName,  # e.g. "[RU] Российская Федерация" or unknownCountryName
                    "step": instrument["step"],  # minimum price increment
                }

                # adding distribution by unique countries:
                if statData["country"] not in byCountry.keys():
                    byCountry[statData["country"]] = {"cost": costRUB, "percent": percentCostRUB}

                else:
                    byCountry[statData["country"]]["cost"] += costRUB
                    byCountry[statData["country"]]["percent"] += percentCostRUB

                if item["instrumentType"] != "currency":
                    # adding distribution by unique companies:
                    if statData["name"]:
                        if statData["name"] not in byComp.keys():
                            byComp[statData["name"]] = {"ticker": statData["ticker"], "cost": costRUB, "percent": percentCostRUB}

                        else:
                            byComp[statData["name"]]["cost"] += costRUB
                            byComp[statData["name"]]["percent"] += percentCostRUB

                    # adding distribution by unique sectors:
                    if statData["sector"] not in bySect.keys():
                        bySect[statData["sector"]] = {"cost": costRUB, "percent": percentCostRUB}

                    else:
                        bySect[statData["sector"]]["cost"] += costRUB
                        bySect[statData["sector"]]["percent"] += percentCostRUB

                # adding distribution by unique currencies:
                if currency not in byCurr.keys():
                    byCurr[currency] = {
                        "name": view["raw"]["currenciesCurrentPrices"][currency]["name"],
                        "cost": costRUB,
                        "percent": percentCostRUB
                    }

                else:
                    byCurr[currency]["cost"] += costRUB
                    byCurr[currency]["percent"] += percentCostRUB

                # saving statistics for every instrument:
                if item["instrumentType"] == "currency":
                    view["stat"]["Currencies"].append(statData)

                    # update dict with free funds for trading (total - blocked) by currencies
                    # e.g. {"rub": {"total": 10000.99, "totalCostRUB": 10000.99, "free": 1234.56, "freeCostRUB": 1234.56}, "usd": {"total": 250.55, "totalCostRUB": 15375.80, "free": 125.05, "freeCostRUB": 7687.50}}
                    view["stat"]["funds"][currency] = {
                        "total": round(volume, 6),
                        "totalCostRUB": round(costRUB * volume, 6),  # total volume cost in rubles
                        "free": round(volume - blocked, 6),
                        "freeCostRUB": round(costRUB * (volume - blocked), 6),  # free volume cost in rubles
                    }

                elif item["instrumentType"] == "share":
                    view["stat"]["Shares"].append(statData)

                elif item["instrumentType"] == "bond":
                    view["stat"]["Bonds"].append(statData)

                elif item["instrumentType"] == "etf":
                    view["stat"]["Etfs"].append(statData)

                elif item["instrumentType"] == "Futures":
                    view["stat"]["Futures"].append(statData)

                else:
                    continue

        # total changes in Russian Ruble:
        view["stat"]["availableRUB"] = view["stat"]["allCurrenciesCostRUB"] - sum([item["cost"] for item in view["stat"]["Currencies"]])  # available RUB without other currencies
        view["stat"]["totalChangesPercentRUB"] = NanoToFloat(view["raw"]["headers"]["expectedYield"]["units"], view["raw"]["headers"]["expectedYield"]["nano"]) if "expectedYield" in view["raw"]["headers"].keys() else 0.
        startCost = view["stat"]["portfolioCostRUB"] / (1 + view["stat"]["totalChangesPercentRUB"] / 100)
        view["stat"]["totalChangesRUB"] = view["stat"]["portfolioCostRUB"] - startCost

        # --- pending limit orders sector data:
        uniquePendingOrdersFIGIs = []  # unique FIGIs of pending limit orders to avoid many times price requests
        uniquePendingOrders = {}  # unique instruments with FIGIs as dictionary keys

        for item in view["raw"]["orders"]:
            self._figi = item["figi"]

            if item["figi"] not in uniquePendingOrdersFIGIs:
                instrument = self.SearchByFIGI(requestPrice=True)  # full raw info about instrument by FIGI, price requests only one time

                uniquePendingOrdersFIGIs.append(item["figi"])
                uniquePendingOrders[item["figi"]] = instrument

            else:
                instrument = uniquePendingOrders[item["figi"]]

            if instrument:
                action = TKS_ORDER_DIRECTIONS[item["direction"]]
                orderType = TKS_ORDER_TYPES[item["orderType"]]
                orderState = TKS_ORDER_STATES[item["executionReportStatus"]]
                orderDate = item["orderDate"].replace("T", " ").replace("Z", "").split(".")[0]  # date in UTC format, e.g. "2022-12-31T23:59:59.123456Z"

                # current instrument's price (last sellers order if you buy, and last buyers order if you sell):
                if item["direction"] == "ORDER_DIRECTION_BUY":
                    lastPrice = instrument["currentPrice"]["sell"][0]["price"] if instrument["currentPrice"]["sell"] else "N/A"

                else:
                    lastPrice = instrument["currentPrice"]["buy"][0]["price"] if instrument["currentPrice"]["buy"] else "N/A"

                # requested price for order execution:
                target = NanoToFloat(item["initialSecurityPrice"]["units"], item["initialSecurityPrice"]["nano"])

                # necessary changes in percent to reach target from current price:
                changes = 100 * (lastPrice - target) / target if lastPrice != "N/A" and target > 0 else 0

                view["stat"]["orders"].append({
                    "orderID": item["orderId"],  # orderId number parameter of current order
                    "figi": item["figi"],  # FIGI identification
                    "ticker": instrument["ticker"],  # ticker name by FIGI
                    "lotsRequested": item["lotsRequested"],  # requested lots value
                    "lotsExecuted": item["lotsExecuted"],  # how many lots are executed
                    "currentPrice": lastPrice,  # current instrument's price for defined action
                    "targetPrice": target,  # requested price for order execution in base currency
                    "baseCurrencyName": item["initialSecurityPrice"]["currency"],  # name of base currency
                    "percentChanges": changes,  # changes in percent to target from current price
                    "currency": item["currency"],  # instrument's currency name
                    "action": action,  # sell / buy / Unknown from TKS_ORDER_DIRECTIONS
                    "type": orderType,  # type of order from TKS_ORDER_TYPES
                    "status": orderState,  # order status from TKS_ORDER_STATES
                    "date": orderDate,  # string with order date and time from UTC format (without nanoseconds part)
                })

        # --- stop orders sector data:
        uniqueStopOrdersFIGIs = []  # unique FIGIs of stop orders to avoid many times price requests
        uniqueStopOrders = {}  # unique instruments with FIGIs as dictionary keys

        for item in view["raw"]["stopOrders"]:
            self._figi = item["figi"]

            if item["figi"] not in uniqueStopOrdersFIGIs:
                instrument = self.SearchByFIGI(requestPrice=True)  # full raw info about instrument by FIGI, price requests only one time

                uniqueStopOrdersFIGIs.append(item["figi"])
                uniqueStopOrders[item["figi"]] = instrument

            else:
                instrument = uniqueStopOrders[item["figi"]]

            if instrument:
                action = TKS_STOP_ORDER_DIRECTIONS[item["direction"]]
                orderType = TKS_STOP_ORDER_TYPES[item["orderType"]]
                createDate = item["createDate"].replace("T", " ").replace("Z", "").split(".")[0]  # date in UTC format, e.g. "2022-12-31T23:59:59.123456Z"

                # hack: server response can't contain "expirationTime" key if it is not "Until date" type of stop order
                if "expirationTime" in item.keys():
                    expType = TKS_STOP_ORDER_EXPIRATION_TYPES["STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE"]
                    expDate = item["expirationTime"].replace("T", " ").replace("Z", "").split(".")[0]

                else:
                    expType = TKS_STOP_ORDER_EXPIRATION_TYPES["STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL"]
                    expDate = TKS_STOP_ORDER_EXPIRATION_TYPES["STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED"]

                # current instrument's price (last sellers order if you buy, and last buyers order if you sell):
                if item["direction"] == "STOP_ORDER_DIRECTION_BUY":
                    lastPrice = instrument["currentPrice"]["sell"][0]["price"] if instrument["currentPrice"]["sell"] else "N/A"

                else:
                    lastPrice = instrument["currentPrice"]["buy"][0]["price"] if instrument["currentPrice"]["buy"] else "N/A"

                # requested price when stop-order executed:
                target = NanoToFloat(item["stopPrice"]["units"], item["stopPrice"]["nano"])

                # price for limit-order, set up when stop-order executed:
                limit = NanoToFloat(item["price"]["units"], item["price"]["nano"])

                # necessary changes in percent to reach target from current price:
                changes = 100 * (lastPrice - target) / target if lastPrice != "N/A" and target > 0 else 0

                view["stat"]["stopOrders"].append({
                    "orderID": item["stopOrderId"],  # stopOrderId number parameter of current stop-order
                    "figi": item["figi"],  # FIGI identification
                    "ticker": instrument["ticker"],  # ticker name by FIGI
                    "lotsRequested": item["lotsRequested"],  # requested lots value
                    "currentPrice": lastPrice,  # current instrument's price for defined action
                    "targetPrice": target,  # requested price for stop-order execution in base currency
                    "limitPrice": limit,  # price for limit-order, set up when stop-order executed, 0 if market order
                    "baseCurrencyName": item["stopPrice"]["currency"],  # name of base currency
                    "percentChanges": changes,  # changes in percent to target from current price
                    "currency": item["currency"],  # instrument's currency name
                    "action": action,  # sell / buy / Unknown from TKS_STOP_ORDER_DIRECTIONS
                    "type": orderType,  # type of order from TKS_STOP_ORDER_TYPES
                    "expType": expType,  # expiration type of stop-order from TKS_STOP_ORDER_EXPIRATION_TYPES
                    "createDate": createDate,  # string with created order date and time from UTC format (without nanoseconds part)
                    "expDate": expDate,  # string with expiration order date and time from UTC format (without nanoseconds part)
                })

        # --- calculating data for analytics section:
        # portfolio distribution by assets:
        view["analytics"]["distrByAssets"] = {
            "Ruble": {
                "uniques": 1,
                "cost": view["stat"]["availableRUB"],
                "percent": 100 * view["stat"]["availableRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
            "Currencies": {
                "uniques": len(view["stat"]["Currencies"]),  # all foreign currencies without RUB
                "cost": view["stat"]["allCurrenciesCostRUB"] - view["stat"]["availableRUB"],
                "percent": 100 * (view["stat"]["allCurrenciesCostRUB"] - view["stat"]["availableRUB"]) / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
            "Shares": {
                "uniques": len(view["stat"]["Shares"]),
                "cost": view["stat"]["sharesCostRUB"],
                "percent": 100 * view["stat"]["sharesCostRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
            "Bonds": {
                "uniques": len(view["stat"]["Bonds"]),
                "cost": view["stat"]["bondsCostRUB"],
                "percent": 100 * view["stat"]["bondsCostRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
            "Etfs": {
                "uniques": len(view["stat"]["Etfs"]),
                "cost": view["stat"]["etfsCostRUB"],
                "percent": 100 * view["stat"]["etfsCostRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
            "Futures": {
                "uniques": len(view["stat"]["Futures"]),
                "cost": view["stat"]["futuresCostRUB"],
                "percent": 100 * view["stat"]["futuresCostRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
            },
        }

        # portfolio distribution by companies:
        view["analytics"]["distrByCompanies"]["All money cash"] = {
            "ticker": "",
            "cost": view["stat"]["allCurrenciesCostRUB"],
            "percent": 100 * view["stat"]["allCurrenciesCostRUB"] / view["stat"]["portfolioCostRUB"] if view["stat"]["portfolioCostRUB"] > 0 else 0.,
        }
        view["analytics"]["distrByCompanies"].update(byComp)

        # portfolio distribution by sectors:
        view["analytics"]["distrBySectors"]["All money cash"] = {
            "cost": view["analytics"]["distrByCompanies"]["All money cash"]["cost"],
            "percent": view["analytics"]["distrByCompanies"]["All money cash"]["percent"],
        }
        view["analytics"]["distrBySectors"].update(bySect)

        # portfolio distribution by currencies:
        if "rub" not in view["analytics"]["distrByCurrencies"].keys():
            view["analytics"]["distrByCurrencies"]["rub"] = {"name": "Российский рубль", "cost": 0, "percent": 0}

            if self.moreDebug:
                uLogger.debug("Fast hack to avoid issues #71 in `Portfolio distribution by currencies` section. Server not returned current available rubles!")

        view["analytics"]["distrByCurrencies"].update(byCurr)
        view["analytics"]["distrByCurrencies"]["rub"]["cost"] += view["analytics"]["distrByAssets"]["Ruble"]["cost"]
        view["analytics"]["distrByCurrencies"]["rub"]["percent"] += view["analytics"]["distrByAssets"]["Ruble"]["percent"]

        # portfolio distribution by countries:
        if "[RU] Российская Федерация" not in view["analytics"]["distrByCountries"].keys():
            view["analytics"]["distrByCountries"]["[RU] Российская Федерация"] = {"cost": 0, "percent": 0}

            if self.moreDebug:
                uLogger.debug("Fast hack to avoid issues #71 in `Portfolio distribution by countries` section. Server not returned current available rubles!")

        view["analytics"]["distrByCountries"].update(byCountry)
        view["analytics"]["distrByCountries"]["[RU] Российская Федерация"]["cost"] += view["analytics"]["distrByAssets"]["Ruble"]["cost"]
        view["analytics"]["distrByCountries"]["[RU] Российская Федерация"]["percent"] += view["analytics"]["distrByAssets"]["Ruble"]["percent"]

        # --- Prepare text statistics overview in human-readable:
        if show or onlyFiles:
            actualOnDate = datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)

            # Whatever the value `details`, header not changes:
            info = [
                "# Client's portfolio\n\n",
                "* **Actual on date:** [{} UTC]\n".format(actualOnDate),
                "* **Account ID:** [{}]\n".format(self.accountId),
            ]

            if details in ["full", "positions", "digest"]:
                info.extend([
                    "* **Portfolio cost:** {:.2f} RUB\n".format(view["stat"]["portfolioCostRUB"]),
                    "* **Changes:** {}{:.2f} RUB ({}{:.2f}%)\n\n".format(
                        "+" if view["stat"]["totalChangesRUB"] > 0 else "",
                        view["stat"]["totalChangesRUB"],
                        "+" if view["stat"]["totalChangesPercentRUB"] > 0 else "",
                        view["stat"]["totalChangesPercentRUB"],
                    ),
                ])

            if details in ["full", "positions"]:
                info.extend([
                    "## Open positions\n\n",
                    "| Ticker [FIGI]               | Volume (blocked)                | Lots     | Curr. price  | Avg. price   | Current volume cost | Profit (%)                   |\n",
                    "|-----------------------------|---------------------------------|----------|--------------|--------------|---------------------|------------------------------|\n",
                    "| **Ruble:**                  | {:>31} |          |              |              |                     |                              |\n".format(
                        "{:.2f} ({:.2f}) rub".format(
                            view["stat"]["availableRUB"],
                            view["stat"]["blockedRUB"],
                        )
                    )
                ])

                def _SplitStr(CostRUB: float = 0, typeStr: str = "", noTradeStr: str = "") -> list:
                    return [
                        "|                             |                                 |          |              |              |                     |                              |\n",
                        "| {:<27} |                                 |          |              |              | {:>19} |                              |\n".format(
                            noTradeStr if noTradeStr else typeStr,
                            "" if noTradeStr else "{:.2f} RUB".format(CostRUB),
                        ),
                    ]

                def _InfoStr(data: dict, isCurr: bool = False) -> str:
                    return "| {:<27} | {:>31} | {:<8} | {:>12} | {:>12} | {:>19} | {:<28} |\n".format(
                        "{} [{}]".format(data["ticker"], data["figi"]),
                        "{:.2f} ({:.2f}) {}".format(
                            data["volume"],
                            data["blocked"],
                            data["currency"],
                        ) if isCurr else "{:.0f} ({:.0f})".format(
                            data["volume"],
                            data["blocked"],
                        ),
                        "—" if isCurr else "{:.4f}".format(data["lots"]).rstrip("0").rstrip("."),
                        "{:.2f} {}".format(data["currentPrice"], data["baseCurrencyName"]) if data["currentPrice"] > 0 else "n/a",
                        "{:.2f} {}".format(data["average"], data["baseCurrencyName"]) if data["average"] > 0 else "n/a",
                        "{:.2f} {}".format(data["cost"], data["baseCurrencyName"]),
                        "{}{:.2f} {} ({}{:.2f}%)".format(
                            "+" if data["profit"] > 0 else "",
                            data["profit"], data["baseCurrencyName"],
                            "+" if data["percentProfit"] > 0 else "",
                            data["percentProfit"],
                        ),
                    )

                # --- Show currencies section:
                if view["stat"]["Currencies"]:
                    info.extend(_SplitStr(CostRUB=view["analytics"]["distrByAssets"]["Currencies"]["cost"], typeStr="**Currencies:**"))
                    for item in view["stat"]["Currencies"]:
                        info.append(_InfoStr(item, isCurr=True))

                else:
                    info.extend(_SplitStr(noTradeStr="**Currencies:** no trades"))

                # --- Show shares section:
                if view["stat"]["Shares"]:
                    info.extend(_SplitStr(CostRUB=view["stat"]["sharesCostRUB"], typeStr="**Shares:**"))

                    for item in view["stat"]["Shares"]:
                        info.append(_InfoStr(item))

                else:
                    info.extend(_SplitStr(noTradeStr="**Shares:** no trades"))

                # --- Show bonds section:
                if view["stat"]["Bonds"]:
                    info.extend(_SplitStr(CostRUB=view["stat"]["bondsCostRUB"], typeStr="**Bonds:**"))

                    for item in view["stat"]["Bonds"]:
                        info.append(_InfoStr(item))

                else:
                    info.extend(_SplitStr(noTradeStr="**Bonds:** no trades"))

                # --- Show etfs section:
                if view["stat"]["Etfs"]:
                    info.extend(_SplitStr(CostRUB=view["stat"]["etfsCostRUB"], typeStr="**Etfs:**"))

                    for item in view["stat"]["Etfs"]:
                        info.append(_InfoStr(item))

                else:
                    info.extend(_SplitStr(noTradeStr="**Etfs:** no trades"))

                # --- Show futures section:
                if view["stat"]["Futures"]:
                    info.extend(_SplitStr(CostRUB=view["stat"]["futuresCostRUB"], typeStr="**Futures:**"))

                    for item in view["stat"]["Futures"]:
                        info.append(_InfoStr(item))

                else:
                    info.extend(_SplitStr(noTradeStr="**Futures:** no trades"))

            if details in ["full", "orders"]:
                # --- Show pending limit orders section:
                if view["stat"]["orders"]:
                    info.extend([
                        "\n## Opened pending limit-orders: [{}]\n".format(len(view["stat"]["orders"])),
                        "\n| Ticker [FIGI]               | Order ID       | Lots (exec.) | Current price (% delta) | Target price  | Action    | Type      | Create date (UTC)       |\n",
                        "|-----------------------------|----------------|--------------|-------------------------|---------------|-----------|-----------|-------------------------|\n",
                    ])

                    for item in view["stat"]["orders"]:
                        info.append("| {:<27} | {:<14} | {:<12} | {:>23} | {:>13} | {:<9} | {:<9} | {:<23} |\n".format(
                            "{} [{}]".format(item["ticker"], item["figi"]),
                            item["orderID"],
                            "{} ({})".format(item["lotsRequested"], item["lotsExecuted"]),
                            "{} {} ({}{:.2f}%)".format(
                                "{}".format(item["currentPrice"]) if isinstance(item["currentPrice"], str) else "{:.2f}".format(float(item["currentPrice"])),
                                item["baseCurrencyName"],
                                "+" if item["percentChanges"] > 0 else "",
                                float(item["percentChanges"]),
                            ),
                            "{:.2f} {}".format(float(item["targetPrice"]), item["baseCurrencyName"]),
                            item["action"],
                            item["type"],
                            item["date"],
                        ))

                else:
                    info.append("\n## Total pending limit-orders: [0]\n")

                # --- Show stop orders section:
                if view["stat"]["stopOrders"]:
                    info.extend([
                        "\n## Opened stop-orders: [{}]\n".format(len(view["stat"]["stopOrders"])),
                        "\n| Ticker [FIGI]               | Stop order ID                        | Lots   | Current price (% delta) | Target price  | Limit price   | Action    | Type        | Expire type  | Create date (UTC)   | Expiration (UTC)    |\n",
                        "|-----------------------------|--------------------------------------|--------|-------------------------|---------------|---------------|-----------|-------------|--------------|---------------------|---------------------|\n",
                    ])

                    for item in view["stat"]["stopOrders"]:
                        info.append("| {:<27} | {:<14} | {:<6} | {:>23} | {:>13} | {:>13} | {:<9} | {:<11} | {:<12} | {:<19} | {:<19} |\n".format(
                            "{} [{}]".format(item["ticker"], item["figi"]),
                            item["orderID"],
                            item["lotsRequested"],
                            "{} {} ({}{:.2f}%)".format(
                                "{}".format(item["currentPrice"]) if isinstance(item["currentPrice"], str) else "{:.2f}".format(float(item["currentPrice"])),
                                item["baseCurrencyName"],
                                "+" if item["percentChanges"] > 0 else "",
                                float(item["percentChanges"]),
                            ),
                            "{:.2f} {}".format(float(item["targetPrice"]), item["baseCurrencyName"]),
                            "{:.2f} {}".format(float(item["limitPrice"]), item["baseCurrencyName"]) if item["limitPrice"] and item["limitPrice"] != item["targetPrice"] else TKS_ORDER_TYPES["ORDER_TYPE_MARKET"],
                            item["action"],
                            item["type"],
                            item["expType"],
                            item["createDate"],
                            item["expDate"],
                        ))

                else:
                    info.append("\n## Total stop-orders: [0]\n")

            if details in ["full", "analytics"]:
                # -- Show analytics section:
                if view["stat"]["portfolioCostRUB"] > 0:
                    info.extend([
                        "\n# Analytics\n\n"
                        "* **Actual on date:** [{} UTC]\n".format(actualOnDate),
                        "* **Current total portfolio cost:** {:.2f} RUB\n".format(view["stat"]["portfolioCostRUB"]),
                        "* **Changes:** {}{:.2f} RUB ({}{:.2f}%)\n".format(
                            "+" if view["stat"]["totalChangesRUB"] > 0 else "",
                            view["stat"]["totalChangesRUB"],
                            "+" if view["stat"]["totalChangesPercentRUB"] > 0 else "",
                            view["stat"]["totalChangesPercentRUB"],
                        ),
                        "\n## Portfolio distribution by assets\n"
                        "\n| Type                               | Uniques | Percent | Current cost       |\n",
                        "|------------------------------------|---------|---------|--------------------|\n",
                    ])

                    for key in view["analytics"]["distrByAssets"].keys():
                        if view["analytics"]["distrByAssets"][key]["cost"] > 0:
                            info.append("| {:<34} | {:<7} | {:<7} | {:<18} |\n".format(
                                key,
                                view["analytics"]["distrByAssets"][key]["uniques"],
                                "{:.2f}%".format(view["analytics"]["distrByAssets"][key]["percent"]),
                                "{:.2f} rub".format(view["analytics"]["distrByAssets"][key]["cost"]),
                            ))

                    aSepLine = "|----------------------------------------------|---------|--------------------|\n"

                    info.extend([
                        "\n## Portfolio distribution by companies\n"
                        "\n| Company                                      | Percent | Current cost       |\n",
                        aSepLine,
                    ])

                    for company in view["analytics"]["distrByCompanies"].keys():
                        if view["analytics"]["distrByCompanies"][company]["cost"] > 0:
                            info.append("| {:<44} | {:<7} | {:<18} |\n".format(
                                "{}{}".format(
                                    "[{}] ".format(view["analytics"]["distrByCompanies"][company]["ticker"]) if view["analytics"]["distrByCompanies"][company]["ticker"] else "",
                                    company,
                                ),
                                "{:.2f}%".format(view["analytics"]["distrByCompanies"][company]["percent"]),
                                "{:.2f} rub".format(view["analytics"]["distrByCompanies"][company]["cost"]),
                            ))

                    info.extend([
                        "\n## Portfolio distribution by sectors\n"
                        "\n| Sector                                       | Percent | Current cost       |\n",
                        aSepLine,
                    ])

                    for sector in view["analytics"]["distrBySectors"].keys():
                        if view["analytics"]["distrBySectors"][sector]["cost"] > 0:
                            info.append("| {:<44} | {:<7} | {:<18} |\n".format(
                                sector,
                                "{:.2f}%".format(view["analytics"]["distrBySectors"][sector]["percent"]),
                                "{:.2f} rub".format(view["analytics"]["distrBySectors"][sector]["cost"]),
                            ))

                    info.extend([
                        "\n## Portfolio distribution by currencies\n"
                        "\n| Instruments currencies                       | Percent | Current cost       |\n",
                        aSepLine,
                    ])

                    for curr in view["analytics"]["distrByCurrencies"].keys():
                        if view["analytics"]["distrByCurrencies"][curr]["cost"] > 0:
                            info.append("| {:<44} | {:<7} | {:<18} |\n".format(
                                "[{}] {}".format(curr, view["analytics"]["distrByCurrencies"][curr]["name"]),
                                "{:.2f}%".format(view["analytics"]["distrByCurrencies"][curr]["percent"]),
                                "{:.2f} rub".format(view["analytics"]["distrByCurrencies"][curr]["cost"]),
                            ))

                    info.extend([
                        "\n## Portfolio distribution by countries\n"
                        "\n| Assets by country                            | Percent | Current cost       |\n",
                        aSepLine,
                    ])

                    for country in view["analytics"]["distrByCountries"].keys():
                        if view["analytics"]["distrByCountries"][country]["cost"] > 0:
                            info.append("| {:<44} | {:<7} | {:<18} |\n".format(
                                country,
                                "{:.2f}%".format(view["analytics"]["distrByCountries"][country]["percent"]),
                                "{:.2f} rub".format(view["analytics"]["distrByCountries"][country]["cost"]),
                            ))

            if details in ["full", "calendar"]:
                # -- Show bonds payment calendar section:
                if view["stat"]["Bonds"]:
                    bondTickers = [item["ticker"] for item in view["stat"]["Bonds"]]
                    view["analytics"]["bondsCalendar"] = self.ExtendBondsData(instruments=bondTickers, xlsx=False)
                    info.append("\n" + self.ShowBondsCalendar(extBonds=view["analytics"]["bondsCalendar"], show=False))

                else:
                    info.append("\n# Bond payments calendar\n\nNo bonds in the portfolio to create payments calendar\n")

            infoText = "".join(info)

            if show and not onlyFiles:
                uLogger.info(infoText)

            if details == "full" and self.overviewFile:
                filename = self.overviewFile

            elif details == "digest" and self.overviewDigestFile:
                filename = self.overviewDigestFile

            elif details == "positions" and self.overviewPositionsFile:
                filename = self.overviewPositionsFile

            elif details == "orders" and self.overviewOrdersFile:
                filename = self.overviewOrdersFile

            elif details == "analytics" and self.overviewAnalyticsFile:
                filename = self.overviewAnalyticsFile

            elif details == "calendar" and self.overviewBondsCalendarFile:
                filename = self.overviewBondsCalendarFile

            else:
                filename = ""

            if filename and (show or onlyFiles):
                with open(filename, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Client's portfolio was saved to file: [{}]".format(os.path.abspath(filename)))

                if self.useHTMLReports:
                    htmlFilePath = filename.replace(".md", ".html") if filename.endswith(".md") else filename + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Client's portfolio", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return view

    def Deals(self, start: str = None, end: str = None, show: bool = False, showCancelled: bool = True, onlyFiles=False) -> tuple[list[dict], dict]:
        """
        Returns history operations between two given dates for current `accountId`.
        If `reportFile` string is not empty then also save human-readable report.
        Shows some statistical data of closed positions.

        :param start: see docstring in `TradeRoutines.GetDatesAsString()` method.
        :param end: see docstring in `TradeRoutines.GetDatesAsString()` method.
        :param show: if `True` then also prints all records to the console.
        :param showCancelled: if `False` then remove information about cancelled operations from the deals report.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: original list of dictionaries with history of deals records from API ("operations" key):
                 https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetOperations
                 and dictionary with custom stats: operations in different currencies, withdrawals, incomes etc.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        startDate, endDate = GetDatesAsString(start, end, userFormat=TKS_DATE_FORMAT, outputFormat=TKS_DATE_TIME_FORMAT)  # Example: ("2000-01-01T00:00:00Z", "2022-12-31T23:59:59Z")

        uLogger.debug("Requesting history of a client's operations. Wait, please...")

        # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetOperations
        dealsURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetOperations"
        self.body = str({"accountId": self.accountId, "from": startDate, "to": endDate})
        ops = self.SendAPIRequest(dealsURL, reqType="POST")["operations"]  # list of dict: operations returns by broker
        customStat = {}  # custom statistics in additional to responseJSON

        # --- output report in human-readable format:
        if self.reportFile and (show or onlyFiles):
            splitLine1 = "|                            |                               |                              |                      |                        |\n"  # Summary section
            splitLine2 = "|                     |              |              |            |           |                 |            |                                                                    |\n"  # Operations section
            nextDay = ""

            info = ["# Client's operations\n\n* **Period:** from [{}] to [{}]\n\n## Summary (operations executed only)\n\n".format(startDate.split("T")[0], endDate.split("T")[0])]

            if len(ops) > 0:
                customStat = {
                    "opsCount": 0,  # total operations count
                    "buyCount": 0,  # buy operations
                    "sellCount": 0,  # sell operations
                    "buyTotal": {"rub": 0.},  # Buy sums in different currencies
                    "sellTotal": {"rub": 0.},  # Sell sums in different currencies
                    "payIn": {"rub": 0.},  # Deposit brokerage account
                    "payOut": {"rub": 0.},  # Withdrawals
                    "divs": {"rub": 0.},  # Dividends income
                    "coupons": {"rub": 0.},  # Coupon's income
                    "brokerCom": {"rub": 0.},  # Service commissions
                    "serviceCom": {"rub": 0.},  # Service commissions
                    "marginCom": {"rub": 0.},  # Margin commissions
                    "allTaxes": {"rub": 0.},  # Sum of withholding taxes and corrections
                }

                # --- calculating statistics depends on operations type in TKS_OPERATION_TYPES:
                for item in ops:
                    if item["state"] == "OPERATION_STATE_EXECUTED":
                        payment = NanoToFloat(item["payment"]["units"], item["payment"]["nano"])

                        # count buy operations:
                        if "_BUY" in item["operationType"]:
                            customStat["buyCount"] += 1

                            if item["payment"]["currency"] in customStat["buyTotal"].keys():
                                customStat["buyTotal"][item["payment"]["currency"]] += payment

                            else:
                                customStat["buyTotal"][item["payment"]["currency"]] = payment

                        # count sell operations:
                        elif "_SELL" in item["operationType"]:
                            customStat["sellCount"] += 1

                            if item["payment"]["currency"] in customStat["sellTotal"].keys():
                                customStat["sellTotal"][item["payment"]["currency"]] += payment

                            else:
                                customStat["sellTotal"][item["payment"]["currency"]] = payment

                        # count incoming operations:
                        elif item["operationType"] in ["OPERATION_TYPE_INPUT"]:
                            if item["payment"]["currency"] in customStat["payIn"].keys():
                                customStat["payIn"][item["payment"]["currency"]] += payment

                            else:
                                customStat["payIn"][item["payment"]["currency"]] = payment

                        # count withdrawals operations:
                        elif item["operationType"] in ["OPERATION_TYPE_OUTPUT"]:
                            if item["payment"]["currency"] in customStat["payOut"].keys():
                                customStat["payOut"][item["payment"]["currency"]] += payment

                            else:
                                customStat["payOut"][item["payment"]["currency"]] = payment

                        # count dividends income:
                        elif item["operationType"] in ["OPERATION_TYPE_DIVIDEND", "OPERATION_TYPE_DIVIDEND_TRANSFER", "OPERATION_TYPE_DIV_EXT"]:
                            if item["payment"]["currency"] in customStat["divs"].keys():
                                customStat["divs"][item["payment"]["currency"]] += payment

                            else:
                                customStat["divs"][item["payment"]["currency"]] = payment

                        # count coupon's income:
                        elif item["operationType"] in ["OPERATION_TYPE_COUPON", "OPERATION_TYPE_BOND_REPAYMENT_FULL", "OPERATION_TYPE_BOND_REPAYMENT"]:
                            if item["payment"]["currency"] in customStat["coupons"].keys():
                                customStat["coupons"][item["payment"]["currency"]] += payment

                            else:
                                customStat["coupons"][item["payment"]["currency"]] = payment

                        # count broker commissions:
                        elif item["operationType"] in ["OPERATION_TYPE_BROKER_FEE", "OPERATION_TYPE_SUCCESS_FEE", "OPERATION_TYPE_TRACK_MFEE", "OPERATION_TYPE_TRACK_PFEE"]:
                            if item["payment"]["currency"] in customStat["brokerCom"].keys():
                                customStat["brokerCom"][item["payment"]["currency"]] += payment

                            else:
                                customStat["brokerCom"][item["payment"]["currency"]] = payment

                        # count service commissions:
                        elif item["operationType"] in ["OPERATION_TYPE_SERVICE_FEE"]:
                            if item["payment"]["currency"] in customStat["serviceCom"].keys():
                                customStat["serviceCom"][item["payment"]["currency"]] += payment

                            else:
                                customStat["serviceCom"][item["payment"]["currency"]] = payment

                        # count margin commissions:
                        elif item["operationType"] in ["OPERATION_TYPE_MARGIN_FEE"]:
                            if item["payment"]["currency"] in customStat["marginCom"].keys():
                                customStat["marginCom"][item["payment"]["currency"]] += payment

                            else:
                                customStat["marginCom"][item["payment"]["currency"]] = payment

                        # count withholding taxes:
                        elif "_TAX" in item["operationType"]:
                            if item["payment"]["currency"] in customStat["allTaxes"].keys():
                                customStat["allTaxes"][item["payment"]["currency"]] += payment

                            else:
                                customStat["allTaxes"][item["payment"]["currency"]] = payment

                        else:
                            continue

                customStat["opsCount"] += customStat["buyCount"] + customStat["sellCount"]

                # --- view "Actions" lines:
                info.extend([
                    "| Report sections            |                               |                              |                      |                        |\n",
                    "|----------------------------|-------------------------------|------------------------------|----------------------|------------------------|\n",
                    "| **Actions:**               | Trades: {:<21} | Trading volumes:             |                      |                        |\n".format(customStat["opsCount"]),
                    "|                            |   Buy: {:<22} | {:<28} |                      |                        |\n".format(
                        "{} ({:.1f}%)".format(customStat["buyCount"], 100 * customStat["buyCount"] / customStat["opsCount"]) if customStat["opsCount"] != 0 else 0,
                        "  rub, buy: {:<16}".format("{:.2f}".format(customStat["buyTotal"]["rub"])) if customStat["buyTotal"]["rub"] != 0 else "  —",
                    ),
                    "|                            |   Sell: {:<21} | {:<28} |                      |                        |\n".format(
                        "{} ({:.1f}%)".format(customStat["sellCount"], 100 * customStat["sellCount"] / customStat["opsCount"]) if customStat["opsCount"] != 0 else 0,
                        "  rub, sell: {:<13}".format("+{:.2f}".format(customStat["sellTotal"]["rub"])) if customStat["sellTotal"]["rub"] != 0 else "  —",
                    ),
                ])

                opsKeys = sorted(list(set(list(customStat["buyTotal"].keys()) + list(customStat["sellTotal"].keys()))))
                for key in opsKeys:
                    if key == "rub":
                        continue

                    info.extend([
                        "|                            |                               | {:<28} |                      |                        |\n".format(
                            "  {}, buy: {:<16}".format(key, "{:.2f}".format(customStat["buyTotal"][key]) if key and key in customStat["buyTotal"].keys() and customStat["buyTotal"][key] != 0 else 0)
                        ),
                        "|                            |                               | {:<28} |                      |                        |\n".format(
                            "  {}, sell: {:<13}".format(key, "+{:.2f}".format(customStat["sellTotal"][key]) if key and key in customStat["sellTotal"].keys() and customStat["sellTotal"][key] != 0 else 0)
                        ),
                    ])

                info.append(splitLine1)

                def _InfoStr(data1: dict, data2: dict, data3: dict, data4: dict, cur: str = "") -> str:
                    return "|                            | {:<29} | {:<28} | {:<20} | {:<22} |\n".format(
                            "  {}: {}{:.2f}".format(cur, "+" if data1[cur] > 0 else "", data1[cur]) if cur and cur in data1.keys() and data1[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data2[cur] > 0 else "", data2[cur]) if cur and cur in data2.keys() and data2[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data3[cur] > 0 else "", data3[cur]) if cur and cur in data3.keys() and data3[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data4[cur] > 0 else "", data4[cur]) if cur and cur in data4.keys() and data4[cur] != 0 else "  —",
                    )

                # --- view "Payments" lines:
                info.append("| **Payments:**              | Deposit on broker account:    | Withdrawals:                 | Dividends income:    | Coupons income:        |\n")
                paymentsKeys = sorted(list(set(list(customStat["payIn"].keys()) + list(customStat["payOut"].keys()) + list(customStat["divs"].keys()) + list(customStat["coupons"].keys()))))

                for key in paymentsKeys:
                    info.append(_InfoStr(customStat["payIn"], customStat["payOut"], customStat["divs"], customStat["coupons"], key))

                info.append(splitLine1)

                # --- view "Commissions and taxes" lines:
                info.append("| **Commissions and taxes:** | Broker commissions:           | Service commissions:         | Margin commissions:  | All taxes/corrections: |\n")
                comKeys = sorted(list(set(list(customStat["brokerCom"].keys()) + list(customStat["serviceCom"].keys()) + list(customStat["marginCom"].keys()) + list(customStat["allTaxes"].keys()))))

                for key in comKeys:
                    info.append(_InfoStr(customStat["brokerCom"], customStat["serviceCom"], customStat["marginCom"], customStat["allTaxes"], key))

                info.extend([
                    "\n## All operations{}\n\n".format("" if showCancelled else " (without cancelled status)"),
                    "| Date and time       | FIGI         | Ticker       | Asset      | Value     | Payment         | Status     | Operation type                                                     |\n",
                    "|---------------------|--------------|--------------|------------|-----------|-----------------|------------|--------------------------------------------------------------------|\n",
                ])

            else:
                info.append("Broker returned no operations during this period\n")

            # --- view "Operations" section:
            for item in ops:
                if not showCancelled and TKS_OPERATION_STATES[item["state"]] == TKS_OPERATION_STATES["OPERATION_STATE_CANCELED"]:
                    continue

                else:
                    self._figi = item["figi"]
                    payment = NanoToFloat(item["payment"]["units"], item["payment"]["nano"])
                    instrument = self.SearchByFIGI(requestPrice=False) if self._figi else {}

                    # group of deals during one day:
                    if nextDay and item["date"].split("T")[0] != nextDay:
                        info.append(splitLine2)
                        nextDay = ""

                    else:
                        nextDay = item["date"].split("T")[0]  # saving current day for splitting

                    info.append("| {:<19} | {:<12} | {:<12} | {:<10} | {:<9} | {:>15} | {:<10} | {:<66} |\n".format(
                        item["date"].replace("T", " ").replace("Z", "").split(".")[0],
                        self._figi if self._figi else "—",
                        instrument["ticker"] if instrument else "—",
                        instrument["type"] if instrument else "—",
                        item["quantity"] if int(item["quantity"]) > 0 else "—",
                        "{}{:.2f} {}".format("+" if payment > 0 else "", payment, item["payment"]["currency"]) if payment != 0 else "—",
                        TKS_OPERATION_STATES[item["state"]],
                        TKS_OPERATION_TYPES[item["operationType"]],
                    ))

            infoText = "".join(info)

            if show and not onlyFiles:
                if self.moreDebug:
                    uLogger.debug("Records about history of a client's operations successfully received")

                uLogger.info(infoText)

            if self.reportFile and (show or onlyFiles):
                with open(self.reportFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("History of a client's operations are saved to file: [{}]".format(os.path.abspath(self.reportFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.reportFile.replace(".md", ".html") if self.reportFile.endswith(".md") else self.reportFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Client's operations", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return ops, customStat

    def History(self, start: str = None, end: str = None, interval: str = "hour", onlyMissing: bool = False, csvSep: str = ",", show: bool = True) -> pd.DataFrame:
        """
        This method returns last history candles of the current instrument defined by `ticker` or `figi` (FIGI id).

        History returned between two given dates: `start` and `end`. Minimum requested date in the past is `1970-01-01`.
        Warning! Broker server used ISO UTC time by default.

        If `historyFile` is not `None` then method save history to file, otherwise return only Pandas DataFrame.
        Also, `historyFile` used to update history with `onlyMissing` parameter.

        See also: `LoadHistory()` and `ShowHistoryChart()` methods.

        :param start: see docstring in `TradeRoutines.GetDatesAsString()` method.
        :param end: see docstring in `TradeRoutines.GetDatesAsString()` method.
        :param interval: this is a candle interval. Current available values are `"1min"`, `"5min"`, `"15min"`,
                         `"hour"`, `"day"`. Default: `"hour"`.
        :param onlyMissing: if `True` then add only last missing candles, do not request all history length from `start`.
                            False by default. Warning! History appends only from last candle to current time
                            with always update last candle!
        :param csvSep: separator if csv-file is used, `,` by default.
        :param show: if `True` then also prints Pandas DataFrame to the console.
        :return: Pandas DataFrame with prices history. Headers of columns are defined by default:
                 `["date", "time", "open", "high", "low", "close", "volume"]`.
        """
        strStartDate, strEndDate = GetDatesAsString(start, end, userFormat=TKS_DATE_FORMAT, outputFormat=TKS_DATE_TIME_FORMAT)  # example: ("2020-01-01T00:00:00Z", "2022-12-31T23:59:59Z")
        headers = ["date", "time", "open", "high", "low", "close", "volume"]  # sequence and names of column headers
        history = None  # empty pandas object for history

        if interval not in TKS_CANDLE_INTERVALS.keys():
            uLogger.error("Interval parameter must be string with current available values: `1min`, `5min`, `15min`, `hour` and `day`.")
            raise Exception("Incorrect value")

        if not (self._ticker or self._figi):
            uLogger.error("Ticker or FIGI must be defined!")
            raise Exception("Ticker or FIGI required")

        if self._ticker and not self._figi:
            instrumentByTicker = self.SearchByTicker(requestPrice=False)
            self._figi = instrumentByTicker["figi"] if instrumentByTicker else ""

        if self._figi and not self._ticker:
            instrumentByFIGI = self.SearchByFIGI(requestPrice=False)
            self._ticker = instrumentByFIGI["ticker"] if instrumentByFIGI else ""

        dtStart = datetime.strptime(strStartDate, TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc())  # datetime object from start time string
        dtEnd = datetime.strptime(strEndDate, TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc())  # datetime object from end time string
        if interval.lower() != "day":
            dtEnd += timedelta(seconds=1)  # adds 1 sec for requests, because day end returned by `TradeRoutines.GetDatesAsString()` is 23:59:59

        delta = dtEnd - dtStart  # current UTC time minus last time in file
        deltaMinutes = delta.days * 1440 + delta.seconds // 60  # minutes between start and end dates

        # calculate history length in candles:
        length = deltaMinutes // TKS_CANDLE_INTERVALS[interval][1]
        if deltaMinutes % TKS_CANDLE_INTERVALS[interval][1] > 0:
            length += 1  # to avoid fraction time

        # calculate data blocks count:
        blocks = 1 if length < TKS_CANDLE_INTERVALS[interval][2] else 1 + length // TKS_CANDLE_INTERVALS[interval][2]

        if show:
            uLogger.debug("Requesting history candlesticks, ticker: [{}], FIGI: [{}]. Wait, please...".format(self._ticker, self._figi))
            if self.moreDebug:
                uLogger.debug("Original requested time period in local time: from [{}] to [{}]".format(start, end))
                uLogger.debug("Requested time period is about from [{}] UTC to [{}] UTC".format(strStartDate, strEndDate))
                uLogger.debug("Calculated history length: [{}], interval: [{}]".format(length, interval))
                uLogger.debug("Data blocks, count: [{}], max candles in block: [{}]".format(blocks, TKS_CANDLE_INTERVALS[interval][2]))

        tempOld = None  # pandas object for old history, if --only-missing key present
        lastTime = None  # datetime object of last old candle in file

        if onlyMissing and self.historyFile is not None and self.historyFile and os.path.exists(self.historyFile):
            try:
                if self.moreDebug and show:
                    uLogger.debug("--only-missing key present, add only last missing candles...")
                    uLogger.debug("History file will be updated: [{}]".format(os.path.abspath(self.historyFile)))

                tempOld = pd.read_csv(self.historyFile, sep=csvSep, header=None, names=headers)

                tempOld["date"] = pd.to_datetime(tempOld["date"])  # load date "as is"
                tempOld["date"] = tempOld["date"].dt.strftime("%Y.%m.%d")  # convert date to string
                tempOld["time"] = pd.to_datetime(tempOld["time"])  # load time "as is"
                tempOld["time"] = tempOld["time"].dt.strftime("%H:%M")  # convert time to string

                # get last datetime object from last string in file or minus 1 delta if file is empty:
                if len(tempOld) > 0:
                    lastTime = datetime.strptime(tempOld.date.iloc[-1] + " " + tempOld.time.iloc[-1], "%Y.%m.%d %H:%M").replace(tzinfo=tzutc())

                else:
                    lastTime = dtEnd - timedelta(days=1)  # history file is empty, so last date set at -1 day

                tempOld = tempOld[:-1]  # always remove last old candle because it may be incompletely at the current time

            except Exception as e:
                uLogger.debug(tb.format_exc())
                uLogger.warning("An issue occurred when loading from file [{}], maybe incorrect format? File will be rewritten. Message: {}".format(os.path.abspath(self.historyFile), e))

        responseJSONs = []  # raw history blocks of data

        blockEnd = dtEnd
        for item in range(blocks):
            tail = length % TKS_CANDLE_INTERVALS[interval][2] if item + 1 == blocks else TKS_CANDLE_INTERVALS[interval][2]
            blockStart = blockEnd - timedelta(minutes=TKS_CANDLE_INTERVALS[interval][1] * tail)

            if self.moreDebug and show:
                uLogger.debug("[Block #{}/{}] time period: [{}] UTC - [{}] UTC".format(
                    item + 1, blocks, blockStart.strftime(TKS_DATE_TIME_FORMAT), blockEnd.strftime(TKS_DATE_TIME_FORMAT),
                ))

            if blockStart == blockEnd:
                if self.moreDebug and show:
                    uLogger.debug("Skipped this zero-length block...")

            else:
                # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetCandles
                historyURL = self.server + r"/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"
                self.body = str({
                    "figi": self._figi,
                    "from": blockStart.strftime(TKS_DATE_TIME_FORMAT),
                    "to": blockEnd.strftime(TKS_DATE_TIME_FORMAT),
                    "interval": TKS_CANDLE_INTERVALS[interval][0]
                })
                responseJSON = self.SendAPIRequest(historyURL, reqType="POST")

                if "code" in responseJSON.keys():
                    uLogger.debug("An issue occurred and block #{}/{} is empty".format(item + 1, blocks))

                else:
                    if "candles" in responseJSON.keys():
                        if start is not None and (start.lower() == "yesterday" or start == end) and interval == "day" and len(responseJSON["candles"]) > 1:
                            responseJSON["candles"] = responseJSON["candles"][:-1]  # removes last candle for "yesterday" request

                        responseJSONs = responseJSON["candles"] + responseJSONs  # add more old history behind newest dates

                    else:
                        if self.moreDebug and show:
                            uLogger.debug("`candles` key not in responseJSON keys! Block #{}/{} is empty".format(item + 1, blocks))

            blockEnd = blockStart

        if responseJSONs:
            tempHistory = pd.DataFrame(
                data={
                    "date": [pd.to_datetime(item["time"]).astimezone(tzutc()) for item in responseJSONs],
                    "time": [pd.to_datetime(item["time"]).astimezone(tzutc()) for item in responseJSONs],
                    "open": [NanoToFloat(item["open"]["units"], item["open"]["nano"]) for item in responseJSONs],
                    "high": [NanoToFloat(item["high"]["units"], item["high"]["nano"]) for item in responseJSONs],
                    "low": [NanoToFloat(item["low"]["units"], item["low"]["nano"]) for item in responseJSONs],
                    "close": [NanoToFloat(item["close"]["units"], item["close"]["nano"]) for item in responseJSONs],
                    "volume": [int(item["volume"]) for item in responseJSONs],
                },
                index=range(len(responseJSONs)),
                columns=["date", "time", "open", "high", "low", "close", "volume"],
            )
            tempHistory["date"] = tempHistory["date"].dt.strftime("%Y.%m.%d")
            tempHistory["time"] = tempHistory["time"].dt.strftime("%H:%M")

            # append only newest candles to old history if --only-missing key present:
            if onlyMissing and tempOld is not None and lastTime is not None:
                index = 0  # find start index in tempHistory data:

                for i, item in tempHistory.iterrows():
                    curTime = datetime.strptime(item["date"] + " " + item["time"], "%Y.%m.%d %H:%M").replace(tzinfo=tzutc())

                    if curTime == lastTime:
                        if show:
                            uLogger.debug("History will be updated starting from the date: [{}]".format(curTime.strftime(TKS_PRINT_DATE_TIME_FORMAT)))

                        index = i
                        break

                history = pd.concat([tempOld, tempHistory[index:]], ignore_index=True)

            else:
                history = tempHistory  # if no `--only-missing` key then load full data from server

            if self.moreDebug and show:
                uLogger.debug("Last 3 rows of received history:\n{}".format(pd.DataFrame.to_string(history[["date", "time", "open", "high", "low", "close", "volume"]][-3:], max_cols=20, index=False)))

        if show:
            if history is not None and not history.empty:
                printCount = len(responseJSONs)  # candles to show in console
                uLogger.info("Here's requested history between [{}] UTC and [{}] UTC, not-empty candles count: [{}]\n{}".format(
                    strStartDate.replace("T", " ").replace("Z", ""), strEndDate.replace("T", " ").replace("Z", ""), len(history[-printCount:]),
                    pd.DataFrame.to_string(history[["date", "time", "open", "high", "low", "close", "volume"]][-printCount:], max_cols=20, index=False),
                ))

            else:
                uLogger.warning("Received an empty candles history!")

        if self.historyFile is not None:
            if history is not None and not history.empty:
                history.to_csv(self.historyFile, sep=csvSep, index=False, header=False)

                if show:
                    uLogger.info("Ticker [{}], FIGI [{}], tf: [{}], history saved: [{}]".format(self._ticker, self._figi, interval, os.path.abspath(self.historyFile)))

            else:
                if show:
                    uLogger.warning("Empty history received! File NOT updated: [{}]".format(os.path.abspath(self.historyFile)))

        else:
            if show:
                uLogger.debug("--output key is not defined. Parsed history file not saved to file, only Pandas DataFrame returns.")

        return history

    def LoadHistory(self, filePath: str, show: bool = True) -> pd.DataFrame:
        """
        Load candles history from csv-file and return Pandas DataFrame object.

        See also: `History()` and `ShowHistoryChart()` methods.

        :param filePath: path to csv-file to open.
        :param show: if `True` then also prints Pandas DataFrame to the console.
        :return: Pandas DataFrame with prices history. Headers of columns are defined by default:
                 `["date", "time", "open", "high", "low", "close", "volume"]`.
        """
        loadedHistory = None  # empty pandas object for history

        if show:
            uLogger.debug("Loading candles history with PriceGenerator module. Wait, please...")

        if os.path.exists(filePath):
            try:
                loadedHistory = self.priceModel.LoadFromFile(filePath)  # load data and get chain of candles as Pandas DataFrame

            except Exception as e:
                uLogger.debug(tb.format_exc())
                uLogger.warning("An issue occurred when loading from file [{}]! Maybe incorrect strings format? Check it, please. Message: {}".format(os.path.abspath(filePath), e))

            tfStr = self.priceModel.FormattedDelta(
                self.priceModel.timeframe,
                "{days} days {hours}h {minutes}m {seconds}s",
            ) if self.priceModel.timeframe >= timedelta(days=1) else self.priceModel.FormattedDelta(
                self.priceModel.timeframe,
                "{hours}h {minutes}m {seconds}s",
            )

            if show:
                if loadedHistory is not None and not loadedHistory.empty:
                    uLogger.info("Rows count loaded: [{}], detected timeframe of candles: [{}]. Showing some last rows:\n{}".format(
                        len(loadedHistory),
                        tfStr,
                        pd.DataFrame.to_string(loadedHistory[-10:], max_cols=20)),
                    )

                else:
                    uLogger.warning("It was loaded an empty history! Path: [{}]".format(os.path.abspath(filePath)))

        else:
            uLogger.error("File with candles history does not exist! Check the path: [{}]".format(filePath))

        return loadedHistory

    def ShowHistoryChart(self, candles: Union[str, pd.DataFrame] = None, interact: bool = True, openInBrowser: bool = False) -> None:
        """
        Render an HTML-file with interact or non-interact candlesticks chart. Candles may be path to the csv-file.

        Self variable `htmlHistoryFile` can be use as html-file name to save interaction or non-interaction chart.
        Default: `index.html` (both for interact and non-interact candlesticks chart).

        See also: `History()` and `LoadHistory()` methods.

        :param candles: string to csv-file with candles in OHLCV-model or like Pandas Dataframe object.
        :param interact: if True (default) then chain of candlesticks will render as interactive Bokeh chart.
                         See examples: https://github.com/Tim55667757/PriceGenerator#overriding-parameters
                         If False then chain of candlesticks will render as not interactive Google Candlestick chart.
                         See examples: https://github.com/Tim55667757/PriceGenerator#statistics-and-chart-on-a-simple-template
        :param openInBrowser: if True then immediately open chart in default browser, otherwise only path to
                              html-file prints to console. False by default, to avoid issues with `permissions denied` to html-file.
        """
        if isinstance(candles, str):
            self.priceModel.prices = self.LoadHistory(filePath=candles)  # load candles chain from file
            self.priceModel.ticker = os.path.basename(candles)  # use filename as ticker name in PriceGenerator

        elif isinstance(candles, pd.DataFrame):
            self.priceModel.prices = candles  # set candles chain from variable
            self.priceModel.ticker = self._ticker  # use current TKSBrokerAPI ticker as ticker name in PriceGenerator

            if "datetime" not in candles.columns:
                self.priceModel.prices["datetime"] = pd.to_datetime(candles.date + ' ' + candles.time, utc=True)  # PriceGenerator uses "datetime" column with date and time

        else:
            uLogger.error("`candles` variable must be path string to the csv-file with candles in OHLCV-model or like Pandas Dataframe object!")
            raise Exception("Incorrect value")

        self.priceModel.horizon = len(self.priceModel.prices)  # use length of candles data as horizon in PriceGenerator

        if interact:
            uLogger.debug("Rendering interactive candles chart. Wait, please...")

            self.priceModel.RenderBokeh(fileName=self.htmlHistoryFile, viewInBrowser=openInBrowser)

        else:
            uLogger.debug("Rendering non-interactive candles chart. Wait, please...")

            self.priceModel.RenderGoogle(fileName=self.htmlHistoryFile, viewInBrowser=openInBrowser)

        uLogger.info("Rendered candles chart: [{}]".format(os.path.abspath(self.htmlHistoryFile)))

    def Trade(self, operation: str, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        Universal method to create market order and make deal at the current price for current `accountId`. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will open stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` docstring. More simple methods than `Trade()` are `Buy()` and `Sell()`.

        :param operation: string "Buy" or "Sell".
        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, target price for stop-order with "TP" type. It used as take profit parameter `targetPrice` in `self.Order()`.
        :param sl: float > 0, target price for stop-order with "SL" type. It used as stop loss parameter `targetPrice` in `self.Order()`.
        :param expDate: string "Undefined" by default or local date in the future,
                        it is a string with format `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        if operation is None or not operation or operation not in ("Buy", "Sell"):
            uLogger.error("You must define operation type only one of them: `Buy` or `Sell`!")
            raise Exception("Incorrect value")

        if lots is None or lots < 1:
            uLogger.warning("You must define trade volume > 0: integer count of lots! For current operation lots reset to 1.")
            lots = 1

        if tp is None or tp < 0:
            tp = 0

        if sl is None or sl < 0:
            sl = 0

        if expDate is None or not expDate:
            expDate = "Undefined"

        if not (self._ticker or self._figi):
            uLogger.error("Ticker or FIGI must be defined!")
            raise Exception("Ticker or FIGI required")

        instrument = self.SearchByTicker(requestPrice=True) if self._ticker else self.SearchByFIGI(requestPrice=True)
        self._ticker = instrument["ticker"]
        self._figi = instrument["figi"]

        uLogger.debug("Opening [{}] market order: ticker [{}], FIGI [{}], lots [{}], TP [{:.4f}], SL [{:.4f}], expiration date of TP/SL orders [{}]. Wait, please...".format(operation, self._ticker, self._figi, lots, tp, sl, expDate))

        openTradeURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"
        self.body = str({
            "figi": self._figi,
            "quantity": str(lots),
            "direction": "ORDER_DIRECTION_BUY" if operation == "Buy" else "ORDER_DIRECTION_SELL",  # see: TKS_ORDER_DIRECTIONS
            "accountId": str(self.accountId),
            "orderType": "ORDER_TYPE_MARKET",  # see: TKS_ORDER_TYPES
        })
        response = self.SendAPIRequest(openTradeURL, reqType="POST")

        if "orderId" in response.keys():
            uLogger.info("[{}] market order [{}] was executed: ticker [{}], FIGI [{}], lots [{}]. Total order price: [{:.4f} {}] (with commission: [{:.2f} {}]). Average price of lot: [{:.2f} {}]".format(
                operation, response["orderId"],
                self._ticker, self._figi, lots,
                NanoToFloat(response["totalOrderAmount"]["units"], response["totalOrderAmount"]["nano"]), response["totalOrderAmount"]["currency"],
                NanoToFloat(response["initialCommission"]["units"], response["initialCommission"]["nano"]), response["initialCommission"]["currency"],
                NanoToFloat(response["executedOrderPrice"]["units"], response["executedOrderPrice"]["nano"]), response["executedOrderPrice"]["currency"],
            ))

            if tp > 0:
                self.Order(operation="Sell" if operation == "Buy" else "Buy", orderType="Stop", lots=lots, targetPrice=tp, limitPrice=tp, stopType="TP", expDate=expDate)

            if sl > 0:
                self.Order(operation="Sell" if operation == "Buy" else "Buy", orderType="Stop", lots=lots, targetPrice=sl, limitPrice=sl, stopType="SL", expDate=expDate)

        else:
            uLogger.warning("Not `oK` status received! Market order not executed. See full debug log and try again open order later.")

        return response

    def Buy(self, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        More simple method than `Trade()`. Create `Buy` market order and make deal at the current price. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will open stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` and `Trade()` docstrings.

        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, take profit price of stop-order.
        :param sl: float > 0, stop loss price of stop-order.
        :param expDate: it's a local date in the future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        return self.Trade(operation="Buy", lots=lots, tp=tp, sl=sl, expDate=expDate)

    def Sell(self, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        More simple method than `Trade()`. Create `Sell` market order and make deal at the current price. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will open stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` and `Trade()` docstrings.

        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, take profit price of stop-order.
        :param sl: float > 0, stop loss price of stop-order.
        :param expDate: it's a local date in the future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        return self.Trade(operation="Sell", lots=lots, tp=tp, sl=sl, expDate=expDate)

    def CloseTrades(self, instruments: list[str], portfolio: dict = None) -> None:
        """
        Close position of given instruments.

        :param instruments: list of instruments defined by tickers or FIGIs that must be closed.
        :param portfolio: pre-received dictionary with open trades, returned by `Overview()` method.
                         This avoids unnecessary downloading data from the server.
        """
        if instruments is None or not instruments:
            uLogger.error("List of tickers or FIGIs must be defined for using this method!")
            raise Exception("Ticker or FIGI required")

        if isinstance(instruments, str):
            instruments = [instruments]

        uniqueInstruments = self.GetUniqueFIGIs(instruments)
        if uniqueInstruments:
            if portfolio is None or not portfolio:
                portfolio = self.Overview(show=False)

            allOpened = [item["figi"] for iType in TKS_INSTRUMENTS for item in portfolio["stat"][iType]]
            uLogger.debug("All opened instruments by it's FIGI: {}".format(", ".join(allOpened)))

            for self._figi in uniqueInstruments:
                if self._figi not in allOpened:
                    uLogger.warning("Instrument with FIGI [{}] not in open positions list!".format(self._figi))
                    continue

                # search open trade info about instrument by ticker:
                instrument = {}
                for iType in TKS_INSTRUMENTS:
                    if instrument:
                        break

                    for item in portfolio["stat"][iType]:
                        if item["figi"] == self._figi:
                            instrument = item
                            break

                if instrument:
                    self._ticker = instrument["ticker"]
                    self._figi = instrument["figi"]

                    uLogger.debug("Closing trade of instrument: ticker [{}], FIGI[{}], lots [{}]{}. Wait, please...".format(
                        self._ticker,
                        self._figi,
                        int(instrument["volume"]),
                        ", blocked [{}]".format(instrument["blocked"]) if instrument["blocked"] > 0 else "",
                    ))

                    tradeLots = abs(instrument["lots"]) - instrument["blocked"]  # available volumes in lots for close operation

                    if tradeLots > 0:
                        if instrument["blocked"] > 0:
                            uLogger.warning("Just for your information: there are [{}] lots blocked for instrument [{}]! Available only [{}] lots to closing trade.".format(
                                instrument["blocked"],
                                self._ticker,
                                tradeLots,
                            ))

                        # if direction is "Long" then we need sell, if direction is "Short" then we need buy:
                        self.Trade(operation="Sell" if instrument["direction"] == "Long" else "Buy", lots=tradeLots)

                    else:
                        uLogger.warning("There are no available lots for instrument [{}] to closing trade at this moment! Try again later or cancel some orders.".format(self._ticker))

    def CloseAllTrades(self, iType: str, portfolio: dict = None) -> None:
        """
        Close all positions of given instruments with defined type.

        :param iType: type of the instruments that be closed, it must be one of supported types in TKS_INSTRUMENTS list.
        :param portfolio: pre-received dictionary with open trades, returned by `Overview()` method.
                         This avoids unnecessary downloading data from the server.
        """
        if iType not in TKS_INSTRUMENTS:
            uLogger.warning("Type of the instrument must be one of supported types: {}. Given: [{}]".format(", ".join(TKS_INSTRUMENTS), iType))

        else:
            if portfolio is None or not portfolio:
                portfolio = self.Overview(show=False)

            tickers = [item["ticker"] for item in portfolio["stat"][iType]]
            uLogger.debug("Instrument tickers with type [{}] that will be closed: {}".format(iType, tickers))

            if tickers and portfolio:
                self.CloseTrades(tickers, portfolio)

            else:
                uLogger.info("Instrument tickers with type [{}] not found, nothing to close.".format(iType))

    def Order(self, operation: str, orderType: str, lots: int, targetPrice: float, limitPrice: float = 0., stopType: str = "Limit", expDate: str = "Undefined") -> dict:
        """
        Universal method to create market or limit orders with all available parameters for current `accountId`.
        See more simple methods: `BuyLimit()`, `BuyStop()`, `SellLimit()`, `SellStop()`.

        If orderType is "Limit" then create pending limit-order below current price if operation is "Buy" and above
        current price if operation is "Sell". A limit order has no expiration date, it lasts until the end of the trading day.

        Warning! If you try to create limit-order above current price if "Buy" or below current price if "Sell"
        then broker immediately open market order as you can do simple --buy or --sell operations!

        If orderType is "Stop" then creates stop-order with any direction "Buy" or "Sell".
        When current price will go up or down to target price value then broker opens a limit order.
        Stop-order is opened with unlimited expiration date by default, or you can define expiration date with expDate parameter.

        Only one attempt without retries recommended for opens order, set `self.retry = 0`. If network issue occurred you can create new request.

        :param operation: string "Buy" or "Sell".
        :param orderType: string "Limit" or "Stop".
        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is open trade price for limit order.
        :param limitPrice: limit price >= 0. This parameter only makes sense for stop-order. If limitPrice = 0, then it set as targetPrice.
                           Broker will create limit-order with price equal to limitPrice, when current price goes to target price of stop-order.
        :param stopType: string "Limit" by default. This parameter only makes sense for stop-order. There are 3 stop-order types
                         "SL", "TP", "Limit" for "Stop loss", "Take profit" and "Stop limit" types accordingly.
                         Stop loss order always executed by market price.
        :param expDate: string "Undefined" by default or local date in the future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
                        This date is converting to UTC format for server. This parameter only makes sense for stop-order.
                        A limit order has no expiration date, it lasts until the end of the trading day.
        :return: JSON with response from broker server.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        if operation is None or not operation or operation not in ("Buy", "Sell"):
            uLogger.error("You must define operation type only one of them: `Buy` or `Sell`!")
            raise Exception("Incorrect value")

        if orderType is None or not orderType or orderType not in ("Limit", "Stop"):
            uLogger.error("You must define order type only one of them: `Limit` or `Stop`!")
            raise Exception("Incorrect value")

        if lots is None or lots < 1:
            uLogger.error("You must define trade volume > 0: integer count of lots!")
            raise Exception("Incorrect value")

        if targetPrice is None or targetPrice <= 0:
            uLogger.error("Target price for limit-order must be greater than 0!")
            raise Exception("Incorrect value")

        if limitPrice is None or limitPrice <= 0:
            limitPrice = targetPrice

        if stopType is None or not stopType or stopType not in ("SL", "TP", "Limit"):
            stopType = "Limit"

        if expDate is None or not expDate:
            expDate = "Undefined"

        if not (self._ticker or self._figi):
            uLogger.error("Tocker or FIGI must be defined!")
            raise Exception("Ticker or FIGI required")

        response = {}
        instrument = self.SearchByTicker(requestPrice=True) if self._ticker else self.SearchByFIGI(requestPrice=True)
        self._ticker = instrument["ticker"]
        self._figi = instrument["figi"]

        if orderType == "Limit":
            uLogger.debug(
                "Creating pending limit-order: ticker [{}], FIGI [{}], action [{}], lots [{}] and the target price [{:.2f} {}]. Wait, please...".format(
                    self._ticker, self._figi,
                    operation, lots, targetPrice, instrument["currency"],
                ))

            openOrderURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"
            self.body = str({
                "figi": self._figi,
                "quantity": str(lots),
                "price": FloatToNano(targetPrice),
                "direction": "ORDER_DIRECTION_BUY" if operation == "Buy" else "ORDER_DIRECTION_SELL",  # see: TKS_ORDER_DIRECTIONS
                "accountId": str(self.accountId),
                "orderType": "ORDER_TYPE_LIMIT",  # see: TKS_ORDER_TYPES
            })
            response = self.SendAPIRequest(openOrderURL, reqType="POST")

            if "orderId" in response.keys():
                uLogger.info(
                    "Limit-order [{}] was created: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{} {}]".format(
                        response["orderId"], self._ticker, self._figi, operation, lots,
                        "{:.4f}".format(targetPrice).rstrip("0").rstrip("."), instrument["currency"],
                    ))

                if "lastPrice" in instrument["currentPrice"].keys() and instrument["currentPrice"]["lastPrice"]:
                    if operation == "Buy" and targetPrice > instrument["currentPrice"]["lastPrice"]:
                        uLogger.warning("Your order was executed as a market order, not as a limit order! Comment: because your target price [{:.2f} {}] was higher than current price [{:.2f} {}] broker immediately opened `Buy` market order, such as if you did simple `--buy` operation.".format(
                            targetPrice, instrument["currency"],
                            instrument["currentPrice"]["lastPrice"], instrument["currency"],
                        ))

                    if operation == "Sell" and targetPrice < instrument["currentPrice"]["lastPrice"]:
                        uLogger.warning("Your order was executed as a market order, not as a limit order! Comment: because your target price [{:.2f} {}] was lower than current price [{:.2f} {}] broker immediately opened `Sell` market order, such as if you did simple `--sell` operation.".format(
                            targetPrice, instrument["currency"],
                            instrument["currentPrice"]["lastPrice"], instrument["currency"],
                        ))

            else:
                uLogger.warning("Not `oK` status received! Limit order not opened. See full debug log and try again open order later.")

        if orderType == "Stop":
            uLogger.debug(
                "Creating stop-order: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{:.2f} {}], limit price [{:.2f} {}], stop-order type [{}] and local expiration date [{}]. Wait, please...".format(
                    self._ticker, self._figi,
                    operation, lots,
                    targetPrice, instrument["currency"],
                    limitPrice, instrument["currency"],
                    stopType, expDate,
                ))

            openOrderURL = self.server + r"/tinkoff.public.invest.api.contract.v1.StopOrdersService/PostStopOrder"
            expDateUTC = "" if expDate == "Undefined" else datetime.strptime(expDate, TKS_PRINT_DATE_TIME_FORMAT).replace(tzinfo=tzlocal()).astimezone(tzutc()).strftime(TKS_DATE_TIME_FORMAT_EXT)
            stopOrderType = "STOP_ORDER_TYPE_STOP_LOSS" if stopType == "SL" else "STOP_ORDER_TYPE_TAKE_PROFIT" if stopType == "TP" else "STOP_ORDER_TYPE_STOP_LIMIT"

            body = {
                "figi": self._figi,
                "quantity": str(lots),
                "price": FloatToNano(limitPrice),
                "stopPrice": FloatToNano(targetPrice),
                "direction": "STOP_ORDER_DIRECTION_BUY" if operation == "Buy" else "STOP_ORDER_DIRECTION_SELL",  # see: TKS_STOP_ORDER_DIRECTIONS
                "accountId": str(self.accountId),
                "expirationType": "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE" if expDateUTC else "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL",  # see: TKS_STOP_ORDER_EXPIRATION_TYPES
                "stopOrderType": stopOrderType,  # see: TKS_STOP_ORDER_TYPES
            }

            if expDateUTC:
                body["expireDate"] = expDateUTC

            self.body = str(body)
            response = self.SendAPIRequest(openOrderURL, reqType="POST")

            if "stopOrderId" in response.keys():
                uLogger.info(
                    "Stop-order [{}] was created: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{} {}], limit price [{} {}], stop-order type [{}] and expiration date [{} UTC]".format(
                        response["stopOrderId"], self._ticker, self._figi, operation, lots,
                        "{:.4f}".format(targetPrice).rstrip("0").rstrip("."), instrument["currency"],
                        "{:.4f}".format(limitPrice).rstrip("0").rstrip("."), instrument["currency"],
                        TKS_STOP_ORDER_TYPES[stopOrderType],
                        datetime.strptime(expDateUTC, TKS_DATE_TIME_FORMAT_EXT).replace(tzinfo=tzutc()).astimezone(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT) if expDateUTC else TKS_STOP_ORDER_EXPIRATION_TYPES["STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED"],
                    ))

                if "lastPrice" in instrument["currentPrice"].keys() and instrument["currentPrice"]["lastPrice"]:
                    if operation == "Buy" and targetPrice < instrument["currentPrice"]["lastPrice"] and stopType != "TP":
                        uLogger.warning("The broker will cancel this order after some time. Comment: you placed the wrong stop order because the target buy price [{} {}] is lower than the current price [{} {}]. Also try to set up order type as `TP` if you want to place stop order at that price.".format(
                            "{:.4f}".format(targetPrice).rstrip("0").rstrip("."), instrument["currency"],
                            "{:.4f}".format(instrument["currentPrice"]["lastPrice"]).rstrip("0").rstrip("."), instrument["currency"],
                        ))

                    if operation == "Sell" and targetPrice > instrument["currentPrice"]["lastPrice"] and stopType != "TP":
                        uLogger.warning("The broker will cancel this order after some time. Comment: you placed the wrong stop order because the target sell price [{} {}] is higher than the current price [{} {}]. Also try to set up order type as `TP` if you want to place stop order at that price.".format(
                            "{:.4f}".format(targetPrice).rstrip("0").rstrip("."), instrument["currency"],
                            "{:.4f}".format(instrument["currentPrice"]["lastPrice"]).rstrip("0").rstrip("."), instrument["currency"],
                        ))

            else:
                uLogger.warning("Not `oK` status received! Stop order not opened. See full debug log and try again open order later.")

        return response

    def BuyLimit(self, lots: int, targetPrice: float) -> dict:
        """
        Create pending `Buy` limit-order (below current price). You must specify only 2 parameters:
        `lots` and `target price` to open buy limit-order. If you try to create buy limit-order above current price then
        broker immediately open `Buy` market order, such as if you do simple `--buy` operation!
        See also: `Order()` docstring.

        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is open trade price for limit order.
        :return: JSON with response from broker server.
        """
        return self.Order(operation="Buy", orderType="Limit", lots=lots, targetPrice=targetPrice)

    def BuyStop(self, lots: int, targetPrice: float, limitPrice: float = 0., stopType: str = "Limit", expDate: str = "Undefined") -> dict:
        """
        Create `Buy` stop-order. You must specify at least 2 parameters: `lots` `target price` to open buy stop-order.
        In additional you can specify 3 parameters for buy stop-order: `limit price` >=0, `stop type` = Limit|SL|TP,
        `expiration date` = Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`. When current price will go up or down to
        target price value then broker opens a limit order. See also: `Order()` docstring.

        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is trigger price for buy stop-order.
        :param limitPrice: limit price >= 0 (limitPrice = targetPrice if limitPrice is 0). Broker will create limit-order
                           with price equal to limitPrice, when current price goes to target price of buy stop-order.
        :param stopType: string "Limit" by default. There are 3 stop-order types "SL", "TP", "Limit"
                         for "Stop loss", "Take profit" and "Stop limit" types accordingly.
        :param expDate: string "Undefined" by default or local date in the future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
                        This date is converting to UTC format for server.
        :return: JSON with response from broker server.
        """
        return self.Order(operation="Buy", orderType="Stop", lots=lots, targetPrice=targetPrice, limitPrice=limitPrice, stopType=stopType, expDate=expDate)

    def SellLimit(self, lots: int, targetPrice: float) -> dict:
        """
        Create pending `Sell` limit-order (above current price). You must specify only 2 parameters:
        `lots` and `target price` to open sell limit-order. If you try to create sell limit-order below current price then
        broker immediately open `Sell` market order, such as if you do simple `--sell` operation!
        See also: `Order()` docstring.

        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is open trade price for limit order.
        :return: JSON with response from broker server.
        """
        return self.Order(operation="Sell", orderType="Limit", lots=lots, targetPrice=targetPrice)

    def SellStop(self, lots: int, targetPrice: float, limitPrice: float = 0., stopType: str = "Limit", expDate: str = "Undefined") -> dict:
        """
        Create `Sell` stop-order. You must specify at least 2 parameters: `lots` `target price` to open sell stop-order.
        In addition, you can specify 3 parameters in sell stop-order: `limit price` >=0, `stop type` = Limit|SL|TP,
        `expiration date` = Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`. When current price will go up or down to
        target price value then broker opens a limit order. See also: `Order()` docstring.

        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is trigger price in sell stop-order.
        :param limitPrice: limit price >= 0 (limitPrice = targetPrice if limitPrice is 0). Broker will create limit-order
                           with price equal to limitPrice, when current price goes to target price of sell stop-order.
        :param stopType: string "Limit" by default. There are 3 stop-order types "SL", "TP", "Limit"
                         for "Stop loss", "Take profit" and "Stop limit" types accordingly.
        :param expDate: string "Undefined" by default or local date in the future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
                        This date is converting to UTC format for server.
        :return: JSON with response from broker server.
        """
        return self.Order(operation="Sell", orderType="Stop", lots=lots, targetPrice=targetPrice, limitPrice=limitPrice, stopType=stopType, expDate=expDate)

    def CloseOrders(self, orderIDs: list, allOrdersIDs: list = None, allStopOrdersIDs: list = None) -> None:
        """
        Cancel order or list of orders by its `orderId` or `stopOrderId` for current `accountId`.

        :param orderIDs: list of integers with `orderId` or `stopOrderId`.
        :param allOrdersIDs: pre-received lists of all active pending limit orders.
                             This avoids unnecessary downloading data from the server.
        :param allStopOrdersIDs: pre-received lists of all active stop orders.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        if orderIDs:
            if allOrdersIDs is None:
                rawOrders = self.RequestPendingOrders()
                allOrdersIDs = [item["orderId"] for item in rawOrders]  # all pending limit orders ID

            if allStopOrdersIDs is None:
                rawStopOrders = self.RequestStopOrders()
                allStopOrdersIDs = [item["stopOrderId"] for item in rawStopOrders]  # all stop orders ID

            for orderID in orderIDs:
                idInPendingOrders = orderID in allOrdersIDs
                idInStopOrders = orderID in allStopOrdersIDs

                if not (idInPendingOrders or idInStopOrders):
                    uLogger.warning("Order not found by ID: [{}]. Maybe cancelled already? Check it with `--overview` key.".format(orderID))
                    continue

                else:
                    if idInPendingOrders:
                        uLogger.debug("Cancelling pending order with ID: [{}]. Wait, please...".format(orderID))

                        # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/OrdersService/OrdersService_CancelOrder
                        self.body = str({"accountId": self.accountId, "orderId": orderID})
                        closeURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/CancelOrder"
                        responseJSON = self.SendAPIRequest(closeURL, reqType="POST")

                        if responseJSON and "time" in responseJSON.keys() and responseJSON["time"]:
                            if self.moreDebug:
                                uLogger.debug("Success time marker received from server: [{}] (UTC)".format(responseJSON["time"]))

                            uLogger.info("Pending order with ID [{}] successfully cancel".format(orderID))

                        else:
                            uLogger.warning("Unknown issue occurred when cancelling pending order with ID: [{}]. Check ID and try again.".format(orderID))

                    elif idInStopOrders:
                        uLogger.debug("Cancelling stop order with ID: [{}]. Wait, please...".format(orderID))

                        # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/StopOrdersService/StopOrdersService_CancelStopOrder
                        self.body = str({"accountId": self.accountId, "stopOrderId": orderID})
                        closeURL = self.server + r"/tinkoff.public.invest.api.contract.v1.StopOrdersService/CancelStopOrder"
                        responseJSON = self.SendAPIRequest(closeURL, reqType="POST")

                        if responseJSON and "time" in responseJSON.keys() and responseJSON["time"]:
                            if self.moreDebug:
                                uLogger.debug("Success time marker received from server: [{}] (UTC)".format(responseJSON["time"]))

                            uLogger.info("Stop order with ID [{}] successfully cancel".format(orderID))

                        else:
                            uLogger.warning("Unknown issue occurred when cancelling stop order with ID: [{}]. Check ID and try again.".format(orderID))

                    else:
                        continue

    def CloseAllOrders(self) -> None:
        """
        Gets a list of open pending and stop orders and cancel it all.
        """
        rawOrders = self.RequestPendingOrders()
        allOrdersIDs = [item["orderId"] for item in rawOrders]  # all pending limit orders ID
        lenOrders = len(allOrdersIDs)

        rawStopOrders = self.RequestStopOrders()
        allStopOrdersIDs = [item["stopOrderId"] for item in rawStopOrders]  # all stop orders ID
        lenSOrders = len(allStopOrdersIDs)

        if lenOrders > 0 or lenSOrders > 0:
            uLogger.info("Found: [{}] opened pending and [{}] stop orders. Let's trying to cancel it all. Wait, please...".format(lenOrders, lenSOrders))

            self.CloseOrders(allOrdersIDs + allStopOrdersIDs, allOrdersIDs, allStopOrdersIDs)

        else:
            uLogger.info("Orders not found, nothing to cancel.")

    def CloseAll(self, *args) -> None:
        """
        Close all available (not blocked) opened trades and orders.

        Also, you can select one or more keywords case-insensitive:
        `orders`, `shares`, `bonds`, `etfs` and `futures` from `TKS_INSTRUMENTS` enum to specify trades type.

        Currency positions you must close manually using buy or sell operations, `CloseTrades()` or `CloseAllTrades()` methods.
        """
        overview = self.Overview(show=False)  # get all open trades info

        if len(args) == 0:
            uLogger.debug("Closing all available (not blocked) opened trades and orders. Currency positions you must closes manually using buy or sell operations! Wait, please...")
            self.CloseAllOrders()  # close all pending and stop orders

            for iType in TKS_INSTRUMENTS:
                if iType != "Currencies":
                    self.CloseAllTrades(iType, overview)  # close all positions of instruments with same type without currencies

        else:
            uLogger.debug("Closing all available {}. Currency positions you must closes manually using buy or sell operations! Wait, please...".format(list(args)))
            lowerArgs = [x.lower() for x in args]

            if "orders" in lowerArgs:
                self.CloseAllOrders()  # close all pending and stop orders

            for iType in TKS_INSTRUMENTS:
                if iType.lower() in lowerArgs and iType != "Currencies":
                    self.CloseAllTrades(iType, overview)  # close all positions of instruments with same type without currencies

    def CloseAllByTicker(self, instrument: str) -> None:
        """
        Close all available (not blocked) opened trades and orders for one instrument defined by its ticker.

        This method searches opened trade and orders of instrument throw all portfolio and then use
        `CloseTrades()` and `CloseOrders()` methods to close trade and cancel all orders for that instrument.

        See also: `IsInLimitOrders()`, `GetLimitOrderIDs()`, `IsInStopOrders()`, `GetStopOrderIDs()`, `CloseTrades()` and `CloseOrders()`.

        :param instrument: string with ticker.
        """
        if instrument is None or not instrument:
            uLogger.error("Ticker name must be defined for using this method!")
            raise Exception("Ticker required")

        overview = self.Overview(show=False)  # get user portfolio with all open trades info

        self._ticker = instrument  # try to set instrument as ticker
        self._figi = ""

        limitAll = [item["orderID"] for item in overview["stat"]["orders"]]  # list of all pending limit order IDs
        stopAll = [item["orderID"] for item in overview["stat"]["stopOrders"]]  # list of all stop order IDs

        if limitAll and self.IsInLimitOrders(portfolio=overview):
            uLogger.debug("Closing all opened pending limit orders for the instrument with ticker [{}]. Wait, please...")
            self.CloseOrders(orderIDs=self.GetLimitOrderIDs(portfolio=overview), allOrdersIDs=limitAll, allStopOrdersIDs=stopAll)

        if stopAll and self.IsInStopOrders(portfolio=overview):
            uLogger.debug("Closing all opened stop orders for the instrument with ticker [{}]. Wait, please...")
            self.CloseOrders(orderIDs=self.GetStopOrderIDs(portfolio=overview), allOrdersIDs=limitAll, allStopOrdersIDs=stopAll)

        if self.IsInPortfolio(portfolio=overview):
            uLogger.debug("Closing all available (not blocked) opened trade for the instrument with ticker [{}]. Wait, please...")
            self.CloseTrades(instruments=[instrument], portfolio=overview)

    def CloseAllByFIGI(self, instrument: str) -> None:
        """
        Close all available (not blocked) opened trades and orders for one instrument defined by its FIGI id.

        This method searches opened trade and orders of instrument throw all portfolio and then use
        `CloseTrades()` and `CloseOrders()` methods to close trade and cancel all orders for that instrument.

        See also: `IsInLimitOrders()`, `GetLimitOrderIDs()`, `IsInStopOrders()`, `GetStopOrderIDs()`, `CloseTrades()` and `CloseOrders()`.

        :param instrument: string with FIGI id.
        """
        if instrument is None or not instrument:
            uLogger.error("FIGI id must be defined for using this method!")
            raise Exception("FIGI required")

        overview = self.Overview(show=False)  # get user portfolio with all open trades info

        self._ticker = ""
        self._figi = instrument  # try to set instrument as FIGI id

        limitAll = [item["orderID"] for item in overview["stat"]["orders"]]  # list of all pending limit order IDs
        stopAll = [item["orderID"] for item in overview["stat"]["stopOrders"]]  # list of all stop order IDs

        if limitAll and self.IsInLimitOrders(portfolio=overview):
            uLogger.debug("Closing all opened pending limit orders for the instrument with FIGI [{}]. Wait, please...")
            self.CloseOrders(orderIDs=self.GetLimitOrderIDs(portfolio=overview), allOrdersIDs=limitAll, allStopOrdersIDs=stopAll)

        if stopAll and self.IsInStopOrders(portfolio=overview):
            uLogger.debug("Closing all opened stop orders for the instrument with FIGI [{}]. Wait, please...")
            self.CloseOrders(orderIDs=self.GetStopOrderIDs(portfolio=overview), allOrdersIDs=limitAll, allStopOrdersIDs=stopAll)

        if self.IsInPortfolio(portfolio=overview):
            uLogger.debug("Closing all available (not blocked) opened trade for the instrument with FIGI [{}]. Wait, please...")
            self.CloseTrades(instruments=[instrument], portfolio=overview)

    @staticmethod
    def ParseOrderParameters(operation, **inputParameters):
        """
        Parse input dictionary of strings with order parameters and return dictionary with parameters to open all orders.

        :param operation: string "Buy" or "Sell".
        :param inputParameters: this is dict of strings that looks like this
               `{"lots": "L_int,...", "prices": "P_float,..."}` where
               "lots" key: one or more lot values (integer numbers) to open with every limit-order
               "prices" key: one or more prices to open limit-orders
               Counts of values in lots and prices lists must be equals!
        :return: list of dictionaries with all lots and prices to open orders that looks like this `[{"lot": lots_1, "price": price_1}, {...}, ...]`
        """
        # TODO: update order grid work with api v2
        pass
        # uLogger.debug("Input parameters: {}".format(inputParameters))
        #
        # if operation is None or not operation or operation not in ("Buy", "Sell"):
        #     uLogger.error("You must define operation type: 'Buy' or 'Sell'!")
        #     raise Exception("Incorrect value")
        #
        # if "l" in inputParameters.keys():
        #     inputParameters["lots"] = inputParameters.pop("l")
        #
        # if "p" in inputParameters.keys():
        #     inputParameters["prices"] = inputParameters.pop("p")
        #
        # if "lots" not in inputParameters.keys() or "prices" not in inputParameters.keys():
        #     uLogger.error("Both of 'lots' and 'prices' keys must be defined to open grid orders!")
        #     raise Exception("Incorrect value")
        #
        # lots = [int(item.strip()) for item in inputParameters["lots"].split(",")]
        # prices = [float(item.strip()) for item in inputParameters["prices"].split(",")]
        #
        # if len(lots) != len(prices):
        #     uLogger.error("'lots' and 'prices' lists must have equal length of values!")
        #     raise Exception("Incorrect value")
        #
        # uLogger.debug("Extracted parameters for orders:")
        # uLogger.debug("lots = {}".format(lots))
        # uLogger.debug("prices = {}".format(prices))
        #
        # # list of dictionaries with order's parameters: [{"lot": lots_1, "price": price_1}, {...}, ...]
        # result = [{"lot": lots[item], "price": prices[item]} for item in range(len(prices))]
        # uLogger.debug("Order parameters: {}".format(result))
        #
        # return result

    def IsInPortfolio(self, portfolio: dict = None) -> bool:
        """
        Checks if instrument is in the user's portfolio. Instrument must be defined by `ticker` (highly priority) or `figi`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: `True` if portfolio contains open position with given instrument, `False` otherwise.
        """
        result = False
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] throw opened positions list...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in open positions".format(self._ticker)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["ticker"] == self._ticker:
                        result = True
                        msg = "Instrument with ticker [{}] is present in open positions".format(self._ticker)
                        break

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throw opened positions list...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in open positions".format(self._figi)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["figi"] == self._figi:
                        result = True
                        msg = "Instrument with FIGI [{}] is present in open positions".format(self._figi)
                        break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def GetInstrumentFromPortfolio(self, portfolio: dict = None) -> dict:
        """
        Returns instrument from the user's portfolio if it presents there.
        Instrument must be defined by `ticker` (highly priority) or `figi`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: dict with instrument if portfolio contains open position with this instrument, `None` otherwise.
        """
        result = None
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] in opened positions...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in open positions".format(self._ticker)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["ticker"] == self._ticker:
                        result = instrument
                        msg = "Instrument with ticker [{}] and FIGI [{}] is present in open positions".format(self._ticker, instrument["figi"])
                        break

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throwout opened positions...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in open positions".format(self._figi)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["figi"] == self._figi:
                        result = instrument
                        msg = "Instrument with ticker [{}] and FIGI [{}] is present in open positions".format(instrument["ticker"], self._figi)
                        break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def IsInLimitOrders(self, portfolio: dict = None) -> bool:
        """
        Checks if instrument is in the limit orders list. Instrument must be defined by `ticker` (highly priority) or `figi`.

        See also: `CloseAllByTicker()` and `CloseAllByFIGI()`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: `True` if limit orders list contains some limit orders for the instrument, `False` otherwise.
        """
        result = False
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] throw opened pending limit orders list...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in opened pending limit orders list".format(self._ticker)

            for instrument in portfolio["stat"]["orders"]:
                if instrument["ticker"] == self._ticker:
                    result = True
                    msg = "Instrument with ticker [{}] is present in limit orders list".format(self._ticker)
                    break

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throw opened pending limit orders list...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in opened pending limit orders list".format(self._figi)

            for instrument in portfolio["stat"]["orders"]:
                if instrument["figi"] == self._figi:
                    result = True
                    msg = "Instrument with FIGI [{}] is present in opened pending limit orders list".format(self._figi)
                    break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def GetLimitOrderIDs(self, portfolio: dict = None) -> list[str]:
        """
        Returns list with all `orderID`s of opened pending limit orders for the instrument.
        Instrument must be defined by `ticker` (highly priority) or `figi`.

        See also: `CloseAllByTicker()` and `CloseAllByFIGI()`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: list with `orderID`s of limit orders.
        """
        result = []
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] throw opened pending limit orders list...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in opened pending limit orders list".format(self._ticker)

            for instrument in portfolio["stat"]["orders"]:
                if instrument["ticker"] == self._ticker:
                    result.append(instrument["orderID"])

            if result:
                msg = "Instrument with ticker [{}] is present in limit orders list".format(self._ticker)

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throw opened pending limit orders list...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in opened pending limit orders list".format(self._figi)

            for instrument in portfolio["stat"]["orders"]:
                if instrument["figi"] == self._figi:
                    result.append(instrument["orderID"])

            if result:
                msg = "Instrument with FIGI [{}] is present in opened pending limit orders list".format(self._figi)

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def IsInStopOrders(self, portfolio: dict = None) -> bool:
        """
        Checks if instrument is in the stop orders list. Instrument must be defined by `ticker` (highly priority) or `figi`.

        See also: `CloseAllByTicker()` and `CloseAllByFIGI()`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: `True` if stop orders list contains some stop orders for the instrument, `False` otherwise.
        """
        result = False
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] throw opened stop orders list...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in opened stop orders list".format(self._ticker)

            for instrument in portfolio["stat"]["stopOrders"]:
                if instrument["ticker"] == self._ticker:
                    result = True
                    msg = "Instrument with ticker [{}] is present in stop orders list".format(self._ticker)
                    break

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throw opened stop orders list...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in opened stop orders list".format(self._figi)

            for instrument in portfolio["stat"]["stopOrders"]:
                if instrument["figi"] == self._figi:
                    result = True
                    msg = "Instrument with FIGI [{}] is present in opened stop orders list".format(self._figi)
                    break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def GetStopOrderIDs(self, portfolio: dict = None) -> list[str]:
        """
        Returns list with all `orderID`s of opened stop orders for the instrument.
        Instrument must be defined by `ticker` (highly priority) or `figi`.

        See also: `CloseAllByTicker()` and `CloseAllByFIGI()`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: list with `orderID`s of stop orders.
        """
        result = []
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(show=False)

        if self._ticker:
            uLogger.debug("Searching instrument with ticker [{}] throw opened stop orders list...".format(self._ticker))
            msg = "Instrument with ticker [{}] is not present in opened stop orders list".format(self._ticker)

            for instrument in portfolio["stat"]["stopOrders"]:
                if instrument["ticker"] == self._ticker:
                    result.append(instrument["orderID"])

            if result:
                msg = "Instrument with ticker [{}] is present in stop orders list".format(self._ticker)

        elif self._figi:
            uLogger.debug("Searching instrument with FIGI [{}] throw opened stop orders list...".format(self._figi))
            msg = "Instrument with FIGI [{}] is not present in opened stop orders list".format(self._figi)

            for instrument in portfolio["stat"]["stopOrders"]:
                if instrument["figi"] == self._figi:
                    result.append(instrument["orderID"])

            if result:
                msg = "Instrument with FIGI [{}] is present in opened stop orders list".format(self._figi)

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def RequestLimits(self) -> dict:
        """
        Method for obtaining the available funds for withdrawal for current `accountId`.

        See also:
        - REST API for limits: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetWithdrawLimits
        - `OverviewLimits()` method

        :return: dict with raw data from server that contains free funds for withdrawal. Example of dict:
                 `{"money": [{"currency": "rub", "units": "100", "nano": 290000000}, {...}], "blocked": [...], "blockedGuarantee": [...]}`.
                 Here `money` is an array of portfolio currency positions, `blocked` is an array of blocked currency
                 positions of the portfolio and `blockedGuarantee` is locked money under collateral for futures.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        uLogger.debug("Requesting current available funds for withdrawal. Wait, please...")

        self.body = str({"accountId": self.accountId})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetWithdrawLimits"
        rawLimits = self.SendAPIRequest(portfolioURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about available funds for withdrawal successfully received")

        return rawLimits

    def OverviewLimits(self, show: bool = False, onlyFiles=False) -> dict:
        """
        Method for parsing and show table with available funds for withdrawal for current `accountId`.

        See also: `RequestLimits()`.

        :param show: if `False` then only dictionary returns, if `True` then also print withdrawal limits to log.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: dict with raw parsed data from server and some calculated statistics about it.
        """
        if self.accountId is None or not self.accountId:
            uLogger.error("Variable `accountId` must be defined for using this method!")
            raise Exception("Account ID required")

        rawLimits = self.RequestLimits()  # raw response with current available funds for withdrawal

        view = {
            "rawLimits": rawLimits,
            "limits": {  # parsed data for every currency:
                "money": {  # this is an array of portfolio currency positions
                    item["currency"]: NanoToFloat(item["units"], item["nano"]) for item in rawLimits["money"]
                },
                "blocked": {  # this is an array of blocked currency
                    item["currency"]: NanoToFloat(item["units"], item["nano"]) for item in rawLimits["blocked"]
                },
                "blockedGuarantee": {  # this is locked money under collateral for futures
                    item["currency"]: NanoToFloat(item["units"], item["nano"]) for item in rawLimits["blockedGuarantee"]
                },
            },
        }

        # --- Prepare text table with limits in human-readable format:
        if show or onlyFiles:
            info = [
                "# Withdrawal limits\n\n",
                "* **Actual on date:** [{} UTC]\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
                "* **Account ID:** [{}]\n".format(self.accountId),
            ]

            if view["limits"]["money"]:
                info.extend([
                    "\n| Currencies | Total         | Available for withdrawal | Blocked for trade | Futures guarantee |\n",
                    "|------------|---------------|--------------------------|-------------------|-------------------|\n",
                ])

            else:
                info.append("\nNo withdrawal limits\n")

            for curr in view["limits"]["money"].keys():
                blocked = view["limits"]["blocked"][curr] if curr in view["limits"]["blocked"].keys() else 0
                blockedGuarantee = view["limits"]["blockedGuarantee"][curr] if curr in view["limits"]["blockedGuarantee"].keys() else 0
                availableMoney = view["limits"]["money"][curr] - (blocked + blockedGuarantee)

                infoStr = "| {:<10} | {:<13} | {:<24} | {:<17} | {:<17} |\n".format(
                    "[{}]".format(curr),
                    "{:.2f}".format(view["limits"]["money"][curr]),
                    "{:.2f}".format(availableMoney),
                    "{:.2f}".format(view["limits"]["blocked"][curr]) if curr in view["limits"]["blocked"].keys() else "—",
                    "{:.2f}".format(view["limits"]["blockedGuarantee"][curr]) if curr in view["limits"]["blockedGuarantee"].keys() else "—",
                )

                if curr == "rub":
                    info.insert(5, infoStr)  # hack: insert "rub" at the first position in table and after headers

                else:
                    info.append(infoStr)

            infoText = "".join(info)

            if show and not onlyFiles:
                uLogger.info(infoText)

            if self.withdrawalLimitsFile and (show or onlyFiles):
                with open(self.withdrawalLimitsFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Client's withdrawal limits was saved to file: [{}]".format(os.path.abspath(self.withdrawalLimitsFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.withdrawalLimitsFile.replace(".md", ".html") if self.withdrawalLimitsFile.endswith(".md") else self.withdrawalLimitsFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Withdrawal limits", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return view

    def RequestAccounts(self) -> dict:
        """
        Method for requesting all brokerage accounts (`accountId`s) of current user detected by `token`.

        See also:
        - REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/UsersService/UsersService_GetAccounts
        - What does account fields mean: https://tinkoff.github.io/investAPI/users/#account
        - `OverviewUserInfo()` method

        :return: dict with raw data from server that contains accounts info. Example of dict:
                 `{"accounts": [{"id": "20000xxxxx", "type": "ACCOUNT_TYPE_TINKOFF", "name": "TKSBrokerAPI account",
                   "status": "ACCOUNT_STATUS_OPEN", "openedDate": "2018-05-23T00:00:00Z",
                   "closedDate": "1970-01-01T00:00:00Z", "accessLevel": "ACCOUNT_ACCESS_LEVEL_FULL_ACCESS"}, ...]}`.
                 If `closedDate="1970-01-01T00:00:00Z"` it means that account is active now.
        """
        uLogger.debug("Requesting all brokerage accounts of current user detected by its token. Wait, please...")

        self.body = str({})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.UsersService/GetAccounts"
        rawAccounts = self.SendAPIRequest(portfolioURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about available accounts successfully received")

        return rawAccounts

    def RequestUserInfo(self) -> dict:
        """
        Method for requesting common user's information.

        See also:
        - REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/UsersService/UsersService_GetInfo
        - What does user info fields mean: https://tinkoff.github.io/investAPI/users/#getinforequest
        - What does `qualified_for_work_with` field mean: https://tinkoff.github.io/investAPI/faq_users/#qualified_for_work_with
        - `OverviewUserInfo()` method

        :return: dict with raw data from server that contains user's information. Example of dict:
                 `{"premStatus": true, "qualStatus": false, "qualifiedForWorkWith": ["bond", "foreign_shares", "leverage",
                   "russian_shares", "structured_income_bonds"], "tariff": "premium"}`.
        """
        uLogger.debug("Requesting common user's information. Wait, please...")

        self.body = str({})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.UsersService/GetInfo"
        rawUserInfo = self.SendAPIRequest(portfolioURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records about current user successfully received")

        return rawUserInfo

    def RequestMarginStatus(self, accountId: str = None) -> dict:
        """
        Method for requesting margin calculation for defined account ID.

        See also:
        - REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/UsersService/UsersService_GetMarginAttributes
        - What does margin fields mean: https://tinkoff.github.io/investAPI/users/#getmarginattributesresponse
        - `OverviewUserInfo()` method

        :param accountId: string with numeric account ID. If `None`, then used class field `accountId`.
        :return: dict with raw data from server that contains margin calculation. If margin is disabled then returns empty dict.
                 Example of responses:
                 status code 400: `{"code": 3, "message": "account margin status is disabled", "description": "30051" }`, returns: `{}`.
                 status code 200: `{"liquidPortfolio": {"currency": "rub", "units": "7175", "nano": 560000000},
                                    "startingMargin": {"currency": "rub", "units": "6311", "nano": 840000000},
                                    "minimalMargin": {"currency": "rub", "units": "3155", "nano": 920000000},
                                    "fundsSufficiencyLevel": {"units": "1", "nano": 280000000},
                                    "amountOfMissingFunds": {"currency": "rub", "units": "-863", "nano": -720000000}}`.
        """
        if accountId is None or not accountId:
            if self.accountId is None or not self.accountId:
                uLogger.error("Variable `accountId` must be defined for using this method!")
                raise Exception("Account ID required")

            else:
                accountId = self.accountId  # use `self.accountId` (main ID) by default

        uLogger.debug("Requesting margin calculation for accountId [{}]. Wait, please...".format(accountId))

        self.body = str({"accountId": accountId})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.UsersService/GetMarginAttributes"
        rawMargin = self.SendAPIRequest(portfolioURL, reqType="POST")

        if rawMargin == {"code": 3, "message": "account margin status is disabled", "description": "30051"}:
            uLogger.debug("Server response: margin status is disabled for current accountId [{}]".format(accountId))
            rawMargin = {}

        else:
            if self.moreDebug:
                uLogger.debug("Records with margin calculation for accountId [{}] successfully received".format(accountId))

        return rawMargin

    def RequestTariffLimits(self) -> dict:
        """
        Method for requesting limits of current tariff (connections, API methods etc.) of current user detected by `token`.

        See also:
        - REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/UsersService/UsersService_GetUserTariff
        - What does fields in tariff mean: https://tinkoff.github.io/investAPI/users/#getusertariffrequest
        - Unary limit: https://tinkoff.github.io/investAPI/users/#unarylimit
        - Stream limit: https://tinkoff.github.io/investAPI/users/#streamlimit
        - `OverviewUserInfo()` method

        :return: dict with raw data from server that contains limits of current tariff. Example of dict:
                 `{"unaryLimits": [{"limitPerMinute": 0, "methods": ["methods", "methods"]}, ...],
                   "streamLimits": [{"streams": ["streams", "streams"], "limit": 6}, ...]}`.
        """
        uLogger.debug("Requesting limits of current tariff. Wait, please...")

        self.body = str({})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.UsersService/GetUserTariff"
        rawTariffLimits = self.SendAPIRequest(portfolioURL, reqType="POST")

        if self.moreDebug:
            uLogger.debug("Records with limits of current tariff successfully received")

        return rawTariffLimits

    def RequestBondCoupons(self, iJSON: dict) -> dict:
        """
        Requesting bond payment calendar from official placement date to maturity date. If these dates are unknown
        then requesting dates `"from": "1970-01-01T00:00:00.000Z"` and `"to": "2099-12-31T23:59:59.000Z"`.
        All dates are in UTC timezone.

        REST API: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService/InstrumentsService_GetBondCoupons
        Documentation:
        - request: https://tinkoff.github.io/investAPI/instruments/#getbondcouponsrequest
        - response: https://tinkoff.github.io/investAPI/instruments/#coupon

        See also: `ExtendBondsData()`.

        :param iJSON: raw json data of a bond from broker server, example `iJSON = self.iList["Bonds"][self._ticker]`
                      If raw iJSON is not data of bond then server returns an error [400] with message:
                      `{"code": 3, "message": "instrument type is not bond", "description": "30048"}`.
        :return: dictionary with bond payment calendar. Response example
                 `{"events": [{"figi": "TCS00A101YV8", "couponDate": "2023-07-26T00:00:00Z", "couponNumber": "12",
                   "fixDate": "2023-07-25T00:00:00Z", "payOneBond": {"currency": "rub", "units": "7", "nano": 170000000},
                   "couponType": "COUPON_TYPE_CONSTANT", "couponStartDate": "2023-04-26T00:00:00Z",
                   "couponEndDate": "2023-07-26T00:00:00Z", "couponPeriod": 91}, {...}, ...]}`
        """
        if iJSON["figi"] is None or not iJSON["figi"]:
            uLogger.error("FIGI must be defined for using this method!")
            raise Exception("FIGI required")

        startDate = iJSON["placementDate"] if "placementDate" in iJSON.keys() else "1970-01-01T00:00:00.000Z"
        endDate = iJSON["maturityDate"] if "maturityDate" in iJSON.keys() else "2099-12-31T23:59:59.000Z"

        uLogger.debug("Requesting bond payment calendar, {}FIGI: [{}], from: [{}], to: [{}]. Wait, please...".format(
            "ticker: [{}], ".format(iJSON["ticker"]) if "ticker" in iJSON.keys() else "",
            self._figi,
            startDate,
            endDate,
        ))

        self.body = str({"figi": iJSON["figi"], "from": startDate, "to": endDate})
        calendarURL = self.server + r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/GetBondCoupons"
        calendar = self.SendAPIRequest(calendarURL, reqType="POST")

        if calendar == {"code": 3, "message": "instrument type is not bond", "description": "30048"}:
            uLogger.warning("Instrument type is not bond!")

        else:
            if self.moreDebug:
                uLogger.debug("Records about bond payment calendar successfully received")

        return calendar

    # noinspection PyTypeChecker
    def ExtendBondsData(self, instruments: list[str], xlsx: bool = False) -> pd.DataFrame:
        """
        Requests jsons with raw bonds data for every ticker or FIGI in instruments list and transform it to the wider
        Pandas DataFrame with more information about bonds: main info, current prices, bond payment calendar,
        coupon yields, current yields and some statistics etc.

        WARNING! This is too long operation if a lot of bonds requested from broker server.

        See also: `ShowInstrumentInfo()`, `CreateBondsCalendar()`, `ShowBondsCalendar()`, `RequestBondCoupons()`.

        :param instruments: list of strings with tickers or FIGIs.
        :param xlsx: if True then also exports Pandas DataFrame to xlsx-file `bondsXLSXFile`, default `ext-bonds.xlsx`,
                     for further used by data scientists or stock analytics.
        :return: wider Pandas DataFrame with more full and calculated data about bonds, than raw response from broker.
                 In XLSX-file and Pandas DataFrame fields mean:
                 - main info about bond: https://tinkoff.github.io/investAPI/instruments/#bond
                 - info about coupon: https://tinkoff.github.io/investAPI/instruments/#coupon
        """
        if instruments is None or not instruments:
            uLogger.error("List of tickers or FIGIs must be defined for using this method!")
            raise Exception("Ticker or FIGI required")

        if isinstance(instruments, str):
            instruments = [instruments]

        uniqueInstruments = self.GetUniqueFIGIs(instruments)

        uLogger.debug("Requesting raw bonds calendar from server, transforming and extending it. Wait, please...")

        iCount = len(uniqueInstruments)
        tooLong = iCount >= 20
        if tooLong:
            uLogger.warning("You requested a lot of bonds! Operation will takes more time. Wait, please...")

        bonds = None
        for i, self._figi in enumerate(uniqueInstruments):
            instrument = self.SearchByFIGI(requestPrice=False)  # raw data about instrument from server

            if "type" in instrument.keys() and instrument["type"] == "Bonds":
                # raw bond data from server where fields mean: https://tinkoff.github.io/investAPI/instruments/#bond
                rawBond = self.SearchByFIGI(requestPrice=True)

                # Widen raw data with UTC current time (iData["actualDateTime"]):
                actualDate = datetime.now(tzutc())
                iData = {"actualDateTime": actualDate.strftime(TKS_DATE_TIME_FORMAT)} | rawBond

                # Widen raw data with bond payment calendar (iData["rawCalendar"]):
                iData = iData | {"rawCalendar": self.RequestBondCoupons(iJSON=iData)}

                # Replace some values with human-readable:
                iData["nominalCurrency"] = iData["nominal"]["currency"]
                iData["nominal"] = NanoToFloat(iData["nominal"]["units"], iData["nominal"]["nano"])
                iData["placementPrice"] = NanoToFloat(iData["placementPrice"]["units"], iData["placementPrice"]["nano"])
                iData["aciCurrency"] = iData["aciValue"]["currency"]
                iData["aciValue"] = NanoToFloat(iData["aciValue"]["units"], iData["aciValue"]["nano"])
                iData["issueSize"] = int(iData["issueSize"])
                iData["issueSizePlan"] = int(iData["issueSizePlan"])
                iData["tradingStatus"] = TKS_TRADING_STATUSES[iData["tradingStatus"]]
                iData["step"] = iData["step"] if "step" in iData.keys() else 0
                iData["realExchange"] = TKS_REAL_EXCHANGES[iData["realExchange"]]
                iData["klong"] = NanoToFloat(iData["klong"]["units"], iData["klong"]["nano"]) if "klong" in iData.keys() else 0
                iData["kshort"] = NanoToFloat(iData["kshort"]["units"], iData["kshort"]["nano"]) if "kshort" in iData.keys() else 0
                iData["dlong"] = NanoToFloat(iData["dlong"]["units"], iData["dlong"]["nano"]) if "dlong" in iData.keys() else 0
                iData["dshort"] = NanoToFloat(iData["dshort"]["units"], iData["dshort"]["nano"]) if "dshort" in iData.keys() else 0
                iData["dlongMin"] = NanoToFloat(iData["dlongMin"]["units"], iData["dlongMin"]["nano"]) if "dlongMin" in iData.keys() else 0
                iData["dshortMin"] = NanoToFloat(iData["dshortMin"]["units"], iData["dshortMin"]["nano"]) if "dshortMin" in iData.keys() else 0

                # Widen raw data with price fields from `currentPrice` values (all prices are actual at `actualDateTime` date):
                iData["limitUpPercent"] = iData["currentPrice"]["limitUp"]  # max price on current day in percents of nominal
                iData["limitDownPercent"] = iData["currentPrice"]["limitDown"]  # min price on current day in percents of nominal
                iData["lastPricePercent"] = iData["currentPrice"]["lastPrice"]  # last price on market in percents of nominal
                iData["closePricePercent"] = iData["currentPrice"]["closePrice"]  # previous day close in percents of nominal
                iData["changes"] = iData["currentPrice"]["changes"]  # this is percent of changes between `currentPrice` and `lastPrice`
                iData["limitUp"] = iData["limitUpPercent"] * iData["nominal"] / 100  # max price on current day is `limitUpPercent` * `nominal`
                iData["limitDown"] = iData["limitDownPercent"] * iData["nominal"] / 100  # min price on current day is `limitDownPercent` * `nominal`
                iData["lastPrice"] = iData["lastPricePercent"] * iData["nominal"] / 100  # last price on market is `lastPricePercent` * `nominal`
                iData["closePrice"] = iData["closePricePercent"] * iData["nominal"] / 100  # previous day close is `closePricePercent` * `nominal`
                iData["changesDelta"] = iData["lastPrice"] - iData["closePrice"]  # this is delta between last deal price and last close

                # Widen raw data with calendar data from `rawCalendar` values:
                calendarData = []
                if "events" in iData["rawCalendar"].keys():
                    for item in iData["rawCalendar"]["events"]:
                        calendarData.append({
                            "couponDate": item["couponDate"],
                            "couponNumber": int(item["couponNumber"]),
                            "fixDate": item["fixDate"] if "fixDate" in item.keys() else "",
                            "payCurrency": item["payOneBond"]["currency"],
                            "payOneBond": NanoToFloat(item["payOneBond"]["units"], item["payOneBond"]["nano"]),
                            "couponType": TKS_COUPON_TYPES[item["couponType"]],
                            "couponStartDate": item["couponStartDate"],
                            "couponEndDate": item["couponEndDate"],
                            "couponPeriod": item["couponPeriod"],
                        })

                    # if maturity date is unknown then uses the latest date in bond payment calendar for it:
                    if "maturityDate" not in iData.keys():
                        iData["maturityDate"] = datetime.strptime(calendarData[0]["couponDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()).strftime(TKS_DATE_TIME_FORMAT) if calendarData else ""

                # Widen raw data with Coupon Rate.
                # This is sum of all coupon payments divided on nominal price and expire days sum and then multiple on 365 days and 100%:
                iData["sumCoupons"] = sum([coupon["payOneBond"] for coupon in calendarData])
                iData["periodDays"] = sum([coupon["couponPeriod"] for coupon in calendarData])
                iData["couponsYield"] = 100 * 365 * (iData["sumCoupons"] / iData["nominal"]) / iData["periodDays"] if iData["nominal"] != 0 and iData["periodDays"] != 0 else 0.

                # Widen raw data with Yield to Maturity (YTM) on current date.
                # This is sum of all stayed coupons to maturity minus ACI and divided on current bond price and then multiple on stayed days and 100%:
                maturityDate = datetime.strptime(iData["maturityDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()) if iData["maturityDate"] else None
                iData["daysToMaturity"] = (maturityDate - actualDate).days if iData["maturityDate"] else None
                iData["sumLastCoupons"] = sum([coupon["payOneBond"] for coupon in calendarData if datetime.strptime(coupon["couponDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()) > actualDate])
                iData["lastPayments"] = iData["sumLastCoupons"] - iData["aciValue"]  # sum of all last coupons minus current ACI value
                iData["currentYield"] = 100 * 365 * (iData["lastPayments"] / iData["lastPrice"]) / iData["daysToMaturity"] if iData["lastPrice"] != 0 and iData["daysToMaturity"] != 0 else 0.

                iData["calendar"] = calendarData  # adds calendar at the end

                # Remove not used data:
                iData.pop("uid")
                iData.pop("positionUid")
                iData.pop("currentPrice")
                iData.pop("rawCalendar")

                colNames = list(iData.keys())
                if bonds is None:
                    bonds = pd.DataFrame(data=pd.DataFrame.from_records(data=[iData], columns=colNames))

                else:
                    bonds = pd.concat([bonds, pd.DataFrame.from_records(data=[iData], columns=colNames)], axis=0, ignore_index=True)

            else:
                uLogger.warning("Instrument is not a bond!")

            processed = round(100 * (i + 1) / iCount, 1)
            if tooLong and processed % 5 == 0:
                uLogger.info("{}% processed [{} / {}]...".format(round(processed), i + 1, iCount))

            else:
                uLogger.debug("{}% bonds processed [{} / {}]...".format(processed, i + 1, iCount))

        bonds.index = bonds["ticker"].tolist()  # replace indexes with ticker names

        # Saving bonds from Pandas DataFrame to XLSX sheet:
        if xlsx and self.bondsXLSXFile:
            with pd.ExcelWriter(
                    path=self.bondsXLSXFile,
                    date_format=TKS_DATE_FORMAT,
                    datetime_format=TKS_DATE_TIME_FORMAT,
                    mode="w",
            ) as writer:
                bonds.to_excel(
                    writer,
                    sheet_name="Extended bonds data",
                    index=True,
                    encoding="UTF-8",
                    freeze_panes=(1, 1),
                )  # saving as XLSX-file with freeze first row and column as headers

            uLogger.info("XLSX-file with extended bonds data for further used by data scientists or stock analytics: [{}]".format(os.path.abspath(self.bondsXLSXFile)))

        return bonds

    def CreateBondsCalendar(self, extBonds: pd.DataFrame, xlsx: bool = False) -> pd.DataFrame:
        """
        Creates bond payments calendar as Pandas DataFrame, and also save it to the XLSX-file, `calendar.xlsx` by default.

        WARNING! This is too long operation if a lot of bonds requested from broker server.

        See also: `ShowBondsCalendar()`, `ExtendBondsData()`.

        :param extBonds: Pandas DataFrame object returns by `ExtendBondsData()` method and contains
                        extended information about bonds: main info, current prices, bond payment calendar,
                        coupon yields, current yields and some statistics etc.
                        If this parameter is `None` then used `figi` or `ticker` as bond name and then calculate `ExtendBondsData()`.
        :param xlsx: if True then also exports Pandas DataFrame to file `calendarFile` + `".xlsx"`, `calendar.xlsx` by default,
                     for further used by data scientists or stock analytics.
        :return: Pandas DataFrame with only bond payments calendar data. Fields mean: https://tinkoff.github.io/investAPI/instruments/#coupon
        """
        if extBonds is None or not isinstance(extBonds, pd.DataFrame) or extBonds.empty:
            extBonds = self.ExtendBondsData(instruments=[self._figi, self._ticker], xlsx=False)

        uLogger.debug("Generating bond payments calendar data. Wait, please...")

        colNames = ["Paid", "Payment date", "FIGI", "Ticker", "Name", "No.", "Value", "Currency", "Coupon type", "Period", "End registry date", "Coupon start date", "Coupon end date"]
        colID = ["paid", "couponDate", "figi", "ticker", "name", "couponNumber", "payOneBond", "payCurrency", "couponType", "couponPeriod", "fixDate", "couponStartDate", "couponEndDate"]
        calendar = None
        for bond in extBonds.iterrows():
            for item in bond[1]["calendar"]:
                cData = {
                    "paid": datetime.now(tzutc()) > datetime.strptime(item["couponDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()),
                    "couponDate": item["couponDate"],
                    "figi": bond[1]["figi"],
                    "ticker": bond[1]["ticker"],
                    "name": bond[1]["name"],
                    "couponNumber": item["couponNumber"],
                    "payOneBond": item["payOneBond"],
                    "payCurrency": item["payCurrency"],
                    "couponType": item["couponType"],
                    "couponPeriod": item["couponPeriod"],
                    "fixDate": item["fixDate"],
                    "couponStartDate": item["couponStartDate"],
                    "couponEndDate": item["couponEndDate"],
                }

                if calendar is None:
                    calendar = pd.DataFrame(data=pd.DataFrame.from_records(data=[cData], columns=colID))

                else:
                    calendar = pd.concat([calendar, pd.DataFrame.from_records(data=[cData], columns=colID)], axis=0, ignore_index=True)

        if calendar is not None:
            calendar = calendar.sort_values(by=["couponDate"], axis=0, ascending=True)  # sort all payments for all bonds by payment date

            # Saving calendar from Pandas DataFrame to XLSX sheet:
            if xlsx:
                xlsxCalendarFile = self.calendarFile.replace(".md", ".xlsx") if self.calendarFile.endswith(".md") else self.calendarFile + ".xlsx"

                with pd.ExcelWriter(
                        path=xlsxCalendarFile,
                        date_format=TKS_DATE_FORMAT,
                        datetime_format=TKS_DATE_TIME_FORMAT,
                        mode="w",
                ) as writer:
                    humanReadable = calendar.copy(deep=True)
                    humanReadable["couponDate"] = humanReadable["couponDate"].apply(lambda x: x.split("T")[0])
                    humanReadable["fixDate"] = humanReadable["fixDate"].apply(lambda x: x.split("T")[0])
                    humanReadable["couponStartDate"] = humanReadable["couponStartDate"].apply(lambda x: x.split("T")[0])
                    humanReadable["couponEndDate"] = humanReadable["couponEndDate"].apply(lambda x: x.split("T")[0])
                    humanReadable.columns = colNames  # human-readable column names

                    humanReadable.to_excel(
                        writer,
                        sheet_name="Bond payments calendar",
                        index=False,
                        freeze_panes=(1, 2),
                    )  # saving as XLSX-file with freeze first row and column as headers

                    del humanReadable  # release df in memory

                uLogger.info("XLSX-file with bond payments calendar for further used by data scientists or stock analytics: [{}]".format(os.path.abspath(xlsxCalendarFile)))

        return calendar

    def ShowBondsCalendar(self, extBonds: pd.DataFrame, show: bool = True, onlyFiles=False) -> str:
        """
        Show bond payments calendar as a table. One row in input `bonds` dataframe contains one bond.
        Also, creates Markdown file with calendar data, `calendar.md` by default.

        See also: `ShowInstrumentInfo()`, `RequestBondCoupons()`, `CreateBondsCalendar()` and `ExtendBondsData()`.

        :param extBonds: Pandas DataFrame object returns by `ExtendBondsData()` method and contains
                        extended information about bonds: main info, current prices, bond payment calendar,
                        coupon yields, current yields and some statistics etc.
                        If this parameter is `None` then used `figi` or `ticker` as bond name and then calculate `ExtendBondsData()`.
        :param show: if `True` then also printing bonds payment calendar to the console,
                     otherwise save to file `calendarFile` only. `False` by default.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: multilines text in Markdown format with bonds payment calendar as a table.
        """
        if extBonds is None or not isinstance(extBonds, pd.DataFrame) or extBonds.empty:
            extBonds = self.ExtendBondsData(instruments=[self._figi, self._ticker], xlsx=show or onlyFiles)

        infoText = "# Bond payments calendar\n\n"

        calendar = self.CreateBondsCalendar(extBonds, xlsx=show or onlyFiles)  # generate Pandas DataFrame with full calendar data

        if not (calendar is None or calendar.empty):
            splitLine = "|       |                 |              |              |     |               |           |        |                   |\n"

            info = [
                "* **Actual on date:** [{} UTC]\n\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
                "| Paid  | Payment date    | FIGI         | Ticker       | No. | Value         | Type      | Period | End registry date |\n",
                "|-------|-----------------|--------------|--------------|-----|---------------|-----------|--------|-------------------|\n",
            ]

            newMonth = False
            notOneBond = calendar["figi"].nunique() > 1
            for i, bond in enumerate(calendar.iterrows()):
                if newMonth and notOneBond:
                    info.append(splitLine)

                info.append(
                    "| {:<5} | {:<15} | {:<12} | {:<12} | {:<3} | {:<13} | {:<9} | {:<6} | {:<17} |\n".format(
                        "  √" if bond[1]["paid"] else "  —",
                        bond[1]["couponDate"].split("T")[0],
                        bond[1]["figi"],
                        bond[1]["ticker"],
                        bond[1]["couponNumber"],
                        "{} {}".format(
                            "{}".format(round(bond[1]["payOneBond"], 6)).rstrip("0").rstrip("."),
                            bond[1]["payCurrency"],
                        ),
                        bond[1]["couponType"],
                        bond[1]["couponPeriod"],
                        bond[1]["fixDate"].split("T")[0],
                    )
                )

                if i < len(calendar.values) - 1:
                    curDate = datetime.strptime(bond[1]["couponDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc())
                    nextDate = datetime.strptime(calendar["couponDate"].values[i + 1], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc())
                    newMonth = False if curDate.month == nextDate.month else True

                else:
                    newMonth = False

            infoText += "".join(info)

            if show and not onlyFiles:
                uLogger.info("{}".format(infoText))

            if self.calendarFile is not None and (show or onlyFiles):
                with open(self.calendarFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Bond payments calendar was saved to file: [{}]".format(os.path.abspath(self.calendarFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.calendarFile.replace(".md", ".html") if self.calendarFile.endswith(".md") else self.calendarFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="Bond payments calendar", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        else:
            infoText += "No data\n"

        return infoText

    def OverviewAccounts(self, show: bool = False, onlyFiles=False) -> dict:
        """
        Method for parsing and show simple table with all available user accounts.

        See also: `RequestAccounts()` and `OverviewUserInfo()` methods.

        :param show: if `False` then only dictionary with accounts data returns, if `True` then also print it to log.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: dict with parsed accounts data received from `RequestAccounts()` method. Example of dict:
                 `view = {"rawAccounts": {rawAccounts from RequestAccounts() method...},
                          "stat": {"accountId string": {"type": "Tinkoff brokerage account", "name": "Test - 1",
                                                        "status": "Opened and active account", "opened": "2018-05-23 00:00:00",
                                                        "closed": "—", "access": "Full access" }, ...}}`
        """
        rawAccounts = self.RequestAccounts()  # Raw responses with accounts

        # This is an array of dict with user accounts, its `accountId`s and some parsed data:
        accounts = {
            item["id"]: {
                "type": TKS_ACCOUNT_TYPES[item["type"]],
                "name": item["name"],
                "status": TKS_ACCOUNT_STATUSES[item["status"]],
                "opened": datetime.strptime(item["openedDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT),
                "closed": datetime.strptime(item["closedDate"], TKS_DATE_TIME_FORMAT).replace(tzinfo=tzutc()).astimezone(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT) if item["closedDate"] != "1970-01-01T00:00:00Z" else "—",
                "access": TKS_ACCESS_LEVELS[item["accessLevel"]],
            } for item in rawAccounts["accounts"]
        }

        # Raw and parsed data with some fields replaced in "stat" section:
        view = {
            "rawAccounts": rawAccounts,
            "stat": accounts,
        }

        # --- Prepare simple text table with only accounts data in human-readable format:
        if show or onlyFiles:
            info = [
                "# User accounts\n\n",
                "* **Actual date:** [{} UTC]\n\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
                "| Account ID   | Type                      | Status                    | Name                           |\n",
                "|--------------|---------------------------|---------------------------|--------------------------------|\n",
            ]

            for account in view["stat"].keys():
                info.extend([
                    "| {:<12} | {:<25} | {:<25} | {:<30} |\n".format(
                        account,
                        view["stat"][account]["type"],
                        view["stat"][account]["status"],
                        view["stat"][account]["name"],
                    )
                ])

            infoText = "".join(info)

            if show and not onlyFiles:
                uLogger.info(infoText)

            if self.userAccountsFile and (show or onlyFiles):
                with open(self.userAccountsFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("User accounts were saved to file: [{}]".format(os.path.abspath(self.userAccountsFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.userAccountsFile.replace(".md", ".html") if self.userAccountsFile.endswith(".md") else self.userAccountsFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="User accounts", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return view

    # noinspection PyTypeChecker
    def OverviewUserInfo(self, show: bool = False, onlyFiles=False) -> dict:
        """
        Method for parsing and show all available user's data (`accountId`s, common user information, margin status and tariff connections limit).

        See also: `OverviewAccounts()`, `RequestAccounts()`, `RequestUserInfo()`, `RequestMarginStatus()` and `RequestTariffLimits()` methods.

        :param show: if `False` then only dictionary returns, if `True` then also print user's data to log.
        :param onlyFiles: if `True` then do not show Markdown table in the console, but only generates report files.
        :return: dict with raw parsed data from server and some calculated statistics about it.
        """
        overview = self.Overview(show=False)  # Request current user portfolio for the ability to calculate missing funds
        tmpTicker = self._ticker
        self._ticker = "RUB000UTSTOM"  # This instrument show in rub how much money cost current margin
        missing = self.GetInstrumentFromPortfolio(portfolio=overview)
        self._ticker = tmpTicker

        rawUserInfo = self.RequestUserInfo()  # Raw response with common user info
        overviewAccount = self.OverviewAccounts(show=False)  # Raw and parsed accounts data
        rawAccounts = overviewAccount["rawAccounts"]  # Raw response with user accounts data
        accounts = overviewAccount["stat"]  # Dict with only statistics about user accounts
        rawMargins = {account: self.RequestMarginStatus(accountId=account) for account in accounts.keys()}  # Raw response with margin calculation for every account ID
        rawTariffLimits = self.RequestTariffLimits()  # Raw response with limits of current tariff

        # This is dict with parsed common user data:
        userInfo = {
            "premium": "Yes" if rawUserInfo["premStatus"] else "No",
            "qualified": "Yes" if rawUserInfo["qualStatus"] else "No",
            "allowed": [TKS_QUALIFIED_TYPES[item] for item in rawUserInfo["qualifiedForWorkWith"]],
            "tariff": rawUserInfo["tariff"],
        }

        # This is an array of dict with parsed margin statuses for every account IDs:
        margins = {}
        for accountId in accounts.keys():
            if rawMargins[accountId]:
                margins[accountId] = {
                    "currency": rawMargins[accountId]["liquidPortfolio"]["currency"],
                    "liquid": NanoToFloat(rawMargins[accountId]["liquidPortfolio"]["units"], rawMargins[accountId]["liquidPortfolio"]["nano"]),
                    "start": NanoToFloat(rawMargins[accountId]["startingMargin"]["units"], rawMargins[accountId]["startingMargin"]["nano"]),
                    "min": NanoToFloat(rawMargins[accountId]["minimalMargin"]["units"], rawMargins[accountId]["minimalMargin"]["nano"]),
                    "diff": NanoToFloat(rawMargins[accountId]["amountOfMissingFunds"]["units"], rawMargins[accountId]["amountOfMissingFunds"]["nano"]),
                    "level": NanoToFloat(rawMargins[accountId]["fundsSufficiencyLevel"]["units"], rawMargins[accountId]["fundsSufficiencyLevel"]["nano"]),
                    "missing": missing["volume"],
                }

            else:
                margins[accountId] = {}  # Server response: margin status is disabled for current accountId

        unary = {}  # unary-connection limits
        for item in rawTariffLimits["unaryLimits"]:
            if item["limitPerMinute"] in unary.keys():
                unary[item["limitPerMinute"]].extend(item["methods"])

            else:
                unary[item["limitPerMinute"]] = item["methods"]

        stream = {}  # stream-connection limits
        for item in rawTariffLimits["streamLimits"]:
            if item["limit"] in stream.keys():
                stream[item["limit"]].extend(item["streams"])

            else:
                stream[item["limit"]] = item["streams"]

        # This is dict with parsed limits of current tariff (connections, API methods etc.):
        limits = {
            "unary": unary,
            "stream": stream,
        }

        # Raw and parsed data as an output result:
        view = {
            "rawUserInfo": rawUserInfo,
            "rawAccounts": rawAccounts,
            "rawMargins": rawMargins,
            "rawTariffLimits": rawTariffLimits,
            "stat": {
                "overview": overview,
                "userInfo": userInfo,
                "accounts": accounts,
                "margins": margins,
                "limits": limits,
            },
        }

        # --- Prepare text table with user information in human-readable format:
        if show or onlyFiles:
            info = [
                "# Full user information\n\n",
                "* **Actual date:** [{} UTC]\n\n".format(datetime.now(tzutc()).strftime(TKS_PRINT_DATE_TIME_FORMAT)),
                "## Common information\n\n",
                "* **Qualified user:** {}\n".format(view["stat"]["userInfo"]["qualified"]),
                "* **Tariff name:** {}\n".format(view["stat"]["userInfo"]["tariff"]),
                "* **Premium user:** {}\n".format(view["stat"]["userInfo"]["premium"]),
                "* **Allowed to work with instruments:**\n{}\n".format("".join(["  - {}\n".format(item) for item in view["stat"]["userInfo"]["allowed"]])),
                "\n## User accounts\n\n",
            ]

            for account in view["stat"]["accounts"].keys():
                info.extend([
                    "### ID: [{}]\n\n".format(account),
                    "| Parameters           | Values                                                       |\n",
                    "|----------------------|--------------------------------------------------------------|\n",
                    "| Account type:        | {:<60} |\n".format(view["stat"]["accounts"][account]["type"]),
                    "| Account name:        | {:<60} |\n".format(view["stat"]["accounts"][account]["name"]),
                    "| Account status:      | {:<60} |\n".format(view["stat"]["accounts"][account]["status"]),
                    "| Access level:        | {:<60} |\n".format(view["stat"]["accounts"][account]["access"]),
                    "| Date opened:         | {:<60} |\n".format(view["stat"]["accounts"][account]["opened"]),
                    "| Date closed:         | {:<60} |\n".format(view["stat"]["accounts"][account]["closed"]),
                ])

                if margins[account]:
                    info.extend([
                        "| Margin status:       | Enabled                                                      |\n",
                        "| - Liquid portfolio:  | {:<60} |\n".format("{} {}".format(margins[account]["liquid"], margins[account]["currency"])),
                        "| - Margin starting:   | {:<60} |\n".format("{} {}".format(margins[account]["start"], margins[account]["currency"])),
                        "| - Margin minimum:    | {:<60} |\n".format("{} {}".format(margins[account]["min"], margins[account]["currency"])),
                        "| - Margin difference: | {:<60} |\n".format("{} {}".format(margins[account]["diff"], margins[account]["currency"])),
                        "| - Sufficiency level: | {:<60} |\n".format("{:.2f} ({:.2f}%)".format(margins[account]["level"], margins[account]["level"] * 100)),
                        "| - Not covered funds: | {:<60} |\n\n".format("{:.2f} {}".format(margins[account]["missing"], margins[account]["currency"])),
                    ])

                else:
                    info.append("| Margin status:       | Disabled                                                     |\n\n")

            info.extend([
                "\n## Current user tariff limits\n",
                "\n### See also\n",
                "* Tinkoff limit policy: https://tinkoff.github.io/investAPI/limits/\n",
                "* Tinkoff Invest API: https://tinkoff.github.io/investAPI/\n",
                "  - More about REST API requests: https://tinkoff.github.io/investAPI/swagger-ui/\n",
                "  - More about gRPC requests for stream connections: https://tinkoff.github.io/investAPI/grpc/\n",
                "\n### Unary limits\n",
            ])

            if unary:
                for key, values in sorted(unary.items()):
                    info.append("\n* Max requests per minute: {}\n".format(key))

                    for value in values:
                        info.append("  - {}\n".format(value))

            else:
                info.append("\nNot available\n")

            info.append("\n### Stream limits\n")

            if stream:
                for key, values in sorted(stream.items()):
                    info.append("\n* Max stream connections: {}\n".format(key))

                    for value in values:
                        info.append("  - {}\n".format(value))

            else:
                info.append("\nNot available\n")

            infoText = "".join(info)

            if show and not onlyFiles:
                uLogger.info(infoText)

            if self.userInfoFile and (show or onlyFiles):
                with open(self.userInfoFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("User data was saved to file: [{}]".format(os.path.abspath(self.userInfoFile)))

                if self.useHTMLReports:
                    htmlFilePath = self.userInfoFile.replace(".md", ".html") if self.userInfoFile.endswith(".md") else self.userInfoFile + ".html"
                    with open(htmlFilePath, "w", encoding="UTF-8") as fH:
                        fH.write(Template(text=MAIN_INFO_TEMPLATE).render(mainTitle="User info", commonCSS=COMMON_CSS, markdown=infoText))

                    uLogger.info("The report has also been converted to an HTML file: [{}]".format(os.path.abspath(htmlFilePath)))

        return view


class Args:
    """
    If `Main()` function is imported as module, then this class used to convert arguments from **kwargs as object.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return None


def ParseArgs():
    """This function get and parse command line keys."""
    parser = ArgumentParser()  # command-line string parser

    parser.description = "TKSBrokerAPI is a trading platform for automation on Python to simplify the implementation of trading scenarios and work with Tinkoff Invest API server via the REST protocol. See examples: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md"
    parser.usage = "\n/as module/ python TKSBrokerAPI.py [some options] [one command]\n/as CLI tool/ tksbrokerapi [some options] [one command]"

    # --- options:

    parser.add_argument("--no-cache", action="store_true", default=False, help="Option: not use local cache `dump.json`, but update raw instruments data when starting the platform. `False` by default.")
    parser.add_argument("--token", type=str, help="Option: Tinkoff service's api key. If not set then used environment variable `TKS_API_TOKEN`. See how to use: https://tinkoff.github.io/investAPI/token/")
    parser.add_argument("--account-id", type=str, default=None, help="Option: string with an user numeric account ID in Tinkoff Broker. It can be found in any broker's reports (see the contract number). Also, this variable can be set from environment variable `TKS_ACCOUNT_ID`.")

    parser.add_argument("--ticker", "-t", type=str, help="Option: instrument's ticker, e.g. `IBM`, `YNDX`, `GOOGL` etc. Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR`.")
    parser.add_argument("--figi", "-f", type=str, help="Option: instrument's FIGI, e.g. `BBG006L8G4H1` (for `YNDX`).")

    parser.add_argument("--depth", type=int, default=1, help="Option: Depth of Market (DOM) can be >=1, 1 by default.")
    parser.add_argument("--no-cancelled", "--no-canceled", action="store_true", default=False, help="Option: remove information about cancelled operations from the deals report by the `--deals` key. `False` by default.")

    parser.add_argument("--output", type=str, default=None, help="Option: replace default paths to output files for some commands. If `None` then used default files.")
    parser.add_argument("--html", "--HTML", action="store_true", default=False, help="Option: if key present then TKSBrokerAPI generate also HTML reports from Markdown. False by default.")

    parser.add_argument("--interval", type=str, default="hour", help="Option: available values are `1min`, `5min`, `15min`, `hour` and `day`. Used only with `--history` key. This is time period of one candle. Default: `hour` for every history candles.")
    parser.add_argument("--only-missing", action="store_true", default=False, help="Option: if history file define by `--output` key then add only last missing candles, do not request all history length. `False` by default.")
    parser.add_argument("--csv-sep", type=str, default=",", help="Option: separator if csv-file is used, `,` by default.")

    parser.add_argument("--debug-level", "--log-level", "--verbosity", "-v", type=int, default=20, help="Option: showing STDOUT messages of minimal debug level, e.g. 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 = ERROR, 50 = CRITICAL. INFO (20) by default.")
    parser.add_argument("--more", "--more-debug", action="store_true", default=False, help="Option: `--debug-level` key only switch log level verbosity, but in addition `--more` key enable all debug information, such as net request and response headers in all methods.")
    parser.add_argument("--tag", type=str, default="", help="Option: identification TKSBrokerAPI tag in log messages to simplify debugging when platform instances runs in parallel mode. Default: `""` (empty string).")

    # --- commands:

    parser.add_argument("--version", "--ver", action="store_true", help="Action: shows current semantic version, looks like `major.minor.buildnumber`. If TKSBrokerAPI not installed via pip, then used local build number `.dev0`.")

    parser.add_argument("--list", "-l", action="store_true", help="Action: get and print all available instruments and some information from broker server. Also, you can define `--output` key to save list of instruments to file, default: `instruments.md`.")
    parser.add_argument("--list-xlsx", "-x", action="store_true", help="Action: get all available instruments from server for current account and save raw data into xlsx-file for further used by data scientists or stock analytics, default: `dump.xlsx`.")
    parser.add_argument("--bonds-xlsx", "-b", type=str, nargs="*", help="Action: get all available bonds if only key present or list of bonds with FIGIs or tickers and transform it to the wider Pandas DataFrame with more information about bonds: main info, current prices, bonds payment calendar, coupon yields, current yields and some statistics etc. And then export data to XLSX-file, default: `ext-bonds.xlsx` or you can change it with `--output` key. WARNING! This is too long operation if a lot of bonds requested from broker server.")
    parser.add_argument("--search", "-s", type=str, nargs=1, help="Action: search for an instruments by part of the name, ticker or FIGI. Also, you can define `--output` key to save results to file, default: `search-results.md`.")
    parser.add_argument("--info", "-i", action="store_true", help="Action: get information from broker server about instrument by it's ticker or FIGI. `--ticker` key or `--figi` key must be defined!")
    parser.add_argument("--calendar", "-c", type=str, nargs="*", help="Action: show bonds payment calendar as a table. Calendar build for one or more tickers or FIGIs, or for all bonds if only key present. If the `--output` key present then calendar saves to file, default: `calendar.md`. Also, created XLSX-file with bond payments calendar for further used by data scientists or stock analytics, `calendar.xlsx` by default. WARNING! This is too long operation if a lot of bonds requested from broker server.")
    parser.add_argument("--price", action="store_true", help="Action: show actual price list for current instrument. Also, you can use `--depth` key. `--ticker` key or `--figi` key must be defined!")
    parser.add_argument("--prices", "-p", type=str, nargs="+", help="Action: get and print current prices for list of given instruments (by it's tickers or by FIGIs). WARNING! This is too long operation if you request a lot of instruments! Also, you can define `--output` key to save list of prices to file, default: `prices.md`.")

    parser.add_argument("--overview", "-o", action="store_true", help="Action: shows all open positions, orders and some statistics. Also, you can define `--output` key to save this information to file, default: `overview.md`.")
    parser.add_argument("--overview-digest", action="store_true", help="Action: shows a short digest of the portfolio status. Also, you can define `--output` key to save this information to file, default: `overview-digest.md`.")
    parser.add_argument("--overview-positions", action="store_true", help="Action: shows only open positions. Also, you can define `--output` key to save this information to file, default: `overview-positions.md`.")
    parser.add_argument("--overview-orders", action="store_true", help="Action: shows only sections of open limits and stop orders. Also, you can define `--output` key to save orders to file, default: `overview-orders.md`.")
    parser.add_argument("--overview-analytics", action="store_true", help="Action: shows only the analytics section and the distribution of the portfolio by various categories. Also, you can define `--output` key to save this information to file, default: `overview-analytics.md`.")
    parser.add_argument("--overview-calendar", action="store_true", help="Action: shows only the bonds calendar section (if these present in portfolio). Also, you can define `--output` key to save this information to file, default: `overview-calendar.md`.")

    parser.add_argument("--deals", "-d", type=str, nargs="*", help="Action: show all deals between two given dates. Start day may be an integer number: -1, -2, -3 days ago. Also, you can use keywords: `today`, `yesterday` (-1), `week` (-7), `month` (-30) and `year` (-365). Dates format must be: `%%Y-%%m-%%d`, e.g. 2020-02-03. With `--no-cancelled` key information about cancelled operations will be removed from the deals report. Also, you can define `--output` key to save all deals to file, default: `deals.md`.")
    parser.add_argument("--history", type=str, nargs="*", help="Action: get last history candles of the current instrument defined by `--ticker` or `--figi` (FIGI id) keys. History returned between two given dates: `start` and `end`. Minimum requested date in the past is `1970-01-01`. This action may be used together with the `--render-chart` key. Also, you can define `--output` key to save history candlesticks to file.")
    parser.add_argument("--load-history", type=str, help="Action: try to load history candles from given csv-file as a Pandas Dataframe and print it in to the console. This action may be used together with the `--render-chart` key.")
    parser.add_argument("--render-chart", type=str, help="Action: render candlesticks chart. This key may only used with `--history` or `--load-history` together. Action has 1 parameter with two possible string values: `interact` (`i`) or `non-interact` (`ni`).")

    parser.add_argument("--trade", nargs="*", help="Action: universal action to open market position for defined ticker or FIGI. You must specify 1-5 parameters: [direction `Buy` or `Sell`] [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`]. See examples in readme.")
    parser.add_argument("--buy", nargs="*", help="Action: immediately open BUY market position at the current price for defined ticker or FIGI. You must specify 0-4 parameters: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`].")
    parser.add_argument("--sell", nargs="*", help="Action: immediately open SELL market position at the current price for defined ticker or FIGI. You must specify 0-4 parameters: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`].")

    parser.add_argument("--order", nargs="*", help="Action: universal action to open limit or stop-order in any directions. You must specify 4-7 parameters: [direction `Buy` or `Sell`] [order type `Limit` or `Stop`] [lots] [target price] [maybe for stop-order: [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`]]. See examples in readme.")
    parser.add_argument("--buy-limit", type=float, nargs=2, help="Action: open pending BUY limit-order (below current price). You must specify only 2 parameters: [lots] [target price] to open BUY limit-order. If you try to create `Buy` limit-order above current price then broker immediately open `Buy` market order, such as if you do simple `--buy` operation!")
    parser.add_argument("--sell-limit", type=float, nargs=2, help="Action: open pending SELL limit-order (above current price). You must specify only 2 parameters: [lots] [target price] to open SELL limit-order. If you try to create `Sell` limit-order below current price then broker immediately open `Sell` market order, such as if you do simple `--sell` operation!")
    parser.add_argument("--buy-stop", nargs="*", help="Action: open BUY stop-order. You must specify at least 2 parameters: [lots] [target price] to open BUY stop-order. In additional you can specify 3 parameters for stop-order: [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`]. When current price will go up or down to target price value then broker opens a limit order. Stop loss order always executed by market price.")
    parser.add_argument("--sell-stop", nargs="*", help="Action: open SELL stop-order. You must specify at least 2 parameters: [lots] [target price] to open SELL stop-order. In additional you can specify 3 parameters for stop-order: [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`]. When current price will go up or down to target price value then broker opens a limit order. Stop loss order always executed by market price.")
    # parser.add_argument("--buy-limit-order-grid", type=str, nargs="*", help="Action: open grid of pending BUY limit-orders (below current price). Parameters format: l(ots)=[L_int,...] p(rices)=[P_float,...]. Counts of values in lots and prices lists must be equals!")
    # parser.add_argument("--sell-limit-order-grid", type=str, nargs="*", help="Action: open grid of pending SELL limit-orders (above current price). Parameters format: l(ots)=[L_int,...] p(rices)=[P_float,...]. Counts of values in lots and prices lists must be equals!")

    parser.add_argument("--close-order", "--cancel-order", type=str, nargs=1, help="Action: close only one order by it's `orderId` or `stopOrderId`. You can find out the meaning of these IDs using the key `--overview`.")
    parser.add_argument("--close-orders", "--cancel-orders", type=str, nargs="+", help="Action: close one or list of orders by it's `orderId` or `stopOrderId`. You can find out the meaning of these IDs using the key `--overview`.")
    parser.add_argument("--close-trade", "--cancel-trade", action="store_true", help="Action: close only one position for instrument defined by `--ticker` (high priority) or `--figi` keys, including for currencies tickers.")
    parser.add_argument("--close-trades", "--cancel-trades", type=str, nargs="+", help="Action: close positions for list of tickers or FIGIs, including for currencies tickers or FIGIs.")
    parser.add_argument("--close-all", "--cancel-all", type=str, nargs="*", help="Action: close all available (not blocked) opened trades and orders, excluding for currencies. Also you can select one or more keywords case insensitive to specify trades type: `orders`, `shares`, `bonds`, `etfs` and `futures`, but not `currencies`. Currency positions you must closes manually using `--buy`, `--sell`, `--close-trade` or `--close-trades` operations. If the `--close-all` key present with the `--ticker` or `--figi` keys, then positions and all open limit and stop orders for the specified instrument are closed.")

    parser.add_argument("--limits", "--withdrawal-limits", "-w", action="store_true", help="Action: show table of funds available for withdrawal for current `accountId`. You can change `accountId` with the key `--account-id`. Also, you can define `--output` key to save this information to file, default: `limits.md`.")
    parser.add_argument("--user-info", "-u", action="store_true", help="Action: show all available user's data (`accountId`s, common user information, margin status and tariff connections limit). Also, you can define `--output` key to save this information to file, default: `user-info.md`.")
    parser.add_argument("--account", "--accounts", "-a", action="store_true", help="Action: show simple table with all available user accounts. Also, you can define `--output` key to save this information to file, default: `accounts.md`.")

    cmdArgs = parser.parse_args()
    return cmdArgs


def Main(**kwargs):
    """
    Main function for work with TKSBrokerAPI in the console.

    See examples:
    - in english: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md
    - in russian: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md

    [![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)
    """
    args = Args(**kwargs) if kwargs else ParseArgs()  # get and parse command-line parameters or use **kwarg parameters

    if args.debug_level:
        uLogger.level = 10  # always debug level by default
        uLogger.handlers[0].level = args.debug_level  # level for STDOUT

    exitCode = 0
    start = datetime.now(tzutc())
    uLogger.debug("=-" * 50)
    uLogger.debug(">>> TKSBrokerAPI module started at: [{}] UTC, it is [{}] local time".format(
        start.strftime(TKS_PRINT_DATE_TIME_FORMAT),
        start.astimezone(tzlocal()).strftime(TKS_PRINT_DATE_TIME_FORMAT),
    ))

    # trying to calculate full current version:
    buildVersion = __version__
    try:
        v = version("tksbrokerapi")
        buildVersion = v if v.startswith(buildVersion) else buildVersion + ".dev0"  # set version as major.minor.dev0 if run as local build or local script

    except Exception:
        buildVersion = __version__ + ".dev0"  # if an errors occurred then also set version as major.minor.dev0

    uLogger.debug("TKSBrokerAPI major.minor.build version used: [{}]".format(buildVersion))
    uLogger.debug("Host CPU count: [{}]".format(CPU_COUNT))

    try:
        if args.version:
            print("TKSBrokerAPI {}".format(buildVersion))
            uLogger.debug("User requested current TKSBrokerAPI major.minor.build version: [{}]".format(buildVersion))

        else:
            # Init class for trading with Tinkoff Broker:
            trader = TinkoffBrokerServer(
                token=args.token,
                accountId=args.account_id,
                useCache=not args.no_cache,
            )

            if args.tag is not None:
                trader.tag = args.tag  # Identification TKSBrokerAPI tag in log messages to simplify debugging when platform instances runs in parallel mode

            # --- set some options:

            if args.more:
                trader.moreDebug = True
                uLogger.warning("More debug info mode is enabled! See network requests, responses and its headers in the full log or run TKSBrokerAPI platform with the `--verbosity 10` to show theres in console.")

            if args.html:
                trader.useHTMLReports = True

            if args.ticker:
                ticker = str(args.ticker).upper()  # Tickers may be upper case only

                if ticker in trader.aliasesKeys:
                    trader.ticker = trader.aliases[ticker]  # Replace some tickers with its aliases

                else:
                    trader.ticker = ticker

            if args.figi:
                trader.figi = str(args.figi).upper()  # FIGIs may be upper case only

            if args.depth is not None:
                trader.depth = args.depth

            # --- do one command:

            if args.list:
                if args.output is not None:
                    trader.instrumentsFile = args.output

                trader.ShowInstrumentsInfo(show=True)

            elif args.list_xlsx:
                trader.DumpInstrumentsAsXLSX(forceUpdate=False)

            elif args.bonds_xlsx is not None:
                if args.output is not None:
                    trader.bondsXLSXFile = args.output

                if len(args.bonds_xlsx) == 0:
                    trader.ExtendBondsData(instruments=trader.iList["Bonds"].keys(), xlsx=True)  # request bonds with all available tickers

                else:
                    trader.ExtendBondsData(instruments=args.bonds_xlsx, xlsx=True)  # request list of given bonds

            elif args.search:
                if args.output is not None:
                    trader.searchResultsFile = args.output

                trader.SearchInstruments(pattern=args.search[0], show=True)

            elif args.info:
                if not (args.ticker or args.figi):
                    uLogger.error("`--ticker` key or `--figi` key is required for this operation!")
                    raise Exception("Ticker or FIGI required")

                if args.output is not None:
                    trader.infoFile = args.output

                if args.ticker:
                    trader.SearchByTicker(requestPrice=True, show=True)  # show info and current prices by ticker name

                else:
                    trader.SearchByFIGI(requestPrice=True, show=True)  # show info and current prices by FIGI id

            elif args.calendar is not None:
                if args.output is not None:
                    trader.calendarFile = args.output

                if len(args.calendar) == 0:
                    bondsData = trader.ExtendBondsData(instruments=trader.iList["Bonds"].keys(), xlsx=False)  # request bonds with all available tickers

                else:
                    bondsData = trader.ExtendBondsData(instruments=args.calendar, xlsx=False)  # request list of given bonds

                trader.ShowBondsCalendar(extBonds=bondsData, show=True)  # shows bonds payment calendar only

            elif args.price:
                if not (args.ticker or args.figi):
                    uLogger.error("`--ticker` key or `--figi` key is required for this operation!")
                    raise Exception("Ticker or FIGI required")

                trader.GetCurrentPrices(show=True)

            elif args.prices is not None:
                if args.output is not None:
                    trader.pricesFile = args.output

                trader.GetListOfPrices(instruments=args.prices, show=True)  # WARNING: too long wait for a lot of instruments prices

            elif args.overview:
                if args.output is not None:
                    trader.overviewFile = args.output

                trader.Overview(show=True, details="full")

            elif args.overview_digest:
                if args.output is not None:
                    trader.overviewDigestFile = args.output

                trader.Overview(show=True, details="digest")

            elif args.overview_positions:
                if args.output is not None:
                    trader.overviewPositionsFile = args.output

                trader.Overview(show=True, details="positions")

            elif args.overview_orders:
                if args.output is not None:
                    trader.overviewOrdersFile = args.output

                trader.Overview(show=True, details="orders")

            elif args.overview_analytics:
                if args.output is not None:
                    trader.overviewAnalyticsFile = args.output

                trader.Overview(show=True, details="analytics")

            elif args.overview_calendar:
                if args.output is not None:
                    trader.overviewAnalyticsFile = args.output

                trader.Overview(show=True, details="calendar")

            elif args.deals is not None:
                if args.output is not None:
                    trader.reportFile = args.output

                if 0 <= len(args.deals) < 3:
                    trader.Deals(
                        start=args.deals[0] if len(args.deals) >= 1 else None,
                        end=args.deals[1] if len(args.deals) == 2 else None,
                        show=True,  # Always show deals report in console
                        showCancelled=not args.no_cancelled,  # If --no-cancelled key then remove cancelled operations from the deals report. False by default.
                    )

                else:
                    uLogger.error("You must specify 0-2 parameters: [DATE_START] [DATE_END]")
                    raise Exception("Incorrect value")

            elif args.history is not None:
                if args.output is not None:
                    trader.historyFile = args.output

                if 0 <= len(args.history) < 3:
                    dataReceived = trader.History(
                        start=args.history[0] if len(args.history) >= 1 else None,
                        end=args.history[1] if len(args.history) == 2 else None,
                        interval="hour" if args.interval is None or not args.interval else args.interval,
                        onlyMissing=False if args.only_missing is None or not args.only_missing else args.only_missing,
                        csvSep="," if args.csv_sep is None or not args.csv_sep else args.csv_sep,
                        show=True,  # shows all downloaded candles in console
                    )

                    if args.render_chart is not None and dataReceived is not None:
                        iChart = False if args.render_chart.lower() == "ni" or args.render_chart.lower() == "non-interact" else True

                        trader.ShowHistoryChart(
                            candles=dataReceived,
                            interact=iChart,
                            openInBrowser=False,  # False by default, to avoid issues with `permissions denied` to html-file.
                        )

                else:
                    uLogger.error("You must specify 0-2 parameters: [DATE_START] [DATE_END]")
                    raise Exception("Incorrect value")

            elif args.load_history is not None:
                histData = trader.LoadHistory(filePath=args.load_history)  # load data from file and show history in console

                if args.render_chart is not None and histData is not None:
                    iChart = False if args.render_chart.lower() == "ni" or args.render_chart.lower() == "non-interact" else True
                    trader.ticker = os.path.basename(args.load_history)  # use filename as ticker name for PriceGenerator's chart

                    trader.ShowHistoryChart(
                        candles=histData,
                        interact=iChart,
                        openInBrowser=False,  # False by default, to avoid issues with `permissions denied` to html-file.
                    )

            elif args.trade is not None:
                if 1 <= len(args.trade) <= 5:
                    trader.Trade(
                        operation=args.trade[0],
                        lots=int(args.trade[1]) if len(args.trade) >= 2 else 1,
                        tp=float(args.trade[2]) if len(args.trade) >= 3 else 0.,
                        sl=float(args.trade[3]) if len(args.trade) >= 4 else 0.,
                        expDate=args.trade[4] if len(args.trade) == 5 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 1-5 parameters to open trade: [direction `Buy` or `Sell`] [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

            elif args.buy is not None:
                if 0 <= len(args.buy) <= 4:
                    trader.Buy(
                        lots=int(args.buy[0]) if len(args.buy) >= 1 else 1,
                        tp=float(args.buy[1]) if len(args.buy) >= 2 else 0.,
                        sl=float(args.buy[2]) if len(args.buy) >= 3 else 0.,
                        expDate=args.buy[3] if len(args.buy) == 4 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 0-4 parameters to open buy position: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

            elif args.sell is not None:
                if 0 <= len(args.sell) <= 4:
                    trader.Sell(
                        lots=int(args.sell[0]) if len(args.sell) >= 1 else 1,
                        tp=float(args.sell[1]) if len(args.sell) >= 2 else 0.,
                        sl=float(args.sell[2]) if len(args.sell) >= 3 else 0.,
                        expDate=args.sell[3] if len(args.sell) == 4 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 0-4 parameters to open sell position: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

            elif args.order:
                if 4 <= len(args.order) <= 7:
                    trader.Order(
                        operation=args.order[0],
                        orderType=args.order[1],
                        lots=int(args.order[2]),
                        targetPrice=float(args.order[3]),
                        limitPrice=float(args.order[4]) if len(args.order) >= 5 else 0.,
                        stopType=args.order[5] if len(args.order) >= 6 else "Limit",
                        expDate=args.order[6] if len(args.order) == 7 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 4-7 parameters to open order: [direction `Buy` or `Sell`] [order type `Limit` or `Stop`] [lots] [target price] [maybe for stop-order: [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d %H:%M:%S`]]. See: `python TKSBrokerAPI.py --help`")

            elif args.buy_limit:
                trader.BuyLimit(lots=int(args.buy_limit[0]), targetPrice=args.buy_limit[1])

            elif args.sell_limit:
                trader.SellLimit(lots=int(args.sell_limit[0]), targetPrice=args.sell_limit[1])

            elif args.buy_stop:
                if 2 <= len(args.buy_stop) <= 7:
                    trader.BuyStop(
                        lots=int(args.buy_stop[0]),
                        targetPrice=float(args.buy_stop[1]),
                        limitPrice=float(args.buy_stop[2]) if len(args.buy_stop) >= 3 else 0.,
                        stopType=args.buy_stop[3] if len(args.buy_stop) >= 4 else "Limit",
                        expDate=args.buy_stop[4] if len(args.buy_stop) == 5 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 2-5 parameters for buy stop-order: [lots] [target price] [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

            elif args.sell_stop:
                if 2 <= len(args.sell_stop) <= 7:
                    trader.SellStop(
                        lots=int(args.sell_stop[0]),
                        targetPrice=float(args.sell_stop[1]),
                        limitPrice=float(args.sell_stop[2]) if len(args.sell_stop) >= 3 else 0.,
                        stopType=args.sell_stop[3] if len(args.sell_stop) >= 4 else "Limit",
                        expDate=args.sell_stop[4] if len(args.sell_stop) == 5 else "Undefined",
                    )

                else:
                    uLogger.error("You must specify 2-5 parameters for sell stop-order: [lots] [target price] [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d %H:%M:%S`]. See: python TKSBrokerAPI.py --help")

            # elif args.buy_order_grid is not None:
            #     # update order grid work with api v2
            #     if len(args.buy_order_grid) == 2:
            #         orderParams = trader.ParseOrderParameters(operation="Buy", **dict(kw.split('=') for kw in args.buy_order_grid))
            #
            #         for order in orderParams:
            #             trader.Order(operation="Buy", lots=order["lot"], price=order["price"])
            #
            #     else:
            #         uLogger.error("To open grid of pending BUY limit-orders (below current price) you must specified 2 parameters: l(ots)=[L_int,...] p(rices)=[P_float,...]. See: `python TKSBrokerAPI.py --help`")
            #
            # elif args.sell_order_grid is not None:
            #     # update order grid work with api v2
            #     if len(args.sell_order_grid) >= 2:
            #         orderParams = trader.ParseOrderParameters(operation="Sell", **dict(kw.split('=') for kw in args.sell_order_grid))
            #
            #         for order in orderParams:
            #             trader.Order(operation="Sell", lots=order["lot"], price=order["price"])
            #
            #     else:
            #         uLogger.error("To open grid of pending SELL limit-orders (above current price) you must specified 2 parameters: l(ots)=[L_int,...] p(rices)=[P_float,...]. See: `python TKSBrokerAPI.py --help`")

            elif args.close_order is not None:
                trader.CloseOrders(args.close_order)  # close only one order

            elif args.close_orders is not None:
                trader.CloseOrders(args.close_orders)  # close list of orders

            elif args.close_trade:
                if not (args.ticker or args.figi):
                    uLogger.error("`--ticker` key or `--figi` key is required for this operation!")
                    raise Exception("Ticker or FIGI required")

                if args.ticker:
                    trader.CloseTrades([str(args.ticker).upper()])  # close only one trade by ticker (priority)

                else:
                    trader.CloseTrades([str(args.figi).upper()])  # close only one trade by FIGI

            elif args.close_trades is not None:
                trader.CloseTrades(args.close_trades)  # close trades for list of tickers

            elif args.close_all is not None:
                if args.ticker:
                    trader.CloseAllByTicker(instrument=str(args.ticker).upper())

                elif args.figi:
                    trader.CloseAllByFIGI(instrument=str(args.figi).upper())

                else:
                    trader.CloseAll(*args.close_all)

            elif args.limits:
                if args.output is not None:
                    trader.withdrawalLimitsFile = args.output

                trader.OverviewLimits(show=True)

            elif args.user_info:
                if args.output is not None:
                    trader.userInfoFile = args.output

                trader.OverviewUserInfo(show=True)

            elif args.account:
                if args.output is not None:
                    trader.userAccountsFile = args.output

                trader.OverviewAccounts(show=True)

            else:
                uLogger.error("There is no command to execute! One of the possible commands must be selected. See help with `--help` key.")
                raise Exception("There is no command to execute")

    except Exception:
        trace = tb.format_exc()
        uLogger.debug(trace)

        for e in ["socket.gaierror", "nodename nor servname provided", "or not known", "NewConnectionError", "[Errno 8]", "Failed to establish a new connection"]:
            if e in trace:
                uLogger.error("Check your Internet connection! Failed to establish connection to broker server!")
                break

        uLogger.debug("Please, check issues or request a new one at https://github.com/Tim55667757/TKSBrokerAPI/issues")
        exitCode = 255  # an error occurred, must be open a ticket for this issue

    finally:
        finish = datetime.now(tzutc())

        if exitCode == 0:
            if args.more:
                uLogger.debug("All operations were finished success (summary code is 0).")

        else:
            uLogger.error("An issue occurred with TKSBrokerAPI module! See full debug log in [{}] or run TKSBrokerAPI once again with the key `--debug-level 10`. Summary code: {}".format(
                os.path.abspath(uLog.defaultLogFile), exitCode,
            ))

        uLogger.debug(">>> TKSBrokerAPI module work duration: [{}]".format(finish - start))
        uLogger.debug(">>> TKSBrokerAPI module finished: [{} UTC], it is [{}] local time".format(
            finish.strftime(TKS_PRINT_DATE_TIME_FORMAT),
            finish.astimezone(tzlocal()).strftime(TKS_PRINT_DATE_TIME_FORMAT),
        ))
        uLogger.debug("=-" * 50)

        if not kwargs:
            sys.exit(exitCode)

        else:
            return exitCode


if __name__ == "__main__":
    Main()
