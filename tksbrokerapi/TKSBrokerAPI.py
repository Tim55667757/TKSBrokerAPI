# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
**TKSBrokerAPI** is a python API to work with some methods of Tinkoff Open API using REST protocol.
It can view history, orders and market information. Also, you can open orders and trades.

If you run this module as CLI program then it realizes simple logic: receiving a lot of options and execute one command.
**See examples**: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Usage-examples

**Used constants are in the TKSEnums module**: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSEnums.html

About Tinkoff Invest API: https://tinkoff.github.io/investAPI/

Tinkoff Invest API documentation: https://tinkoff.github.io/investAPI/swagger-ui/
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

from datetime import datetime, timedelta
from dateutil.tz import tzlocal, tzutc
from time import sleep

import re
import json
import requests
from urllib.parse import quote
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import pandas as pd

import UniLogger as uLog
import traceback as tb

from TKSEnums import *  # a lot of constants from enums sections: https://tinkoff.github.io/investAPI/swagger-ui/


# --- Common technical parameters:

uLogger = uLog.UniLogger
uLogger.level = 10  # debug level by default
uLogger.handlers[0].level = 20  # info level by default for STDOUT

CPU_COUNT = cpu_count()  # host's real CPU count
CPU_USAGES = CPU_COUNT - 1 if CPU_COUNT > 1 else 1  # how many CPUs will be used for parallel calculations
uLogger.debug("Host CPU count: [{}]".format(CPU_COUNT))

# --- Main constants:

NANO = 0.000000001  # SI-constant nano = 10^-9


def NanoToFloat(units: str, nano: int) -> float:
    """
    Convert number in nano-view mode with string parameter `units` and integer parameter `nano` to float view. Examples:

    `NanoToFloat(units="2", nano=500000000) -> 2.5`

    `NanoToFloat(units="0", nano=50000000) -> 0.05`

    :param units: integer string or integer parameter that represents the integer part of number
    :param nano: integer string or integer parameter that represents the fractional part of number
    :return: float view of number
    """
    return int(units) + int(nano) * NANO


def FloatToNano(number: float) -> dict:
    """
    Convert float number to nano-type view: dictionary with string `units` and integer `nano` parameters `{"units": "string", "nano": integer}`. Examples:

    `FloatToNano(number=2.5) -> {"units": "2", "nano": 500000000}`

    `FloatToNano(number=0.05) -> {"units": "0", "nano": 50000000}`

    :param number: float number
    :return: nano-type view of number: `{"units": "string", "nano": integer}`
    """
    splitByPoint = str(number).split(".")
    frac = 0

    if len(splitByPoint) > 1:
        if len(splitByPoint[1]) <= 9:
            frac = int("{}{}".format(
                int(splitByPoint[1]),
                "0" * (9 - len(splitByPoint[1])),
            ))

    if (number < 0) and (frac > 0):
        frac = -frac

    return {"units": str(int(number)), "nano": frac}


def GetDatesAsString(start: str = None, end: str = None) -> tuple:
    """
    If `start=None`, `end=None` then return dates from yesterday to current time.
    If `start=some_date_1`, `end=None` then return dates from `some_date_1` to current time.
    If `start=some_date_1`, `end=some_date_2` then return dates from `some_date_1` to `some_date_2`.
    Start day may be negative integer numbers: `-1`, `-2`, `-3` - how many days ago.

    Also, you can use keywords for start if `dateEnd=None`:
    `today` (from 00:00:00 to current time),
    `yesterday` (-1 day from 00:00:00 to 23:59:59),
    `week` (-7 day from 00:00:00 to current date and time),
    `month` (-30 day from 00:00:00 to current date and time),
    `year` (-365 day from 00:00:00 to current date and time),

    User dates format must be like: `%Y-%m-%d`, e.g. `2020-02-03` (3 Feb, 2020).

    :return: tuple with 2 strings `(start, end)` dates in UTC ISO time format `%Y-%m-%dT%H:%M:%SZ` for OpenAPI.
             Example: `("2022-06-01T00:00:00Z", "2022-06-20T23:59:59Z")`
    """
    uLogger.debug("Input start day is [{}] (UTC), end day is [{}] (UTC)".format(start, end))
    now = datetime.now(tzutc())

    # showing statistics between start of the current day and current time:
    if start is None or start.lower() == "today":
        s = now.replace(hour=0, minute=0, second=0, microsecond=0)
        e = now

    # from start of the last day to the end of the last day:
    elif start.lower() == "yesterday":
        s = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        e = now.replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)

    # week (-7 day from 00:00:00 to current date and time):
    elif start.lower() == "week":
        s = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        e = now

    # month (-30 day from 00:00:00 to current date and time):
    elif start.lower() == "month":
        s = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)
        e = now

    # year (-365 day from 00:00:00 to current date and time):
    elif start.lower() == "year":
        s = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=365)
        e = now

    # showing statistics from -N days ago to current date and time:
    elif start.startswith('-') and start[1:].isdigit():
        s = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=abs(int(start)))
        e = now

    # showing statistics between start day at 00:00:00 and the end day at 23:59:59:
    else:
        s = datetime.strptime(start, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc())
        e = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=tzutc()) if end is not None else now

    # converting to UTC ISO time formatted with Z suffix for Tinkoff Open API:
    s = s.strftime("%Y-%m-%dT%H:%M:%SZ")
    e = e.strftime("%Y-%m-%dT%H:%M:%SZ")

    uLogger.debug("Tinkoff Open API uses this start day (converted to UTC ISO format, with Z): [{}], and the end day: [{}]".format(s, e))

    return s, e


class TinkoffBrokerServer:
    """
    This class implements methods to work with Tinkoff broker server.

    Examples to work with API: https://tinkoff.github.io/investAPI/swagger-ui/

    About `token`: https://tinkoff.github.io/investAPI/token/
    """
    def __init__(self, token: str, accountId: str = None, iList: dict = None, useCache: bool = True) -> None:
        """
        Main class init.

        :param token: Bearer token for Tinkoff Invest API. It can be set from environment variable `TKS_API_TOKEN`.
        :param accountId: string with user's numeric account ID in Tinkoff Broker. It can be found in broker's reports.
                          Also, this variable can be set from environment variable `TKS_ACCOUNT_ID`.
        :param iList: dictionary with raw data about shares, currencies, bonds, etfs and futures from broker server.
                      At first time, when class init, `Listing()` method auto-update this variable, or you can use dump file.
                      For future use, you can save this variable and use as `iList` to avoid permanent downloads
                      from the server. Also, you can try `DumpInstruments()` method.
        :param useCache: use default cache file `dump.json` with raw data to use instead of `iList` if `iList` set as `None`.
                         True by default. Cache is auto-update if new day has come.
                         If `iList` is not `None` then it value has higher priority than `dump.json` and `useCache`.
                         If you don't want to use cache and always updates raw data then set `useCache=False`.
        """
        if token is None or not token:
            try:
                self.token = r"{}".format(os.environ["TKS_API_TOKEN"])
                uLogger.debug("Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/")

            except KeyError:
                raise Exception("`--token` key or environment variable `TKS_API_TOKEN` is required! See https://tinkoff.github.io/investAPI/token/")

        else:
            self.token = token  # highly priority than environment variable 'TKS_API_TOKEN'
            uLogger.debug("Bearer token for Tinkoff OpenApi set up from class variable `token`")

        if accountId is None or not accountId:
            try:
                self.accountId = r"{}".format(os.environ["TKS_ACCOUNT_ID"])
                uLogger.debug("String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`")

            except KeyError:
                uLogger.warning("`--account-id` key or environment variable `TKS_ACCOUNT_ID` undefined! Some of operations may be unavailable (overview, trading etc).")

        else:
            self.accountId = accountId  # highly priority than environment variable 'TKS_ACCOUNT_ID'
            uLogger.debug("String with user's numeric account ID in Tinkoff Broker set up from class variable `accountId`")

        self.aliases = TKS_TICKER_ALIASES
        """Some aliases instead official tickers. See `TKSEnums.TKS_TICKER_ALIASES`"""

        self.aliasesKeys = self.aliases.keys()  # re-calc only first time at class init
        self.exclude = TKS_TICKERS_OR_FIGI_EXCLUDED  # some of tickets or FIGIs raised exception earlier when it sends to server, that is why we exclude there

        self.ticker = ""
        """String with ticker, e.g. `GOOGL`. Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR` etc. More tickers aliases here: `TKSEnums.TKS_TICKER_ALIASES`."""

        self.figi = ""
        """String with FIGI, e.g. ticker `GOOGL` has FIGI `BBG009S39JX6`"""

        self.depth = 1
        """Depth of Market (DOM) can be >= 1. Default: 1. It used with `--price` key to showing DOM with current prices for givens ticker or FIGI."""

        self.server = r"https://invest-public-api.tinkoff.ru/rest"
        """Tinkoff REST API server for real trade operations. Default: https://invest-public-api.tinkoff.ru/rest

        See also: https://tinkoff.github.io/investAPI/#tinkoff-invest-api_1
        """

        uLogger.debug("Broker API server: {}".format(self.server))

        self.timeout = 15
        """Server operations timeout in seconds. Default: 15"""

        self.headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": "Bearer {}".format(self.token)}
        """Headers which send in every request to broker server. Default: `{"Content-Type": "application/json", "accept": "application/json", "Authorization": "Bearer {token}"}`"""

        self.body = None
        """Request body which send to broker server. Default: `None`"""

        self.historyLength = 24
        """How many candles returns if candles history request. For example, if `historyInterval="hour"` and `historyLength=24` it means: "give me last 24 hours". Must be >=1. Default: 24"""

        self.historyInterval = "hour"
        """Interval string for Tinkoff API (see: `TKSEnums.TKS_TIMEFRAMES`). Available values are `"1min"`, `"2min"`, `"3min"`, `"5min"`, `"10min"`, `"15min"`, `"30min"`, `"hour"`, `"day"`, `"week"`, `"month"`. Default: `"hour"`"""

        self.instrumentsFile = "instruments.md"
        """Filename where full broker's instruments list will be saved. Default: `instruments.md`"""

        self.searchResultsFile = "search-results.md"
        """Filename with all found instruments searched by part of its ticker, FIGI or name. Default: `search-results.md`"""

        self.pricesFile = "prices.md"
        """Filename where prices of selected instruments will be saved. Default: `prices.md`"""

        self.overviewFile = "overview.md"
        """Filename where current portfolio, open trades and orders will be saved. Default: `overview.md`"""

        self.reportFile = "deals.md"
        """Filename where history of deals and trade statistics will be saved. Default: `deals.md`"""

        self.historyFile = None
        """Full path to .csv output file where history candles will be saved. Default: `None`, mean that returns only pandas dataframe."""

        self.iListDumpFile = "dump.json"
        """Filename where raw data about shares, currencies, bonds, etfs and futures will be stored. Default: `dump.json`"""

        self.iList = None  # init iList
        """Dictionary with raw data about shares, currencies, bonds, etfs and futures from broker server. Auto-updating.
        
        See also: `Listing()` and `DumpInstruments()`.
        """

        # try to re-use raw instruments data saved as `iList` or try to load it from the dump file:
        if iList is not None and isinstance(iList, dict):
            uLogger.debug("Instruments raw data set up from given `iList` variable. Dump file not updated.")

            self.iList = iList  # only used given iList, dump not updated

        elif useCache:
            if os.path.exists(self.iListDumpFile):
                dumpTime = datetime.fromtimestamp(os.path.getmtime(self.iListDumpFile)).astimezone(tzutc())  # dump modification date and time
                curTime = datetime.now(tzutc())

                if (curTime.day > dumpTime.day) or (curTime.month > dumpTime.month) or (curTime.year > dumpTime.year):
                    uLogger.warning("Local cache may be outdated! It has last modified [{}] UTC. Updating from broker server, wait, please...".format(dumpTime.strftime("%Y-%m-%d %H:%M:%S")))

                    self.DumpInstruments(forceUpdate=True)  # updating self.iList and dump file

                else:
                    self.iList = json.load(open(self.iListDumpFile, mode="r", encoding="UTF-8"))  # load iList from dump

                    uLogger.debug("Local cache with raw instruments data is used: [{}]".format(os.path.abspath(self.iListDumpFile)))
                    uLogger.debug("Dump file was modified [{}] UTC".format(dumpTime.strftime("%Y-%m-%d %H:%M:%S")))

            else:
                uLogger.warning("Local cache with raw instruments data not exists! Creating new dump, wait, please...")
                self.DumpInstruments(forceUpdate=True)  # updating self.iList and creating default dump file

        else:
            self.iList = self.Listing()  # request new raw instruments data from broker server
            self.DumpInstruments(forceUpdate=False)  # save updated info to default dump file

    @staticmethod
    def _ParseJSON(rawData="{}", debug: bool = False) -> dict:
        """
        Parse JSON from response string.

        :param rawData: this is a string with JSON-formatted text.
        :param debug: if `True` then print more debug information.
        :return: JSON (dictionary), parsed from server response string.
        """
        if debug:
            uLogger.debug("Raw text body:")
            uLogger.debug(rawData)

        responseJSON = json.loads(rawData) if rawData else {}

        if debug:
            uLogger.debug("JSON formatted:")
            for jsonLine in json.dumps(responseJSON, indent=4).split('\n'):
                uLogger.debug(jsonLine)

        return responseJSON

    def SendAPIRequest(self, url: str, reqType: str = "GET", retry: int = 3, pause: int = 5, debug: bool = False) -> dict:
        """
        Send GET or POST request to broker server and receive JSON object.

        self.header: must be define with dictionary of headers.
        self.body: if define then used as request body. None by default.
        self.timeout: global request timeout, 15 seconds by default.
        :param url: url with REST request.
        :param reqType: send "GET" or "POST" request. "GET" by default.
        :param retry: how many times retry after first request if an error occurred.
        :param pause: sleep time in seconds between retries.
        :param debug: if `True` then print more debug information.
        :return: response JSON (dictionary) from broker.
        """
        if reqType not in ("GET", "POST"):
            raise Exception("You can define request type: 'GET' or 'POST'!")

        if debug:
            uLogger.debug("Request parameters:")
            uLogger.debug("    - REST API URL: {}".format(url))
            uLogger.debug("    - request type: {}".format(reqType))
            uLogger.debug("    - headers: {}".format(str(self.headers).replace(self.token, "*** request token ***")))
            uLogger.debug("    - body: {}".format(self.body))

        # fast hack to avoid all operations with some tickers/FIGI
        responseJSON = {}
        oK = True
        for item in self.exclude:
            if item in url:
                if debug:
                    uLogger.warning("Do not execute operations with list of this tickers/FIGI: {}".format(str(self.exclude)))

                oK = False
                break

        if oK:
            counter = 0
            response = None
            errMsg = ""

            while not response and counter <= retry:
                if reqType == "GET":
                    response = requests.get(url, headers=self.headers, data=self.body, timeout=self.timeout)

                if reqType == "POST":
                    response = requests.post(url, headers=self.headers, data=self.body, timeout=self.timeout)

                if debug:
                    uLogger.debug("Response:")
                    uLogger.debug("    - status code: {}".format(response.status_code))
                    uLogger.debug("    - reason: {}".format(response.reason))
                    uLogger.debug("    - body length: {}".format(len(response.text)))

                # Error status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                if 400 <= response.status_code < 600:
                    errMsg = "[{}] {}".format(response.status_code, response.text)
                    uLogger.debug("    - not oK status code received: {}".format(errMsg))
                    counter += 1

                    if counter <= retry:
                        uLogger.debug("Retry: [{}]. Wait until {} sec. and try again...".format(counter, pause))
                        sleep(pause)

            responseJSON = self._ParseJSON(response.text)

            if errMsg:
                uLogger.error("Not `oK` status received from broker server!")
                uLogger.error("    - message: {}".format(errMsg))
                # raise Exception("Server returned an error! See full debug log. Also you can set debug=True in SendAPIRequest() and _ParseJSON() methods.")

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
            result = self.SendAPIRequest(instrumentURL, reqType="POST", debug=False)["instruments"]

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
        uLogger.debug("Requesting all available instruments from broker for current user token. Wait, please...")
        uLogger.debug("CPU usages for parallel requests: [{}]".format(CPU_USAGES))

        # this parameters insert to requests: https://tinkoff.github.io/investAPI/swagger-ui/#/InstrumentsService
        # iType is type of instrument, it must be one of supported types in TKS_INSTRUMENTS list.
        iParams = [{"iType": iType} for iType in TKS_INSTRUMENTS]

        poolUpdater = ThreadPool(processes=CPU_USAGES)  # create pool for update instruments in parallel mode
        listing = poolUpdater.map(self._IWrapper, iParams)  # execute update operations
        poolUpdater.close()

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

    def DumpInstruments(self, forceUpdate: bool = True) -> str:
        """
        Receives and returns actual raw data about shares, currencies, bonds, etfs and futures from broker server
        using `Listing()` method. If `iListDumpFile` string is not empty then also save information to this file.

        :param forceUpdate: if `True` then at first updates data with `Listing()` method, otherwise just saves exist `iList`.
        :return: serialized JSON formatted `str` with full data of instruments, also saved to the `--output` file.
        """
        if self.iListDumpFile is None or not self.iListDumpFile:
            raise Exception("Output name of dump file must be defined!")

        if not self.iList or forceUpdate:
            self.iList = self.Listing()

        dump = json.dumps(self.iList, indent=4, sort_keys=False)
        with open(self.iListDumpFile, mode="w", encoding="UTF-8") as fH:
            fH.write(dump)

        uLogger.info("Instruments raw data were cached for future used: [{}]".format(os.path.abspath(self.iListDumpFile)))

        return dump

    @staticmethod
    def ShowInstrumentInfo(iJSON: dict, printInfo: bool = False) -> str:
        """
        Show information about instrument defined by json and print in Markdown format.

        :param iJSON: json data of instrument, e.g. in code `iJSON = self.iList["Shares"][self.ticker]`
        :param printInfo: if `True` then also printing information about instrument and its current price.
        :return: text in Markdown format with information about instrument.
        """
        infoText = ""
        if iJSON is not None and iJSON and isinstance(iJSON, dict):
            info = [
                "# Information is actual at: [{}] (UTC)\n\n".format(datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M")),
                "| Parameters                                              | Values\n",
                "|---------------------------------------------------------|---------------------------------------------------------\n",
                "| Ticker:                                                 | {}\n".format(iJSON["ticker"]),
                "| Full name:                                              | {}\n".format(iJSON["name"]),
            ]

            if "sector" in iJSON.keys() and iJSON["sector"]:
                info.append("| Sector:                                                 | {}\n".format(iJSON["sector"]))

            info.append("| Country of instrument:                                  | {}{}\n".format(
                "({}) ".format(iJSON["countryOfRisk"]) if "countryOfRisk" in iJSON.keys() and iJSON["countryOfRisk"] else "",
                iJSON["countryOfRiskName"] if "countryOfRiskName" in iJSON.keys() and iJSON["countryOfRiskName"] else "",
            ))

            info.extend([
                "|                                                         |\n",
                "| FIGI (Financial Instrument Global Identifier):          | {}\n".format(iJSON["figi"]),
                "| Exchange:                                               | {}\n".format(iJSON["exchange"]),
            ])

            if "isin" in iJSON.keys() and iJSON["isin"]:
                info.append("| ISIN (International Securities Identification Number):  | {}\n".format(iJSON["isin"]))

            if "classCode" in iJSON.keys():
                info.append("| Class Code:                                             | {}\n".format(iJSON["classCode"]))

            info.extend([
                "|                                                         |\n",
                "| Current broker security trading status:                 | {}\n".format(TKS_TRADING_STATUSES[iJSON["tradingStatus"]]),
                "| Buy operations allowed:                                 | {}\n".format("Yes" if iJSON["buyAvailableFlag"] else "No"),
                "| Sale operations allowed:                                | {}\n".format("Yes" if iJSON["sellAvailableFlag"] else "No"),
                "| Short positions allowed:                                | {}\n".format("Yes" if iJSON["shortEnabledFlag"] else "No"),
            ])

            info.append("|                                                         |\n")

            if "type" in iJSON.keys() and iJSON["type"]:
                info.append("| Type of the instrument:                                 | {}\n".format(iJSON["type"]))

            if "futuresType" in iJSON.keys() and iJSON["futuresType"]:
                info.append("| Futures type:                                           | {}\n".format(iJSON["futuresType"]))

            if "ipoDate" in iJSON.keys() and iJSON["ipoDate"]:
                info.append("| IPO date:                                               | {}\n".format(iJSON["ipoDate"].replace("T", " ").replace("Z", "")))

            if "releasedDate" in iJSON.keys() and iJSON["releasedDate"]:
                info.append("| Released date:                                          | {}\n".format(iJSON["releasedDate"].replace("T", " ").replace("Z", "")))

            if "rebalancingFreq" in iJSON.keys() and iJSON["rebalancingFreq"]:
                info.append("| Rebalancing frequency:                                  | {}\n".format(iJSON["rebalancingFreq"]))

            if "focusType" in iJSON.keys() and iJSON["focusType"]:
                info.append("| Focusing type:                                          | {}\n".format(iJSON["focusType"]))

            if "assetType" in iJSON.keys() and iJSON["assetType"]:
                info.append("| Asset type:                                             | {}\n".format(iJSON["assetType"]))

            if "basicAsset" in iJSON.keys() and iJSON["basicAsset"]:
                info.append("| Basic asset:                                            | {}\n".format(iJSON["basicAsset"]))

            if "basicAssetSize" in iJSON.keys() and iJSON["basicAssetSize"]:
                info.append("| Basic asset size:                                       | {:.2f}\n".format(NanoToFloat(str(iJSON["basicAssetSize"]["units"]), iJSON["basicAssetSize"]["nano"])))

            if "isoCurrencyName" in iJSON.keys() and iJSON["isoCurrencyName"]:
                info.append("| ISO currency name:                                      | {}\n".format(iJSON["isoCurrencyName"]))

            if "currency" in iJSON.keys():
                info.append("| Payment currency:                                       | {}\n".format(iJSON["currency"]))

            if "firstTradeDate" in iJSON.keys() and iJSON["firstTradeDate"] != 0:
                info.append("| First trade date:                                       | {}\n".format(iJSON["firstTradeDate"].replace("T", " ").replace("Z", "")))

            if "lastTradeDate" in iJSON.keys() and iJSON["lastTradeDate"] != 0:
                info.append("| Last trade date:                                        | {}\n".format(iJSON["lastTradeDate"].replace("T", " ").replace("Z", "")))

            if "expirationDate" in iJSON.keys() and iJSON["expirationDate"] != 0:
                info.append("| Date of expiration:                                     | {}\n".format(iJSON["expirationDate"].replace("T", " ").replace("Z", "")))

            if "stateRegDate" in iJSON.keys() and iJSON["stateRegDate"] != 0:
                info.append("| State registration date:                                | {}\n".format(iJSON["stateRegDate"].replace("T", " ").replace("Z", "")))

            if "placementDate" in iJSON.keys() and iJSON["placementDate"] != 0:
                info.append("| Placement date:                                         | {}\n".format(iJSON["placementDate"].replace("T", " ").replace("Z", "")))

            if "maturityDate" in iJSON.keys() and iJSON["maturityDate"] != 0:
                info.append("| Maturity date:                                          | {}\n".format(iJSON["maturityDate"].replace("T", " ").replace("Z", "")))

            if "perpetualFlag" in iJSON.keys() and iJSON["perpetualFlag"]:
                info.append("| Perpetual bond:                                         | Yes\n")

            if "otcFlag" in iJSON.keys() and iJSON["otcFlag"]:
                info.append("| Over-the-counter (OTC) securities:                      | Yes\n")

            if iJSON["type"] == "Bonds":
                info.append("| Bond issue (size / plan):                               | {} / {}\n".format(iJSON["issueSize"], iJSON["issueSizePlan"]))

                info.append("| Nominal price (100%):                                   | {:.2f} {}\n".format(
                    NanoToFloat(str(iJSON["nominal"]["units"]), iJSON["nominal"]["nano"]),
                    iJSON["nominal"]["currency"],
                ))

                if "floatingCouponFlag" in iJSON.keys():
                    info.append("| Floating coupon:                                        | {}\n".format("Yes" if iJSON["floatingCouponFlag"] else "No"))

                if "amortizationFlag" in iJSON.keys():
                    info.append("| Amortization:                                           | {}\n".format("Yes" if iJSON["amortizationFlag"] else "No"))

                if "couponQuantityPerYear" in iJSON.keys() and iJSON["couponQuantityPerYear"]:
                    info.append("| Number of coupon payments per year:                     | {}\n".format(iJSON["couponQuantityPerYear"]))

                if "aciValue" in iJSON.keys() and iJSON["aciValue"]:
                    info.append("| Current ACI (Accrued Interest):                         | {:.2f} {}\n".format(
                        NanoToFloat(str(iJSON["aciValue"]["units"]), iJSON["aciValue"]["nano"]),
                        iJSON["aciValue"]["currency"]
                    ))

            if "currentPrice" in iJSON.keys():
                info.append("|                                                         |\n")

                info.extend([
                    "| Previous close price of the instrument:                 | {}{}\n".format(
                        "{}".format(iJSON["currentPrice"]["closePrice"]).rstrip("0") if iJSON["currentPrice"]["closePrice"] is not None else "N/A",
                        "% of nominal price" if iJSON["type"] == "Bonds" else " {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                    ),
                    "| Last deal price of the instrument:                      | {}{}\n".format(
                        "{}".format(iJSON["currentPrice"]["lastPrice"]).rstrip("0") if iJSON["currentPrice"]["lastPrice"] is not None else "N/A",
                        "% of nominal price" if iJSON["type"] == "Bonds" else " {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                    ),
                    "| Changes between last deal price and last close  %       | {:.2f}%\n".format(iJSON["currentPrice"]["changes"]),
                    "| Current limit price, min / max:                         | {}{} / {}{}\n".format(
                        "{}".format(iJSON["currentPrice"]["limitDown"]).rstrip("0") if iJSON["currentPrice"]["limitDown"] is not None else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                        "{}".format(iJSON["currentPrice"]["limitUp"]).rstrip("0") if iJSON["currentPrice"]["limitUp"] is not None else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                    ),
                    "| Actual price, sell / buy:                               | {}{} / {}{}\n".format(
                        "{}".format(iJSON["currentPrice"]["sell"][0]["price"]).rstrip("0") if iJSON["currentPrice"]["sell"] else "N/A",
                        "%" if iJSON["type"] == "Bonds" else " {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                        "{}".format(iJSON["currentPrice"]["buy"][0]["price"]).rstrip("0") if iJSON["currentPrice"]["buy"] else "N/A",
                        "%" if iJSON["type"] == "Bonds" else" {}".format(iJSON["currency"] if "currency" in iJSON.keys() else ""),
                    ),
                ])

            if "lot" in iJSON.keys():
                info.append("| Minimum lot to buy:                                     | {}\n".format(iJSON["lot"]))

            if "step" in iJSON.keys() and iJSON["step"] != 0:
                info.append("| Minimum price increment (step):                         | {}\n".format(iJSON["step"]))

            infoText += "".join(info)

            if printInfo:
                uLogger.info("Information about instrument: ticker [{}], FIGI [{}]\n{}".format(iJSON["ticker"], iJSON["figi"], infoText))

            else:
                uLogger.debug("Information about instrument: ticker [{}], FIGI [{}]\n{}".format(iJSON["ticker"], iJSON["figi"], infoText))

        return infoText

    def SearchByTicker(self, requestPrice: bool = False, showInfo: bool = False, debug: bool = False) -> dict:
        """
        Search and return raw broker's information about instrument by it's ticker.
        `ticker` must be define! If debug=True then print all debug messages.

        :param requestPrice: if `False` then do not request current price of instrument (because this is long operation).
        :param showInfo: if `False` then do not run `ShowInstrumentInfo()` method and do not print info to the console.
        :param debug: if `True` then print all debug console messages.
        :return: JSON formatted data with information about instrument.
        """
        tickerJSON = {}
        if debug:
            uLogger.debug("Searching information about instrument by it's ticker [{}] ...".format(self.ticker))

        if not self.ticker:
            uLogger.warning("self.ticker variable is not be empty!")

        else:
            if not self.iList:
                self.iList = self.Listing()

            if self.ticker in self.iList["Shares"].keys():
                tickerJSON = self.iList["Shares"][self.ticker]
                if debug:
                    uLogger.debug("Ticker [{}] found in shares list".format(self.ticker))

            elif self.ticker in self.iList["Currencies"].keys():
                tickerJSON = self.iList["Currencies"][self.ticker]
                if debug:
                    uLogger.debug("Ticker [{}] found in currencies list".format(self.ticker))

            elif self.ticker in self.iList["Bonds"].keys():
                tickerJSON = self.iList["Bonds"][self.ticker]
                if debug:
                    uLogger.debug("Ticker [{}] found in bonds list".format(self.ticker))

            elif self.ticker in self.iList["Etfs"].keys():
                tickerJSON = self.iList["Etfs"][self.ticker]
                if debug:
                    uLogger.debug("Ticker [{}] found in etfs list".format(self.ticker))

            elif self.ticker in self.iList["Futures"].keys():
                tickerJSON = self.iList["Futures"][self.ticker]
                if debug:
                    uLogger.debug("Ticker [{}] found in futures list".format(self.ticker))

        if tickerJSON:
            self.figi = tickerJSON["figi"]

            if requestPrice:
                tickerJSON["currentPrice"] = self.GetCurrentPrices(showPrice=False)

                if tickerJSON["currentPrice"]["closePrice"] is not None and tickerJSON["currentPrice"]["closePrice"] != 0 and tickerJSON["currentPrice"]["lastPrice"] is not None:
                    tickerJSON["currentPrice"]["changes"] = 100 * (tickerJSON["currentPrice"]["lastPrice"] - tickerJSON["currentPrice"]["closePrice"]) / tickerJSON["currentPrice"]["closePrice"]

                else:
                    tickerJSON["currentPrice"]["changes"] = 0

            if showInfo:
                self.ShowInstrumentInfo(iJSON=tickerJSON, printInfo=True)  # print info as Markdown text

        else:
            if showInfo:
                uLogger.warning("Ticker [{}] not found in available broker instrument's list!".format(self.ticker))

        return tickerJSON

    def SearchByFIGI(self, requestPrice: bool = False, showInfo: bool = False, debug: bool = False) -> dict:
        """
        Search and return raw broker's information about instrument by it's FIGI.
        `figi` must be define! If debug=True then print all debug messages.

        :param requestPrice: if `False` then do not request current price of instrument (it's long operation).
        :param showInfo: if `False` then do not run `ShowInstrumentInfo()` method and do not print info to the console.
        :param debug: if `True` then print all debug console messages.
        :return: JSON formatted data with information about instrument.
        """
        figiJSON = {}
        if debug:
            uLogger.debug("Searching information about instrument by it's FIGI [{}] ...".format(self.figi))

        if not self.figi:
            uLogger.warning("self.figi variable is not be empty!")

        else:
            if not self.iList:
                self.iList = self.Listing()

            for item in self.iList["Shares"].keys():
                if self.figi == self.iList["Shares"][item]["figi"]:
                    figiJSON = self.iList["Shares"][item]

                    if debug:
                        uLogger.debug("FIGI [{}] found in shares list".format(self.figi))

                    break

            if not figiJSON:
                for item in self.iList["Currencies"].keys():
                    if self.figi == self.iList["Currencies"][item]["figi"]:
                        figiJSON = self.iList["Currencies"][item]

                        if debug:
                            uLogger.debug("FIGI [{}] found in currencies list".format(self.figi))

                        break

            if not figiJSON:
                for item in self.iList["Bonds"].keys():
                    if self.figi == self.iList["Bonds"][item]["figi"]:
                        figiJSON = self.iList["Bonds"][item]

                        if debug:
                            uLogger.debug("FIGI [{}] found in bonds list".format(self.figi))

                        break

            if not figiJSON:
                for item in self.iList["Etfs"].keys():
                    if self.figi == self.iList["Etfs"][item]["figi"]:
                        figiJSON = self.iList["Etfs"][item]

                        if debug:
                            uLogger.debug("FIGI [{}] found in etfs list".format(self.figi))

                        break

            if not figiJSON:
                for item in self.iList["Futures"].keys():
                    if self.figi == self.iList["Futures"][item]["figi"]:
                        figiJSON = self.iList["Futures"][item]

                        if debug:
                            uLogger.debug("FIGI [{}] found in futures list".format(self.figi))

                        break

        if figiJSON:
            self.figi = figiJSON["figi"]
            self.ticker = figiJSON["ticker"]

            if requestPrice:
                figiJSON["currentPrice"] = self.GetCurrentPrices(showPrice=False)

                if figiJSON["currentPrice"]["closePrice"] is not None and figiJSON["currentPrice"]["closePrice"] != 0 and figiJSON["currentPrice"]["lastPrice"] is not None:
                    figiJSON["currentPrice"]["changes"] = 100 * (figiJSON["currentPrice"]["lastPrice"] - figiJSON["currentPrice"]["closePrice"]) / figiJSON["currentPrice"]["closePrice"]

                else:
                    figiJSON["currentPrice"]["changes"] = 0

            if showInfo:
                self.ShowInstrumentInfo(iJSON=figiJSON, printInfo=True)  # print info as Markdown text

        else:
            if showInfo:
                uLogger.warning("FIGI [{}] not found in available broker instrument's list!".format(self.figi))

        return figiJSON

    def GetCurrentPrices(self, showPrice: bool = False) -> dict:
        """
        Get and show Depth of Market with current prices of the instrument. If an error occurred then returns an empty record:
        `{"buy": [], "sell": [], "limitUp": None, "limitDown": None, "lastPrice": None, "closePrice": None}`.

        :param showPrice: if `True` then print DOM.
        :return: orders book dict with lists of current buy and sell prices: `{"buy": [{"price": x1, "quantity": y1, ...}], "sell": [....]}`.
        """
        prices = {"buy": [], "sell": [], "limitUp": 0, "limitDown": 0, "lastPrice": 0, "closePrice": 0}

        if self.depth < 1:
            raise Exception("Depth of Market (DOM) must be >=1!")

        if not (self.ticker or self.figi):
            raise Exception("self.ticker or self.figi variables must be defined!")

        if self.ticker and not self.figi:
            instrumentByTicker = self.SearchByTicker(requestPrice=False)  # WARNING! requestPrice=False to avoid recursion!
            self.figi = instrumentByTicker["figi"] if instrumentByTicker else ""

        if not self.ticker and self.figi:
            instrumentByFigi = self.SearchByFIGI(requestPrice=False)  # WARNING! requestPrice=False to avoid recursion!
            self.ticker = instrumentByFigi["ticker"] if instrumentByFigi else ""

        if not self.figi:
            uLogger.error("FIGI is not determined!")

        else:
            uLogger.debug("Requesting current prices for instrument with ticker [{}] and FIGI [{}]...".format(self.ticker, self.figi))

            # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetOrderBook
            priceURL = self.server + r"/tinkoff.public.invest.api.contract.v1.MarketDataService/GetOrderBook"
            self.body = str({"figi": self.figi, "depth": self.depth})
            pricesResponse = self.SendAPIRequest(priceURL, reqType="POST")

            if pricesResponse:
                # list of dicts with sellers orders:
                prices["buy"] = [{"price": NanoToFloat(item["price"]["units"], item["price"]["nano"]), "quantity": int(item["quantity"])} for item in pricesResponse["asks"]]

                # list of dicts with buyers orders:
                prices["sell"] = [{"price": NanoToFloat(item["price"]["units"], item["price"]["nano"]), "quantity": int(item["quantity"])} for item in pricesResponse["bids"]]

                # max price of instrument at this time:
                prices["limitUp"] = NanoToFloat(pricesResponse["limitUp"]["units"], pricesResponse["limitUp"]["nano"]) if "limitUp" in pricesResponse.keys() else None

                # min price of instrument at this time:
                prices["limitDown"] = NanoToFloat(pricesResponse["limitDown"]["units"], pricesResponse["limitDown"]["nano"]) if "limitDown" in pricesResponse.keys() else None

                # last price of deal with instrument:
                prices["lastPrice"] = NanoToFloat(pricesResponse["lastPrice"]["units"], pricesResponse["lastPrice"]["nano"]) if "lastPrice" in pricesResponse.keys() else 0

                # last close price of instrument:
                prices["closePrice"] = NanoToFloat(pricesResponse["closePrice"]["units"], pricesResponse["closePrice"]["nano"]) if "closePrice" in pricesResponse.keys() else 0

            else:
                uLogger.warning("Server return an empty or error response! See full log. Instrument: ticker [{}], FIGI [{}]".format(self.ticker, self.figi))
                uLogger.debug("Server response: {}".format(pricesResponse))

            if showPrice:
                if prices["buy"] or prices["sell"]:
                    info = [
                        "Orders book actual at [{}] (UTC)\nTicker: [{}], FIGI: [{}], Depth of Market: [{}]\n".format(
                            datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M:%S"),
                            self.ticker,
                            self.figi,
                            self.depth,
                        ),
                        uLog.sepShort, "\n",
                        " Orders of Buyers   | Orders of Sellers\n",
                        uLog.sepShort, "\n",
                        " Sell prices (vol.) | Buy prices (vol.)\n",
                        uLog.sepShort, "\n",
                    ]

                    if not prices["buy"]:
                        info.append("                    | No orders!\n")
                        sumBuy = 0

                    else:
                        sumBuy = sum([x["quantity"] for x in prices["buy"]])
                        maxMinSorted = sorted(prices["buy"], key=lambda k: k["price"], reverse=True)
                        for item in maxMinSorted:
                            info.append("                    | {} ({})\n".format(item["price"], item["quantity"]))

                    if not prices["sell"]:
                        info.append("No orders!          |\n")
                        sumSell = 0

                    else:
                        sumSell = sum([x["quantity"] for x in prices["sell"]])
                        for item in prices["sell"]:
                            info.append("{:>19} |\n".format("{} ({})".format(item["price"], item["quantity"])))

                    info.extend([
                        uLog.sepShort, "\n",
                        "{:>19} | {}\n".format("Total sell: {}".format(sumSell), "Total buy: {}".format(sumBuy)),
                        uLog.sepShort, "\n",
                    ])

                    infoText = "".join(info)

                    uLogger.info("Current prices in order book:\n\n{}".format(infoText))

                else:
                    uLogger.warning("Orders book is empty at this time! Instrument: ticker [{}], FIGI [{}]".format(self.ticker, self.figi))

        return prices

    def ShowInstrumentsInfo(self, showInstruments: bool = False) -> str:
        """
        This method get and show information about all available broker instruments.
        If `instrumentsFile` string is not empty then also save information to this file.

        :param showInstruments: if `True` then print results to console, if `False` - print only to file.
        :return: multi-string with all available broker instruments
        """
        if not self.iList:
            self.iList = self.Listing()

        info = [
            "# All available instruments from Tinkoff Broker server for current user token\n\n",
            "* **Actual on date:** [{}] (UTC)\n".format(datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M")),
        ]

        # add instruments count by type:
        for iType in self.iList.keys():
            info.append("* **{}:** [{}]\n".format(iType, len(self.iList[iType])))

        headerLine = "| Ticker       | Full name                                                      | FIGI         | Cur | Lot    | Step\n"
        splitLine = "|--------------|----------------------------------------------------------------|--------------|-----|--------|---------\n"

        # generating info tables with all instruments by type:
        for iType in self.iList.keys():
            info.extend(["\n\n## {} available. Total: [{}]\n\n".format(iType, len(self.iList[iType])), headerLine, splitLine])

            for instrument in self.iList[iType].keys():
                iName = self.iList[iType][instrument]["name"]  # instrument's name
                if len(iName) > 63:
                    iName = "{}...".format(iName[:60])  # right trim for a long string
    
                info.append("| {:<12} | {:<63}| {:<13}| {:<4}| {:<7}| {}\n".format(
                    self.iList[iType][instrument]["ticker"],
                    iName,
                    self.iList[iType][instrument]["figi"],
                    self.iList[iType][instrument]["currency"],
                    self.iList[iType][instrument]["lot"],
                    str(self.iList[iType][instrument]["step"]).rstrip("0"),
                ))

        infoText = "".join(info)

        if showInstruments:
            uLogger.info(infoText)

        if self.instrumentsFile:
            with open(self.instrumentsFile, "w", encoding="UTF-8") as fH:
                fH.write(infoText)

            uLogger.info("All available instruments are saved to file: [{}]".format(os.path.abspath(self.instrumentsFile)))

        return infoText

    def SearchInstruments(self, pattern: str, showResults: bool = False) -> dict:
        """
        This method search and show information about instruments by part of its ticker, FIGI or name.
        If `searchResultsFile` string is not empty then also save information to this file.

        :param pattern: string with part of ticker, FIGI or instrument's name.
        :param showResults: if `True` then print results to console, if `False` - return list of result only.
        :return: list of dictionaries with all found instruments.
        """
        if not self.iList:
            self.iList = self.Listing()

        searchResults = {iType: {} for iType in self.iList}  # same as iList but will contains only filtered instruments
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
            "* **Search pattern:** [{}]\n".format(pattern),
            "* **Found instruments:** [{}]\n\n".format(resultsLen),
            "**Note:** you can view info about found instruments with key `--info`, e.g.: `tksbrokerapi -t TICKER --info` or `tksbrokerapi -f FIGI --info`.\n"
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
                    info.extend(["\n### {}: [{}]\n\n".format(iType, iTypeValuesCount), headerLine, splitLine])
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

        if showResults:
            uLogger.info(infoTextShort)
            uLogger.info("You can view info about found instruments with key `--info`, e.g.: `tksbrokerapi -t IBM --info` or `tksbrokerapi -f BBG000BLNNH6 --info`")

        if self.searchResultsFile:
            with open(self.searchResultsFile, "w", encoding="UTF-8") as fH:
                fH.write(infoText)

            uLogger.info("Full search results were saved to file: [{}]".format(os.path.abspath(self.searchResultsFile)))

        return searchResults

    def GetListOfPrices(self, instruments: list = None, showPrices: bool = False) -> list:
        """
        This method get, maybe show and return prices of list of instruments. WARNING! This is potential long operation!
        See limits: https://tinkoff.github.io/investAPI/limits/
        If `pricesFile` string is not empty then also save information to this file.

        :param instruments: list of tickers or FIGIs.
        :param showPrices: if `True` then print to console, if `False` - print only to file.
        :return: list of instruments looks like this: `iList = [{some ticker info, "currentPrice": {current prices}}, {...}, ...]`
                 One item is dict returned by `SearchByTicker()` or `SearchByFIGI()` methods.
        """
        if instruments is None or not instruments:
            raise Exception("You must define some of tickers or FIGIs to request it's actual prices!")

        uLogger.debug("Requesting current prices of list of instruments from Tinkoff Broker server...")

        iList = []
        for iName in instruments:
            if iName not in self.aliases.keys():
                iList.append(iName)

            else:
                iList.append(self.aliases[iName])

        unique = set()  # create list with every figi only one time with the same order position:
        tempNames = [item for item in iList if not (item in unique or unique.add(item))]

        uLogger.debug("Ordered input list of instruments without duplicates of names: {}".format(tempNames))

        iList = []  # try to get info about all unique instruments:
        for iName in tempNames:
            self.ticker = iName
            iData = self.SearchByTicker(requestPrice=True)

            if not iData:
                self.ticker = ""
                self.figi = iName

                iData = self.SearchByFIGI(requestPrice=True)

                if not iData:
                    self.figi = ""
                    uLogger.warning("Instrument [{}] not in list of available instruments for current token!".format(iName))

            if iData:
                isUnique = True
                for item in iList:
                    if item["figi"] == iData["figi"] or item["ticker"] == iData["ticker"]:
                        isUnique = False
                        break

                if isUnique:
                    iList.append(iData)

        if showPrices:
            info = [
                "# Actual prices at: [{} UTC]\n\n".format(datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M")),
                "| Ticker       | FIGI         | Type       | Prev. close | Last price  | Chg. %   | Day limits min/max  | Actual sell / buy   | Curr.\n",
                "|--------------|--------------|------------|-------------|-------------|----------|---------------------|---------------------|------\n",
            ]

            for item in iList:
                info.append("| {:<12} | {:<12} | {:<10} | {:>11} | {:>11} | {:>7}% | {:>19} | {:>19} | {}\n".format(
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

            if showPrices:
                uLogger.info("Only unique instruments are shown:\n{}".format(infoText))

            if self.pricesFile:
                with open(self.pricesFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Price list for all instruments saved to file: [{}]".format(os.path.abspath(self.pricesFile)))

        return iList

    def RequestPortfolio(self) -> dict:
        """
        Requesting current actual user's portfolio.
        REST API for user portfolio: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetPortfolio

        :return: dictionary with user's portfolio.
        """
        uLogger.debug("Requesting current actual user's portfolio. Wait, please...")

        self.body = str({"accountId": self.accountId})
        portfolioURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio"
        rawPortfolio = self.SendAPIRequest(portfolioURL, reqType="POST")

        uLogger.debug("Records about user's portfolio successfully received")

        return rawPortfolio

    def RequestPositions(self) -> dict:
        """
        Requesting current open positions in currencies and instruments.
        REST API for open positions: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetPositions

        :return: dictionary with open positions by instruments.
        """
        uLogger.debug("Requesting current open positions in currencies and instruments. Wait, please...")

        self.body = str({"accountId": self.accountId})
        positionsURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetPositions"
        rawPositions = self.SendAPIRequest(positionsURL, reqType="POST")

        uLogger.debug("Records about current open positions successfully received")

        return rawPositions

    def RequestPendingOrders(self) -> list:
        """
        Requesting current actual pending orders.
        REST API for pending (market) orders: https://tinkoff.github.io/investAPI/swagger-ui/#/OrdersService/OrdersService_GetOrders

        :return: list of dictionaries with pending orders.
        """
        uLogger.debug("Requesting current actual pending orders. Wait, please...")

        self.body = str({"accountId": self.accountId})
        ordersURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/GetOrders"
        rawOrders = self.SendAPIRequest(ordersURL, reqType="POST")["orders"]

        uLogger.debug("[{}] records about pending orders successfully received".format(len(rawOrders)))

        return rawOrders

    def RequestStopOrders(self) -> list:
        """
        Requesting current actual stop orders.
        REST API for opened stop-orders: https://tinkoff.github.io/investAPI/swagger-ui/#/StopOrdersService/StopOrdersService_GetStopOrders

        :return: list of dictionaries with stop orders.
        """
        uLogger.debug("Requesting current actual stop orders. Wait, please...")

        self.body = str({"accountId": self.accountId})
        ordersURL = self.server + r"/tinkoff.public.invest.api.contract.v1.StopOrdersService/GetStopOrders"
        rawStopOrders = self.SendAPIRequest(ordersURL, reqType="POST")["stopOrders"]

        uLogger.debug("[{}] records about stop orders successfully received".format(len(rawStopOrders)))

        return rawStopOrders

    def Overview(self, showStatistics: bool = False) -> dict:
        """
        Get portfolio: all open positions, orders and some statistics for defined accountId.
        If `overviewFile` is define then also save information to file.

        :param showStatistics: if `False` then only dictionary returns, if `True` then show more debug information.
        :return: dictionary with client's raw portfolio and some statistics.
        """
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
            }
        }

        if showStatistics:
            uLogger.debug("Requesting portfolio of a client. Wait, please...")

        portfolioResponse = self.RequestPortfolio()  # current user's portfolio (dict)
        view["raw"]["positions"] = self.RequestPositions()  # current open positions by instruments (dict)
        view["raw"]["orders"] = self.RequestPendingOrders()  # current actual pending orders (list)
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
                self.figi = item["figi"]
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
            self.figi = item["figi"]
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
                cost = (curPrice + NanoToFloat(item["currentNkd"]["units"], item["currentNkd"]["nano"])) * volume  # current cost of all volume of instrument in basic asset
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
                    "percentProfit": 100 * profit / (average * volume),  # expected percents of profit at current moment for this instrument
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
                        "total": volume,
                        "totalCostRUB": costRUB,  # total volume cost in rubles
                        "free": volume - blocked,
                        "freeCostRUB": costRUB * ((volume - blocked) / volume) if volume > 0 else 0,  # free volume cost in rubles
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
        view["stat"]["funds"]["rub"] = {
            "total": view["stat"]["availableRUB"],
            "totalCostRUB": view["stat"]["availableRUB"],
            "free": view["stat"]["availableRUB"] - view["stat"]["blockedRUB"],
            "freeCostRUB": view["stat"]["availableRUB"] - view["stat"]["blockedRUB"],
        }

        # --- pending orders sector data:
        for item in view["raw"]["orders"]:
            self.figi = item["figi"]
            instrument = self.SearchByFIGI(requestPrice=True)  # full raw info about instrument by FIGI

            if instrument:
                action = TKS_ORDER_DIRECTIONS[item["direction"]]
                orderType = TKS_ORDER_TYPES[item["orderType"]]
                orderState = TKS_ORDER_STATES[item["executionReportStatus"]]
                orderDate = item["orderDate"].replace("T", " ").replace("Z", "").split(".")[0]  # date in UTC format, e.g. "2022-12-31T23:59:59.123456Z"

                # current instrument's price (last sellers order if buy, and last buyers order if sell):
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
                    "date": orderDate,  # string with order date and time from UTC format (without nano seconds part)
                })

        # --- stop orders sector data:
        for item in view["raw"]["stopOrders"]:
            self.figi = item["figi"]
            instrument = self.SearchByFIGI(requestPrice=True)  # full raw info about instrument by FIGI

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

                # current instrument's price (last sellers order if buy, and last buyers order if sell):
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
                    "createDate": createDate,  # string with created order date and time from UTC format (without nano seconds part)
                    "expDate": expDate,  # string with expiration order date and time from UTC format (without nano seconds part)
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
        view["analytics"]["distrByCurrencies"].update(byCurr)
        view["analytics"]["distrByCurrencies"]["rub"]["cost"] += view["analytics"]["distrByAssets"]["Ruble"]["cost"]
        view["analytics"]["distrByCurrencies"]["rub"]["percent"] += view["analytics"]["distrByAssets"]["Ruble"]["percent"]

        # portfolio distribution by countries:
        view["analytics"]["distrByCountries"].update(byCountry)

        # --- Prepare text statistics overview in human-readable:
        if showStatistics:
            info = [
                "# Client's portfolio\n\n",
                "* **Actual date:** [{}] (UTC)\n".format(datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M:%S")),
                "* **Portfolio cost:** {:.2f} RUB\n".format(view["stat"]["portfolioCostRUB"]),
                "* **Changes:** {}{:.2f} RUB ({}{:.2f}%)\n\n".format(
                    "+" if view["stat"]["totalChangesRUB"] > 0 else "",
                    view["stat"]["totalChangesRUB"],
                    "+" if view["stat"]["totalChangesPercentRUB"] > 0 else "",
                    view["stat"]["totalChangesPercentRUB"],
                ),
                "## Open positions\n\n",
                "| Ticker [FIGI]               | Volume (blocked)                | Lots     | Curr. price  | Avg. price   | Current volume cost | Profit (%)\n",
                "|-----------------------------|---------------------------------|----------|--------------|--------------|---------------------|----------------------\n",
                "| Ruble                       | {:>31} |          |              |              |                     |\n".format(
                    "{:.2f} ({:.2f}) rub".format(
                        view["stat"]["availableRUB"],
                        view["stat"]["blockedRUB"],
                    )
                )
            ]

            def _SplitStr(CostRUB: float = 0, typeStr: str = "", noTradeStr: str = "") -> list:
                return [
                    "|                             |                                 |          |              |              |                     |\n",
                    "| {:<27} |                                 |          |              |              | {:>19} |\n".format(
                        noTradeStr if noTradeStr else typeStr,
                        "" if noTradeStr else "{:.2f} RUB".format(CostRUB),
                    ),
                ]

            def _InfoStr(data: dict, showCurrencyName: bool = False) -> str:
                return "| {:<27} | {:>31} | {:<8} | {:>12} | {:>12} | {:>19} | {}\n".format(
                    "{} [{}]".format(data["ticker"], data["figi"]),
                    "{:.2f} ({:.2f}) {}".format(
                        data["volume"],
                        data["blocked"],
                        data["currency"],
                    ) if showCurrencyName else "{:.0f} ({:.0f})".format(
                        data["volume"],
                        data["blocked"],
                    ),
                    "{:.4f}".format(data["lots"]) if showCurrencyName else "{:.0f}".format(data["lots"]),
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
                    info.append(_InfoStr(item, showCurrencyName=True))

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

            # --- Show pending orders section:
            if view["stat"]["orders"]:
                info.extend([
                    "\n## Opened pending limit-orders: {}\n".format(len(view["stat"]["orders"])),
                    "\n| Ticker [FIGI]               | Order ID       | Lots (exec.) | Current price (% delta) | Target price  | Action    | Type      | Create date (UTC)\n",
                    "|-----------------------------|----------------|--------------|-------------------------|---------------|-----------|-----------|---------------------\n",
                ])
                for item in view["stat"]["orders"]:
                    info.append("| {:<27} | {:<14} | {:<12} | {:>23} | {:>13} | {:<9} | {:<9} | {}\n".format(
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
                info.append("\n## Total pending limit-orders: 0\n")

            # --- Show stop orders section:
            if view["stat"]["stopOrders"]:
                info.extend([
                    "\n## Opened stop-orders: {}\n".format(len(view["stat"]["stopOrders"])),
                    "\n| Ticker [FIGI]               | Stop order ID                        | Lots   | Current price (% delta) | Target price  | Limit price   | Action    | Type        | Expire type  | Create date (UTC)   | Expiration (UTC)\n",
                    "|-----------------------------|--------------------------------------|--------|-------------------------|---------------|---------------|-----------|-------------|--------------|---------------------|---------------------\n",
                ])
                for item in view["stat"]["stopOrders"]:
                    info.append("| {:<27} | {:<14} | {:<6} | {:>23} | {:>13} | {:>13} | {:<9} | {:<11} | {:<12} | {:<19} | {}\n".format(
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
                info.append("\n## Total stop-orders: 0\n")

            # -- Show analytics section:
            if view["stat"]["portfolioCostRUB"] > 0:
                info.extend([
                    "\n# Analytics\n"
                    "\n* **Current total portfolio cost:** {:.2f} RUB\n".format(view["stat"]["portfolioCostRUB"]),
                    "* **Changes:** {}{:.2f} RUB ({}{:.2f}%)\n".format(
                        "+" if view["stat"]["totalChangesRUB"] > 0 else "",
                        view["stat"]["totalChangesRUB"],
                        "+" if view["stat"]["totalChangesPercentRUB"] > 0 else "",
                        view["stat"]["totalChangesPercentRUB"],
                    ),
                    "\n## Portfolio distribution by assets\n"
                    "\n| Type       | Uniques | Percent | Current cost\n",
                    "|------------|---------|---------|-----------------\n",
                ])

                for key in view["analytics"]["distrByAssets"].keys():
                    if view["analytics"]["distrByAssets"][key]["cost"] > 0:
                        info.append("| {:<10} | {:<7} | {:<7} | {:.2f} rub\n".format(
                            key,
                            view["analytics"]["distrByAssets"][key]["uniques"],
                            "{:.2f}%".format(view["analytics"]["distrByAssets"][key]["percent"]),
                            view["analytics"]["distrByAssets"][key]["cost"],
                        ))

                maxLenNames = 3 + max([len(company) + len(view["analytics"]["distrByCompanies"][company]["ticker"]) for company in view["analytics"]["distrByCompanies"].keys()])
                info.extend([
                    "\n## Portfolio distribution by companies\n"
                    "\n| Company{} | Percent | Current cost\n".format(" " * (maxLenNames - 7)),
                    "|--------{}-|---------|-----------------\n".format("-" * (maxLenNames - 7)),
                ])

                for company in view["analytics"]["distrByCompanies"].keys():
                    if view["analytics"]["distrByCompanies"][company]["cost"] > 0:
                        nameLen = 3 + len(company) + len(view["analytics"]["distrByCompanies"][company]["ticker"])
                        info.append("| {} | {:<7} | {:.2f} rub\n".format(
                            "{}{}{}".format(
                                "[{}] ".format(view["analytics"]["distrByCompanies"][company]["ticker"]) if view["analytics"]["distrByCompanies"][company]["ticker"] else "",
                                company,
                                "" if nameLen == maxLenNames else "{}".format(" " * (maxLenNames - nameLen) if view["analytics"]["distrByCompanies"][company]["ticker"] else " " * (maxLenNames - nameLen + 3)),
                            ),
                            "{:.2f}%".format(view["analytics"]["distrByCompanies"][company]["percent"]),
                            view["analytics"]["distrByCompanies"][company]["cost"],
                        ))

                maxLenSectors = max([len(sector) for sector in view["analytics"]["distrBySectors"].keys()])
                info.extend([
                    "\n## Portfolio distribution by sectors\n"
                    "\n| Sector{} | Percent | Current cost\n".format(" " * (maxLenSectors - 6)),
                    "|-------{}-|---------|-----------------\n".format("-" * (maxLenSectors - 6)),
                ])

                for sector in view["analytics"]["distrBySectors"].keys():
                    if view["analytics"]["distrBySectors"][sector]["cost"] > 0:
                        info.append("| {}{} | {:<7} | {:.2f} rub\n".format(
                            sector,
                            "" if len(sector) == maxLenSectors else " " * (maxLenSectors - len(sector)),
                            "{:.2f}%".format(view["analytics"]["distrBySectors"][sector]["percent"]),
                            view["analytics"]["distrBySectors"][sector]["cost"],
                        ))

                maxLenMoney = 3 + max([len(currency) + len(view["analytics"]["distrByCurrencies"][currency]["name"]) for currency in view["analytics"]["distrByCurrencies"].keys()])
                info.extend([
                    "\n## Portfolio distribution by currencies\n"
                    "\n| Instruments currencies{} | Percent | Current cost\n".format(" " * (maxLenMoney - 22)),
                    "|-----------------------{}-|---------|-----------------\n".format("-" * (maxLenMoney - 22)),
                ])

                for curr in view["analytics"]["distrByCurrencies"].keys():
                    if view["analytics"]["distrByCurrencies"][curr]["cost"] > 0:
                        nameLen = 3 + len(curr) + len(view["analytics"]["distrByCurrencies"][curr]["name"])
                        info.append("| {} | {:<7} | {:.2f} rub\n".format(
                            "[{}] {}{}".format(
                                curr,
                                view["analytics"]["distrByCurrencies"][curr]["name"],
                                "" if nameLen == maxLenMoney else " " * (maxLenMoney - nameLen),
                            ),
                            "{:.2f}%".format(view["analytics"]["distrByCurrencies"][curr]["percent"]),
                            view["analytics"]["distrByCurrencies"][curr]["cost"],
                        ))

                maxLenCountry = max(17, max([len(country) for country in view["analytics"]["distrByCountries"].keys()]))
                info.extend([
                    "\n## Portfolio distribution by countries\n"
                    "\n| Assets by country{} | Percent | Current cost\n".format(" " * (maxLenCountry - 17)),
                    "|------------------{}-|---------|-----------------\n".format("-" * (maxLenCountry - 17)),
                ])

                for country in view["analytics"]["distrByCountries"].keys():
                    if view["analytics"]["distrByCountries"][country]["cost"] > 0:
                        nameLen = len(country)
                        info.append("| {} | {:<7} | {:.2f} rub\n".format(
                            "{}{}".format(
                                country,
                                "" if nameLen == maxLenCountry else " " * (maxLenCountry - nameLen),
                            ),
                            "{:.2f}%".format(view["analytics"]["distrByCountries"][country]["percent"]),
                            view["analytics"]["distrByCountries"][country]["cost"],
                        ))

            infoText = "".join(info)

            if showStatistics:
                uLogger.info("Statistics of client's portfolio:\n{}".format(infoText))

            if self.overviewFile:
                with open(self.overviewFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("Client's portfolio is saved to file: [{}]".format(os.path.abspath(self.overviewFile)))

        return view

    def Deals(self, start: str = None, end: str = None, printDeals: bool = False, showCancelled: bool = True) -> tuple:
        """
        Returns history operations between two given dates.
        If `reportFile` string is not empty then also save human-readable report.
        Shows some statistical data of closed positions.

        :param start: see docstring in `GetDatesAsString()` method
        :param end: see docstring in `GetDatesAsString()` method
        :param printDeals: if `True` then also print all records to the console.
        :param showCancelled: if `False` then remove information about cancelled operations from the deals report.
        :return: original list of dictionaries with history of deals records from API ("operations" key):
                 https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetOperations
                 and dictionary with custom stats: operations in different currencies, withdrawals, incomes etc.
        """
        startDate, endDate = GetDatesAsString(start, end)  # Example: ("2000-01-01T00:00:00Z", "2022-12-31T23:59:59Z")

        uLogger.debug("Requesting history of a client's operations. Wait, please...")

        # REST API for request: https://tinkoff.github.io/investAPI/swagger-ui/#/OperationsService/OperationsService_GetOperations
        dealsURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OperationsService/GetOperations"
        self.body = str({"accountId": self.accountId, "from": startDate, "to": endDate})
        ops = self.SendAPIRequest(dealsURL, reqType="POST")["operations"]  # list of dict: operations returns by broker
        customStat = {}  # custom statistics in additional to responseJSON

        # --- output report in human-readable format:
        if printDeals or self.reportFile:
            splitLine1 = "|                            |                               |                              |                      |\n"  # Summary section
            splitLine2 = "|                     |              |              |            |           |                 |            |\n"  # Operations section
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
                    "| 1                          | 2                             | 3                            | 4                    | 5\n",
                    "|----------------------------|-------------------------------|------------------------------|----------------------|------------------------\n",
                    "| **Actions:**               | Trades: {:<21} | Trading volumes:             |                      |\n".format(customStat["opsCount"]),
                    "|                            |   Buy: {:<22} | {:<28} |                      |\n".format(
                        "{} ({:.1f}%)".format(customStat["buyCount"], 100 * customStat["buyCount"] / customStat["opsCount"]) if customStat["opsCount"] != 0 else 0,
                        "  rub, buy: {:<16}".format("{:.2f}".format(customStat["buyTotal"]["rub"])) if customStat["buyTotal"]["rub"] != 0 else "  —",
                    ),
                    "|                            |   Sell: {:<21} | {:<28} |                      |\n".format(
                        "{} ({:.1f}%)".format(customStat["sellCount"], 100 * customStat["sellCount"] / customStat["opsCount"]) if customStat["opsCount"] != 0 else 0,
                        "  rub, sell: {:<13}".format("+{:.2f}".format(customStat["sellTotal"]["rub"])) if customStat["sellTotal"]["rub"] != 0 else "  —",
                    ),
                ])

                opsKeys = sorted(list(set(list(customStat["buyTotal"].keys()) + list(customStat["sellTotal"].keys()))))
                for key in opsKeys:
                    if key == "rub":
                        continue

                    info.extend([
                        "|                            |                               | {:<28} |                      |\n".format(
                            "  {}, buy: {:<16}".format(key, "{:.2f}".format(customStat["buyTotal"][key]) if key and key in customStat["buyTotal"].keys() and customStat["buyTotal"][key] != 0 else 0)
                        ),
                        "|                            |                               | {:<28} |                      |\n".format(
                            "  {}, sell: {:<13}".format(key, "+{:.2f}".format(customStat["sellTotal"][key]) if key and key in customStat["sellTotal"].keys() and customStat["sellTotal"][key] != 0 else 0)
                        ),
                    ])

                info.append(splitLine1)

                def _InfoStr(data1: dict, data2: dict, data3: dict, data4: dict, cur: str = "") -> str:
                    return "|                            | {:<29} | {:<28} | {:<20} | {:<22}\n".format(
                            "  {}: {}{:.2f}".format(cur, "+" if data1[cur] > 0 else "", data1[cur]) if cur and cur in data1.keys() and data1[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data2[cur] > 0 else "", data2[cur]) if cur and cur in data2.keys() and data2[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data3[cur] > 0 else "", data3[cur]) if cur and cur in data3.keys() and data3[cur] != 0 else "  —",
                            "  {}: {}{:.2f}".format(cur, "+" if data4[cur] > 0 else "", data4[cur]) if cur and cur in data4.keys() and data4[cur] != 0 else "  —",
                    )

                # --- view "Payments" lines:
                info.append("| **Payments:**              | Deposit on broker account:    | Withdrawals:                 | Dividends income:    | Coupons income:\n")
                paymentsKeys = sorted(list(set(list(customStat["payIn"].keys()) + list(customStat["payOut"].keys()) + list(customStat["divs"].keys()) + list(customStat["coupons"].keys()))))

                for key in paymentsKeys:
                    info.append(_InfoStr(customStat["payIn"], customStat["payOut"], customStat["divs"], customStat["coupons"], key))

                info.append(splitLine1)

                # --- view "Commissions and taxes" lines:
                info.append("| **Commissions and taxes:** | Broker commissions:           | Service commissions:         | Margin commissions:  | All taxes/corrections:\n")
                comKeys = sorted(list(set(list(customStat["brokerCom"].keys()) + list(customStat["serviceCom"].keys()) + list(customStat["marginCom"].keys()) + list(customStat["allTaxes"].keys()))))

                for key in comKeys:
                    info.append(_InfoStr(customStat["brokerCom"], customStat["serviceCom"], customStat["marginCom"], customStat["allTaxes"], key))

                info.append(splitLine1)

                info.extend([
                    "\n## All operations{}\n\n".format("" if showCancelled else " (without cancelled status)"),
                    "| Date and time       | FIGI         | Ticker       | Asset      | Value     | Payment         | Status     | Operation type\n",
                    "|---------------------|--------------|--------------|------------|-----------|-----------------|------------|--------------------------------------------------------------------\n",
                ])

            else:
                info.append("Broker returned no operations during this period\n")

            # --- view "Operations" section:
            for item in ops:
                if not showCancelled and TKS_OPERATION_STATES[item["state"]] == TKS_OPERATION_STATES["OPERATION_STATE_CANCELED"]:
                    continue

                else:
                    self.figi = item["figi"] if item["figi"] else ""
                    payment = NanoToFloat(item["payment"]["units"], item["payment"]["nano"])
                    instrument = self.SearchByFIGI(requestPrice=False) if self.figi else {}

                    # group of deals during one day:
                    if nextDay and item["date"].split("T")[0] != nextDay:
                        info.append(splitLine2)
                        nextDay = ""

                    else:
                        nextDay = item["date"].split("T")[0]  # saving current day for splitting

                    info.append("| {:<19} | {:<12} | {:<12} | {:<10} | {:<9} | {:>15} | {:<10} | {}\n".format(
                        item["date"].replace("T", " ").replace("Z", "").split(".")[0],
                        self.figi if self.figi else "—",
                        instrument["ticker"] if instrument else "—",
                        instrument["type"] if instrument else "—",
                        item["quantity"] if int(item["quantity"]) > 0 else "—",
                        "{}{:.2f} {}".format("+" if payment > 0 else "", payment, item["payment"]["currency"]) if payment != 0 else "—",
                        TKS_OPERATION_STATES[item["state"]],
                        TKS_OPERATION_TYPES[item["operationType"]],
                    ))

            infoText = "".join(info)

            if printDeals:
                uLogger.info(infoText)

            if self.reportFile:
                with open(self.reportFile, "w", encoding="UTF-8") as fH:
                    fH.write(infoText)

                uLogger.info("History of a client's operations are saved to file: [{}]".format(os.path.abspath(self.reportFile)))

        return ops, customStat

    def History(self, onlyMissing: bool = False):
        """
        This method returns last history candles of the current instrument defined by `ticker`.
        If `historyFile` is not None then method save history to this file, otherwise return only pandas dataframe.
        `historyLength` define how many candles returns from past to current date.
        `historyInterval` define candle interval. Available values are strings: `"1min"`, `"2min"`, `"3min"`, `"5min"`,
        `"10min"`, `"15min"`, `"30min"`, `"hour"`, `"day"`, `"week"`, `"month"`. Default: `"hour"`.
        Maximum requested history date in the past: `1970.01.02 03:45`

        :param onlyMissing: if history file define then add only last missing candles, do not request all history length. False by default.
                            WARNING! History appends only from last candle to current time with replace last candle! Intervals must be similar!
        :return: pandas dataframe with prices history. Columns: `date`, `time`, `open`, `high`, `low`, `close`, `volume`.
        """
        history = None  # empty pandas object for history
        # TODO: update history to work with api v2
        # if self.historyLength < 1:
        #     raise Exception("History length parameter must be >=1!")
        #
        # if self.historyInterval not in TKS_TIMEFRAMES.keys():
        #     raise Exception("Interval parameter must be string with available values: 1min, 2min, 3min, 5min, 10min, 15min, 30min, hour, day, week, month.")
        #
        # if not (self.ticker or self.figi):
        #     raise Exception("self.ticker or self.figi variables must be defined!")
        #
        # if self.ticker and not self.figi:
        #     instrumentByTicker = self.SearchByTicker(requestPrice=False, debug=False)
        #     self.figi = instrumentByTicker["figi"] if instrumentByTicker else ""
        #
        # endDate = datetime.now(tzutc())  # current time for request history
        # tempOld = None  # pandas object for old history, if --only-missing key present
        # lastTime = None  # datetime object of last old candle in file
        # minStartDate = datetime.strptime("1970.01.02 03:45", "%Y.%m.%d %H:%M").astimezone(tzutc())  # Maximum requested history date in the past
        #
        # # get old history saved earlier in file:
        # if onlyMissing and self.historyFile and os.path.exists(self.historyFile):
        #     uLogger.debug("--only-missing key present, so auto decreasing --length value...")
        #     uLogger.debug("Only append missing last history candles at the end of the file [{}]".format(os.path.abspath(self.historyFile)))
        #
        #     tempOld = pd.read_csv(self.historyFile, sep=",", header=None, names=["date", "time", "open", "high", "low", "close", "volume"])
        #
        #     tempOld["date"] = pd.to_datetime(tempOld["date"])  # load date "as is"
        #     tempOld["date"] = tempOld["date"].dt.strftime("%Y.%m.%d")  # convert date to string
        #     tempOld["time"] = pd.to_datetime(tempOld["time"])  # load time "as is"
        #     tempOld["time"] = tempOld["time"].dt.strftime("%H:%M")  # convert time to string
        #
        #     # get last datetime object from last string in file or minus 1 delta if file is empty:
        #     if len(tempOld) > 0:
        #         lastTime = datetime.strptime(tempOld.date.iloc[-1] + " " + tempOld.time.iloc[-1], "%Y.%m.%d %H:%M").astimezone(tzutc())
        #
        #     else:
        #         lastTime = endDate - timedelta(minutes=TKS_TIMEFRAMES[self.historyInterval]["minutes"])
        #         uLogger.warning("No history in file, set last date to request at [{}]".format(lastTime))
        #
        #     delta = endDate - lastTime  # current time minus last time in file
        #     deltaMinutes = delta.days * 1440 + delta.seconds // 60  # minutes between last datetime and current datetime
        #
        #     # calculate new (decreased) history length to download:
        #     self.historyLength = deltaMinutes // TKS_TIMEFRAMES[self.historyInterval]["minutes"]
        #     if deltaMinutes % TKS_TIMEFRAMES[self.historyInterval]["minutes"] > 0:
        #         self.historyLength += 1  # to avoid fraction time
        #
        #     tempOld = tempOld[:-1]  # always remove last old candle because it may be incompletely at the current time
        #
        # if self.figi:
        #     blocks = 1 if self.historyLength <= TKS_TIMEFRAMES[self.historyInterval]["maxCandles"] else 1 + self.historyLength // TKS_TIMEFRAMES[self.historyInterval]["maxCandles"]
        #     responseJSONs = []  # raw history blocks
        #
        #     uLogger.debug("Request last history from Tinkoff Broker server for ticker [{}], FIGI [{}]...".format(self.ticker, self.figi))
        #
        #     uLogger.debug("Requested history length: [{}], interval: [{}]".format(self.historyLength, self.historyInterval))
        #     uLogger.debug("User requested time period is about from [{}] to [{}]".format(
        #         (endDate - timedelta(minutes=TKS_TIMEFRAMES[self.historyInterval]["minutes"] * self.historyLength)).strftime("%Y-%m-%d %H:%M:%S"),
        #         endDate.strftime("%Y-%m-%d %H:%M:%S"),
        #     ))
        #
        #     uLogger.debug("Blocks count: [{}], max candles in block for this interval: [{}]".format(blocks, TKS_TIMEFRAMES[self.historyInterval]["maxCandles"]))
        #
        #     oldFlag = False
        #     for item in range(blocks):
        #         tail = self.historyLength % TKS_TIMEFRAMES[self.historyInterval]["maxCandles"] if item + 1 == blocks else TKS_TIMEFRAMES[self.historyInterval]["maxCandles"]
        #         startDate = endDate - timedelta(minutes=TKS_TIMEFRAMES[self.historyInterval]["minutes"] * tail)
        #
        #         if startDate < minStartDate:
        #             startDate = minStartDate  # set minimum date in the past if delta is too long
        #             uLogger.debug("Date in the past is too old for request. Set start time to [{}]".format(minStartDate.strftime("%Y-%m-%d %H:%M:%S")))
        #             oldFlag = True
        #
        #         uLogger.debug("Block time period: from [{}] to [{}] ({}/{})".format(
        #             startDate.strftime("%Y-%m-%d %H:%M:%S"),
        #             endDate.strftime("%Y-%m-%d %H:%M:%S"),
        #             item + 1,
        #             blocks,
        #         ))
        #
        #         historyURL = self.server + r"/market/candles?figi={}&from={}&to={}&interval={}".format(
        #             self.figi,
        #             quote(startDate.isoformat()),
        #             quote(endDate.isoformat()),
        #             self.historyInterval,
        #         )
        #         responseJSON = self.SendAPIRequest(historyURL, debug=False)["payload"]["candles"]
        #
        #         responseJSONs = responseJSON + responseJSONs  # add more old history behind newest dates
        #         endDate = startDate
        #
        #         if oldFlag: break
        #
        #     if responseJSONs:
        #         tempHistory = pd.DataFrame(
        #             data={
        #                 "date": [pd.to_datetime(item["time"]).astimezone(tzutc()) for item in responseJSONs],
        #                 "time": [pd.to_datetime(item["time"]).astimezone(tzutc()) for item in responseJSONs],
        #                 "open": [item["o"] for item in responseJSONs],
        #                 "high": [item["h"] for item in responseJSONs],
        #                 "low": [item["l"] for item in responseJSONs],
        #                 "close": [item["c"] for item in responseJSONs],
        #                 "volume": [item["v"] for item in responseJSONs],
        #             },
        #             index=range(len(responseJSONs)),
        #             columns=["date", "time", "open", "high", "low", "close", "volume"],
        #         )
        #         tempHistory["date"] = tempHistory["date"].dt.strftime("%Y.%m.%d")
        #         tempHistory["time"] = tempHistory["time"].dt.strftime("%H:%M")
        #
        #         # append only newest candles to old history if --only-missing key present:
        #         if onlyMissing and tempOld is not None and lastTime is not None:
        #             indx = 0  # find start index in given from server tempHistory data:
        #             for i, item in tempHistory.iterrows():
        #                 curTime = datetime.strptime(item["date"] + " " + item["time"], "%Y.%m.%d %H:%M").astimezone(tzutc())
        #                 if curTime == lastTime:
        #                     uLogger.debug("History candles will be updated starting from the candle with date: [{}]".format(curTime.strftime("%Y-%m-%d %H:%M:%S")))
        #                     indx = i
        #                     break
        #
        #             history = tempOld.append(tempHistory[indx:], ignore_index=True)
        #
        #         else:
        #             history = tempHistory  # if no --only-missing key then load full data from server
        #
        #         uLogger.debug("Showing last 3 rows of candles history:")
        #         for line in pd.DataFrame.to_string(
        #                 history[["date", "time", "open", "high", "low", "close", "volume"]][-3:],
        #                 max_cols=20,
        #         ).split("\n"):
        #             uLogger.debug(line)
        #
        #     if self.historyFile is not None:
        #         if history is not None:
        #             history.to_csv(self.historyFile, sep=",", index=False, header=False)
        #             uLogger.info("Ticker [{}], FIGI [{}], tf: [{}], history saved: [{}]".format(
        #                 self.ticker,
        #                 self.figi,
        #                 self.historyInterval,
        #                 os.path.abspath(self.historyFile),
        #             ))
        #
        #         else:
        #             uLogger.warning("Empty history received! File NOT updated: [{}]".format(os.path.abspath(self.historyFile)))
        #
        #     else:
        #         uLogger.debug("--output key is not defined. Parsed history file not saved to .csv-file, only pandas dataframe returns.")

        return history

    def Trade(self, operation: str, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        Universal method to create market order and make deal at the current price. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will opens stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` docstring. More simple methods than `Trade()` are `Buy()` and `Sell()`.

        :param operation: string "Buy" or "Sell".
        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, target price for stop-order with "TP" type. It used as take profit parameter `targetPrice` in `self.Order()`.
        :param sl: float > 0, target price for stop-order with "SL" type. It used as stop loss parameter `targetPrice` in `self.Order()`.
        :param expDate: string "Undefined" by default or local date in future,
                        it is a string with format `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        if operation is None or not operation or operation not in ("Buy", "Sell"):
            raise Exception("You must define operation type only one of them: `Buy` or `Sell`!")

        if lots is None or lots < 1:
            uLogger.warning("You must define trade volume > 0: integer count of lots! For current operation lots reset to 1.")
            lots = 1

        if tp is None or tp < 0:
            tp = 0

        if sl is None or sl < 0:
            sl = 0

        if expDate is None or not expDate:
            expDate = "Undefined"

        if not (self.ticker or self.figi):
            raise Exception("`self.ticker` or `self.figi` variables must be defined!")

        instrument = self.SearchByTicker(requestPrice=True, debug=False) if self.ticker else self.SearchByFIGI(requestPrice=True, debug=False)
        self.ticker = instrument["ticker"]
        self.figi = instrument["figi"]

        uLogger.debug("Opening [{}] market order: ticker [{}], FIGI [{}], lots [{}], TP [{:.4f}], SL [{:.4f}], expiration date of TP/SL orders [{}]. Wait, please...".format(operation, self.ticker, self.figi, lots, tp, sl, expDate))

        openTradeURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"
        self.body = str({
            "figi": self.figi,
            "quantity": str(lots),
            "direction": "ORDER_DIRECTION_BUY" if operation == "Buy" else "ORDER_DIRECTION_SELL",  # see: TKS_ORDER_DIRECTIONS
            "accountId": str(self.accountId),
            "orderType": "ORDER_TYPE_MARKET",  # see: TKS_ORDER_TYPES
        })
        response = self.SendAPIRequest(openTradeURL, reqType="POST", retry=0, debug=False)

        if "orderId" in response.keys():
            uLogger.info("[{}] market order [{}] was executed: ticker [{}], FIGI [{}], lots [{}]. Total order price: [{:.4f} {}] (with commission: [{:.2f} {}]). Average price of lot: [{:.2f} {}]".format(
                operation, response["orderId"],
                self.ticker, self.figi, lots,
                NanoToFloat(response["totalOrderAmount"]["units"], response["totalOrderAmount"]["nano"]), response["totalOrderAmount"]["currency"],
                NanoToFloat(response["initialCommission"]["units"], response["initialCommission"]["nano"]), response["initialCommission"]["currency"],
                NanoToFloat(response["executedOrderPrice"]["units"], response["executedOrderPrice"]["nano"]), response["executedOrderPrice"]["currency"],
            ))

        else:
            uLogger.warning("Not `oK` status received! Market order not created. See full debug log or try again and open order later.")

        if tp > 0:
            self.Order(operation="Sell" if operation == "Buy" else "Buy", orderType="Stop", lots=lots, targetPrice=tp, limitPrice=tp, stopType="TP", expDate=expDate)

        if sl > 0:
            self.Order(operation="Sell" if operation == "Buy" else "Buy", orderType="Stop", lots=lots, targetPrice=sl, limitPrice=sl, stopType="SL", expDate=expDate)

        return response

    def Buy(self, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        More simple method than `Trade()`. Create `Buy` market order and make deal at the current price. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will opens stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` and `Trade()` docstrings.

        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, take profit price of stop-order.
        :param sl: float > 0, stop loss price of stop-order.
        :param expDate: it's a local date in future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        return self.Trade(operation="Buy", lots=lots, tp=tp, sl=sl, expDate=expDate)

    def Sell(self, lots: int = 1, tp: float = 0., sl: float = 0., expDate: str = "Undefined") -> dict:
        """
        More simple method than `Trade()`. Create `Sell` market order and make deal at the current price. Returns JSON data with response.
        If `tp` or `sl` > 0, then in additional will opens stop-orders with "TP" and "SL" flags for `stopType` parameter.

        See also: `Order()` and `Trade()` docstrings.

        :param lots: volume, integer count of lots >= 1.
        :param tp: float > 0, take profit price of stop-order.
        :param sl: float > 0, stop loss price of stop-order.
        :param expDate: it's a local date in future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
        :return: JSON with response from broker server.
        """
        return self.Trade(operation="Sell", lots=lots, tp=tp, sl=sl, expDate=expDate)

    def CloseTrades(self, tickers: list, overview: dict = None) -> None:
        """
        Close position of given instruments.

        :param tickers: tickers list of instruments that must be closed.
        :param overview: pre-received dictionary with open trades, returned by `Overview()` method.
                         This avoids unnecessary downloading data from the server.
        """
        if not tickers:
            uLogger.info("Tickers list is empty, nothing to close.")

        else:
            if overview is None or not overview:
                overview = self.Overview(showStatistics=False)

            allOpenedTickers = [item["ticker"] for iType in TKS_INSTRUMENTS for item in overview["stat"][iType]]
            uLogger.debug("All opened instruments by it's tickers names: {}".format(allOpenedTickers))

            for ticker in tickers:
                if ticker not in allOpenedTickers:
                    uLogger.warning("Instrument with ticker [{}] not in open positions list!".format(ticker))
                    continue

                # search open trade info about instrument by ticker:
                instrument = {}
                for iType in TKS_INSTRUMENTS:
                    if instrument:
                        break

                    for item in overview["stat"][iType]:
                        if item["ticker"] == ticker:
                            instrument = item
                            break

                if instrument:
                    self.ticker = ticker
                    self.figi = instrument["figi"]

                    uLogger.debug("Closing trade of instrument: ticker [{}], FIGI[{}], lots [{}]{}. Wait, please...".format(
                        self.ticker,
                        self.figi,
                        int(instrument["volume"]),
                        ", blocked [{}]".format(instrument["blocked"]) if instrument["blocked"] > 0 else "",
                    ))

                    tradeLots = abs(instrument["lots"]) - instrument["blocked"]  # available volumes in lots for close operation

                    if tradeLots > 0:
                        if instrument["blocked"] > 0:
                            uLogger.warning("Just for your information: there are [{}] lots blocked for instrument [{}]! Available only [{}] lots to closing trade.".format(
                                instrument["blocked"],
                                self.ticker,
                                tradeLots,
                            ))

                        # if direction is "Long" then we need sell, if direction is "Short" then we need buy:
                        self.Trade(operation="Sell" if instrument["direction"] == "Long" else "Buy", lots=tradeLots)

                    else:
                        uLogger.warning("There are no available lots for instrument [{}] to closing trade at this moment! Try again later or cancel some orders.".format(self.ticker))

    def CloseAllTrades(self, iType: str, overview: dict = None) -> None:
        """
        Close all positions of given instruments with defined type.

        :param iType: type of the instruments that be closed, it must be one of supported types in TKS_INSTRUMENTS list.
        :param overview: pre-received dictionary with open trades, returned by `Overview()` method.
                         This avoids unnecessary downloading data from the server.
        """
        if iType not in TKS_INSTRUMENTS:
            uLogger.warning("Type of the instrument must be one of supported types: {}. Given: [{}]".format(", ".join(TKS_INSTRUMENTS), iType))

        else:
            if overview is None or not overview:
                overview = self.Overview(showStatistics=False)

            tickers = [item["ticker"] for item in overview["stat"][iType]]
            uLogger.debug("Instrument tickers with type [{}] that will be closed: {}".format(iType, tickers))

            if tickers and overview:
                self.CloseTrades(tickers, overview)

            else:
                uLogger.info("Instrument tickers with type [{}] not found, nothing to close.".format(iType))

    def Order(self, operation: str, orderType: str, lots: int, targetPrice: float, limitPrice: float = 0., stopType: str = "Limit", expDate: str = "Undefined") -> dict:
        """
        Universal method to create market or limit orders with all available parameters.
        See more simple methods: `BuyLimit()`, `BuyStop()`, `SellLimit()`, `SellStop()`.

        If orderType is "Limit" then create pending limit-order below current price if operation is "Buy" and above
        current price if operation is "Sell". A limit order has no expiration date, it lasts until the end of the trading day.

        Warning! If you try to create limit-order above current price if "Buy" or below current price if "Sell"
        then broker immediately open market order as you can do simple --buy or --sell operations!

        If orderType is "Stop" then creates stop-order with any direction "Buy" or "Sell".
        When current price will go up or down to target price value then broker opens a limit order.
        Stop-order is opened with unlimited expiration date by default, or you can define expiration date with expDate parameter.

        Only one attempt and no retry for opens order. If network issue occurred you can create new request.

        :param operation: string "Buy" or "Sell".
        :param orderType: string "Limit" or "Stop".
        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is open trade price for limit order.
        :param limitPrice: limit price >= 0. This parameter only makes sense for stop-order. If limitPrice = 0, then it set as targetPrice.
                           Broker will creates limit-order with price equal to limitPrice, when current price goes to target price of stop-order.
        :param stopType: string "Limit" by default. This parameter only makes sense for stop-order. There are 3 stop-order types
                         "SL", "TP", "Limit" for "Stop loss", "Take profit" and "Stop limit" types accordingly.
                         Stop loss order always executed by market price.
        :param expDate: string "Undefined" by default or local date in future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
                        This date is converting to UTC format for server. This parameter only makes sense for stop-order.
                        A limit order has no expiration date, it lasts until the end of the trading day.
        :return: JSON with response from broker server.
        """
        if operation is None or not operation or operation not in ("Buy", "Sell"):
            raise Exception("You must define operation type only one of them: `Buy` or `Sell`!")

        if orderType is None or not orderType or orderType not in ("Limit", "Stop"):
            raise Exception("You must define order type only one of them: `Limit` or `Stop`!")

        if lots is None or lots < 1:
            raise Exception("You must define trade volume > 0: integer count of lots!")

        if targetPrice is None or targetPrice <= 0:
            raise Exception("Target price for limit-order must be greater than 0!")

        if limitPrice is None or limitPrice <= 0:
            limitPrice = targetPrice

        if stopType is None or not stopType or stopType not in ("SL", "TP", "Limit"):
            stopType = "Limit"

        if expDate is None or not expDate:
            expDate = "Undefined"

        if not (self.ticker or self.figi):
            raise Exception("`self.ticker` or `self.figi` variables must be defined!")

        response = {}
        instrument = self.SearchByTicker(requestPrice=True, debug=False) if self.ticker else self.SearchByFIGI(requestPrice=True, debug=False)
        self.ticker = instrument["ticker"]
        self.figi = instrument["figi"]

        if orderType == "Limit":
            uLogger.debug(
                "Creating pending limit-order: ticker [{}], FIGI [{}], action [{}], lots [{}] and the target price [{:.2f} {}]. Wait, please...".format(
                    self.ticker, self.figi,
                    operation, lots, targetPrice, instrument["currency"],
                ))

            openOrderURL = self.server + r"/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"
            self.body = str({
                "figi": self.figi,
                "quantity": str(lots),
                "price": FloatToNano(targetPrice),
                "direction": "ORDER_DIRECTION_BUY" if operation == "Buy" else "ORDER_DIRECTION_SELL",  # see: TKS_ORDER_DIRECTIONS
                "accountId": str(self.accountId),
                "orderType": "ORDER_TYPE_LIMIT",  # see: TKS_ORDER_TYPES
            })
            response = self.SendAPIRequest(openOrderURL, reqType="POST", retry=0, debug=False)

            if "orderId" in response.keys():
                uLogger.info(
                    "Limit-order [{}] was created: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{:.2f} {}]".format(
                        response["orderId"],
                        self.ticker, self.figi,
                        operation, lots, targetPrice, instrument["currency"],
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
                uLogger.warning("Not `oK` status received! Limit order not opened. See full debug log or try again and open order later.")

        if orderType == "Stop":
            uLogger.debug(
                "Creating stop-order: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{:.2f} {}], limit price [{:.2f} {}], stop-order type [{}] and local expiration date [{}]. Wait, please...".format(
                    self.ticker, self.figi,
                    operation, lots,
                    targetPrice, instrument["currency"],
                    limitPrice, instrument["currency"],
                    stopType, expDate,
                ))

            openOrderURL = self.server + r"/tinkoff.public.invest.api.contract.v1.StopOrdersService/PostStopOrder"
            expDateUTC = "" if expDate == "Undefined" else datetime.strptime(expDate, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tzlocal()).astimezone(tzutc()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            stopOrderType = "STOP_ORDER_TYPE_STOP_LOSS" if stopType == "SL" else "STOP_ORDER_TYPE_TAKE_PROFIT" if stopType == "TP" else "STOP_ORDER_TYPE_STOP_LIMIT"

            body = {
                "figi": self.figi,
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
            response = self.SendAPIRequest(openOrderURL, reqType="POST", retry=0, debug=False)

            if "stopOrderId" in response.keys():
                uLogger.info(
                    "Stop-order [{}] was created: ticker [{}], FIGI [{}], action [{}], lots [{}], target price [{:.2f} {}], limit price [{:.2f} {}], stop-order type [{}] and expiration date in UTC [{}]".format(
                    response["stopOrderId"],
                    self.ticker, self.figi,
                    operation, lots,
                    targetPrice, instrument["currency"],
                    limitPrice, instrument["currency"],
                    TKS_STOP_ORDER_TYPES[stopOrderType],
                    datetime.strptime(expDateUTC, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tzutc()).astimezone(tzutc()).strftime("%Y-%m-%d %H:%M:%S") if expDateUTC else TKS_STOP_ORDER_EXPIRATION_TYPES["STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED"],
                ))

                if "lastPrice" in instrument["currentPrice"].keys() and instrument["currentPrice"]["lastPrice"]:
                    if operation == "Buy" and targetPrice < instrument["currentPrice"]["lastPrice"] and stopType != "TP":
                        uLogger.warning("The broker will cancel this order after some time. Comment: you placed the wrong stop order because the target buy price [{:.2f} {}] is lower than the current price [{:.2f} {}]. Also try to set up order type as `TP` if you want to place stop order at that price.".format(
                            targetPrice, instrument["currency"],
                            instrument["currentPrice"]["lastPrice"], instrument["currency"],
                        ))

                    if operation == "Sell" and targetPrice > instrument["currentPrice"]["lastPrice"] and stopType != "TP":
                        uLogger.warning("The broker will cancel this order after some time. Comment: you placed the wrong stop order because the target sell price [{:.2f} {}] is higher than the current price [{:.2f} {}]. Also try to set up order type as `TP` if you want to place stop order at that price.".format(
                            targetPrice, instrument["currency"],
                            instrument["currentPrice"]["lastPrice"], instrument["currency"],
                        ))

            else:
                uLogger.warning("Not `oK` status received! Stop order not opened. See full debug log or try again and open order later.")

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
        :param limitPrice: limit price >= 0 (limitPrice = targetPrice if limitPrice is 0). Broker will creates limit-order
                           with price equal to limitPrice, when current price goes to target price of buy stop-order.
        :param stopType: string "Limit" by default. There are 3 stop-order types "SL", "TP", "Limit"
                         for "Stop loss", "Take profit" and "Stop limit" types accordingly.
        :param expDate: string "Undefined" by default or local date in future.
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
        In additional you can specify 3 parameters for sell stop-order: `limit price` >=0, `stop type` = Limit|SL|TP,
        `expiration date` = Undefined|`%%Y-%%m-%%d %%H:%%M:%%S`. When current price will go up or down to
        target price value then broker opens a limit order. See also: `Order()` docstring.

        :param lots: volume, integer count of lots >= 1.
        :param targetPrice: target price > 0. This is trigger price for sell stop-order.
        :param limitPrice: limit price >= 0 (limitPrice = targetPrice if limitPrice is 0). Broker will creates limit-order
                           with price equal to limitPrice, when current price goes to target price of sell stop-order.
        :param stopType: string "Limit" by default. There are 3 stop-order types "SL", "TP", "Limit"
                         for "Stop loss", "Take profit" and "Stop limit" types accordingly.
        :param expDate: string "Undefined" by default or local date in future.
                        String has a format like this: `%Y-%m-%d %H:%M:%S`.
                        This date is converting to UTC format for server.
        :return: JSON with response from broker server.
        """
        return self.Order(operation="Sell", orderType="Stop", lots=lots, targetPrice=targetPrice, limitPrice=limitPrice, stopType=stopType, expDate=expDate)

    def CloseOrders(self, orderIDs: list, allOrdersIDs: list = None, allStopOrdersIDs: list = None) -> None:
        """
        Cancel order or list of orders by its `orderId` or `stopOrderId`.

        :param orderIDs: list of integers with `orderId` or `stopOrderId`.
        :param allOrdersIDs: pre-received lists of all active pending orders.
                             This avoids unnecessary downloading data from the server.
        :param allStopOrdersIDs: pre-received lists of all active stop orders.
        """
        if orderIDs:
            if allOrdersIDs is None or not allOrdersIDs:
                rawOrders = self.RequestPendingOrders()
                allOrdersIDs = [item["orderId"] for item in rawOrders]  # all pending orders ID

            if allStopOrdersIDs is None or not allStopOrdersIDs:
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
        allOrdersIDs = [item["orderId"] for item in rawOrders]  # all pending orders ID
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

        Also you can select one or more keywords case insensitive:
        `orders`, `shares`, `bonds`, `etfs` and `futures` from `TKS_INSTRUMENTS` enum to specify trades type.

        Currency positions you must closes manually using buy or sell operations, `CloseTrades()` or `CloseAllTrades()` methods.
        """
        overview = self.Overview(showStatistics=False)  # get all open trades info

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
        #     raise Exception("You must define operation type: 'Buy' or 'Sell'!")
        #
        # if "l" in inputParameters.keys():
        #     inputParameters["lots"] = inputParameters.pop("l")
        #
        # if "p" in inputParameters.keys():
        #     inputParameters["prices"] = inputParameters.pop("p")
        #
        # if "lots" not in inputParameters.keys() or "prices" not in inputParameters.keys():
        #     raise Exception("Both of 'lots' and 'prices' keys must be define to open grid orders!")
        #
        # lots = [int(item.strip()) for item in inputParameters["lots"].split(",")]
        # prices = [float(item.strip()) for item in inputParameters["prices"].split(",")]
        #
        # if len(lots) != len(prices):
        #     raise Exception("'lots' and 'prices' lists must have equal length of values!")
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
            portfolio = self.Overview(showStatistics=False)

        if self.ticker:
            uLogger.debug("Searching instrument with ticker [{}] throwout opened positions...".format(self.ticker))
            msg = "Instrument with ticker [{}] is not present in open positions".format(self.ticker)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["ticker"] == self.ticker:
                        result = True
                        msg = "Instrument with ticker [{}] is present in open positions".format(self.ticker)
                        break

        elif self.figi:
            uLogger.debug("Searching instrument with FIGI [{}] throwout opened positions...".format(self.figi))
            msg = "Instrument with FIGI [{}] is not present in open positions".format(self.figi)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["figi"] == self.figi:
                        result = True
                        msg = "Instrument with FIGI [{}] is present in open positions".format(self.figi)
                        break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result

    def GetInstrumentFromPortfolio(self, portfolio: dict = None) -> dict:
        """
        Returns instrument is in the user's portfolio if it presents there.
        Instrument must be defined by `ticker` (highly priority) or `figi`.

        :param portfolio: dict with user's portfolio data. If `None`, then requests portfolio from `Overview()` method.
        :return: dict with instrument if portfolio contains open position with this instrument, `None` otherwise.
        """
        result = None
        msg = "Instrument not defined!"

        if portfolio is None or not portfolio:
            portfolio = self.Overview(showStatistics=False)

        if self.ticker:
            uLogger.debug("Searching instrument with ticker [{}] throwout opened positions...".format(self.ticker))
            msg = "Instrument with ticker [{}] is not present in open positions".format(self.ticker)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["ticker"] == self.ticker:
                        result = instrument
                        msg = "Instrument with ticker [{}] and FIGI [{}] is present in open positions".format(self.ticker, instrument["figi"])
                        break

        elif self.figi:
            uLogger.debug("Searching instrument with FIGI [{}] throwout opened positions...".format(self.figi))
            msg = "Instrument with FIGI [{}] is not present in open positions".format(self.figi)

            for iType in TKS_INSTRUMENTS:
                for instrument in portfolio["stat"][iType]:
                    if instrument["figi"] == self.figi:
                        result = instrument
                        msg = "Instrument with ticker [{}] and FIGI [{}] is present in open positions".format(instrument["ticker"], self.figi)
                        break

        else:
            uLogger.warning("Instrument must be defined by `ticker` (highly priority) or `figi`!")

        uLogger.debug(msg)

        return result


class Args:
    """
    If `Main()` function is imported as module, then this class used to convert arguments from **kwargs as object.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return None


def ParseArgs():
    """
    Function get and parse command line keys. See examples: https://tim55667757.github.io/TKSBrokerAPI/
    """
    parser = ArgumentParser()  # command-line string parser

    parser.description = "TKSBrokerAPI is a python API to work with some methods of Tinkoff Open API using REST protocol. It can view history, orders and market information. Also, you can open orders and trades. See examples: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Usage-examples"
    parser.usage = "\n/as module/ python TKSBrokerAPI.py [some options] [one command]\n/as CLI tool/ tksbrokerapi [some options] [one command]"

    # --- options:

    parser.add_argument("--no-cache", action="store_true", default=False, help="Option: not use local cache `dump.json`, but update raw instruments data when starting the program. `False` by default.")
    parser.add_argument("--token", type=str, help="Option: Tinkoff service's api key. If not set then used environment variable `TKS_API_TOKEN`. See how to use: https://tinkoff.github.io/investAPI/token/")
    parser.add_argument("--account-id", type=str, default=None, help="Option: string with an user numeric account ID in Tinkoff Broker. It can be found in any broker's reports (see the contract number). Also, this variable can be set from environment variable `TKS_ACCOUNT_ID`.")

    parser.add_argument("--ticker", "-t", type=str, help="Option: instrument's ticker, e.g. `IBM`, `YNDX`, `GOOGL` etc. Use alias for `USD000UTSTOM` simple as `USD`, `EUR_RUB__TOM` as `EUR`.")
    parser.add_argument("--figi", "-f", type=str, help="Option: instrument's FIGI, e.g. `BBG006L8G4H1` (for `YNDX`).")

    parser.add_argument("--depth", type=int, default=1, help="Option: Depth of Market (DOM) can be >=1, 1 by default.")
    parser.add_argument("--no-cancelled", action="store_true", default=False, help="Option: remove information about cancelled operations from the deals report by the `--deals` key. `False` by default.")

    parser.add_argument("--output", type=str, default=None, help="Option: replace default paths to output files for some commands. If None then used default files.")

    # parser.add_argument("--length", type=int, default=24, help="Option: how many last candles returns for history. Used only with --history key.")
    # parser.add_argument("--interval", type=str, default="60", help="Option: available values are 1min, 2min, 3min, 5min, 10min, 15min, 30min, hour, day, week, month. Used only with `--history` key. This is time period used in 'interval' api parameter. Default: `--interval=60` that means 60 min for every history candles.")
    # parser.add_argument("--only-missing", action="store_true", default=False, help="Option: if history file define by `--output` key then add only last missing candles, do not request all history length. False by default.")

    parser.add_argument("--debug-level", "--verbosity", "-v", type=int, default=20, help="Option: showing STDOUT messages of minimal debug level, e.g. 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 = ERROR, 50 = CRITICAL. INFO (20) by default.")

    # --- commands:

    parser.add_argument("--list", "-l", action="store_true", help="Action: get and print all available instruments and some information from broker server. Also, you can define `--output` key to save list of instruments to file, default: `instruments.md`.")
    parser.add_argument("--search", "-s", type=str, nargs=1, help="Action: search for an instruments by part of the name, ticker or FIGI. Also, you can define `--output` key to save results to file, default: `search-results.md`.")
    parser.add_argument("--info", "-i", action="store_true", help="Action: get information from broker server about instrument by it's ticker or FIGI. `--ticker` key or `--figi` key must be defined!")
    parser.add_argument("--price", action="store_true", help="Action: show actual price list for current instrument. Also, you can use --depth key. `--ticker` key or `--figi` key must be defined!")
    parser.add_argument("--prices", "-p", type=str, nargs="+", help="Action: get and print current prices for list of given instruments (by it's tickers or by FIGIs). WARNING! This is too long operation if you request a lot of instruments! Also, you can define `--output` key to save list of prices to file, default: `prices.md`.")

    parser.add_argument("--overview", "-o", action="store_true", help="Action: show all open positions, orders and some statistics. Also, you can define `--output` key to save this information to file, default: `overview.md`.")
    parser.add_argument("--deals", "-d", type=str, nargs="*", help="Action: show all deals between two given dates. Start day may be an integer number: -1, -2, -3 days ago. Also, you can use keywords: `today`, `yesterday` (-1), `week` (-7), `month` (-30) and `year` (-365). Dates format must be: `%%Y-%%m-%%d`, e.g. 2020-02-03. With `--no-cancelled` key information about cancelled operations will be removed from the deals report. Also, you can define `--output` key to save all deals to file, default: `deals.md`.")
    # parser.add_argument("--history", action="store_true", help="Action: get last (--length) history candles from past to current time with (--interval) values. Also, you can define `--output` key to save history candles to .csv-file.")

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
    parser.add_argument("--close-trade", "--cancel-trade", action="store_true", help="Action: close only one position for instrument defined by `--ticker` key, including for currencies tickers.")
    parser.add_argument("--close-trades", "--cancel-trades", type=str, nargs="+", help="Action: close positions for list of tickers, including for currencies tickers.")
    parser.add_argument("--close-all", "--cancel-all", type=str, nargs="*", help="Action: close all available (not blocked) opened trades and orders, excluding for currencies. Also you can select one or more keywords case insensitive to specify trades type: `orders`, `shares`, `bonds`, `etfs` and `futures`, but not `currencies`. Currency positions you must closes manually using `--buy`, `--sell`, `--close-trade` or `--close-trades` operations.")

    cmdArgs = parser.parse_args()
    return cmdArgs


def Main(**kwargs):
    """
    Main function for work with Tinkoff Open API service. It realizes simple logic: get a lot of options and execute one command.

    See examples: https://tim55667757.github.io/TKSBrokerAPI/
    """
    args = Args(**kwargs) if kwargs else ParseArgs()  # get and parse command-line parameters or use **kwarg parameters

    if args.debug_level:
        uLogger.level = 10  # always debug level by default
        uLogger.handlers[0].level = args.debug_level  # level for STDOUT

    exitCode = 0
    start = datetime.now(tzutc())
    uLogger.debug("TKSBrokerAPI module started at: [{}] (UTC), it is [{}] local time".format(
        start.strftime("%Y-%m-%d %H:%M:%S"),
        start.astimezone(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
    ))

    # Init class for trading with Tinkoff Broker:
    server = TinkoffBrokerServer(
        token=args.token,
        accountId=args.account_id,
        iList=kwargs["instruments"] if kwargs and "instruments" in kwargs.keys() else None,  # re-use iList
        useCache=not args.no_cache,
    )

    try:
        # --- set some options:

        if args.ticker:
            if args.ticker in server.aliasesKeys:
                server.ticker = server.aliases[args.ticker]  # Replace some tickers with it's aliases

            else:
                server.ticker = args.ticker

        if args.figi:
            server.figi = args.figi

        if args.depth is not None:
            server.depth = args.depth

        # if args.length is not None:
        #     server.historyLength = args.length
        #
        # if args.interval is not None:
        #     server.historyInterval = args.interval

        # --- do one of commands:

        if args.list:
            if args.output is not None:
                server.instrumentsFile = args.output

            server.ShowInstrumentsInfo(showInstruments=True)

        elif args.search:
            if args.output is not None:
                server.searchResultsFile = args.output

            server.SearchInstruments(pattern=args.search[0], showResults=True)

        elif args.info:
            if not (args.ticker or args.figi):
                raise Exception("`--ticker` key or `--figi` key is required for this operation!")

            if args.ticker:
                server.SearchByTicker(requestPrice=True, showInfo=True, debug=False)  # show info and current prices by ticker name

            else:
                server.SearchByFIGI(requestPrice=True, showInfo=True, debug=False)  # show info and current prices by FIGI id

        elif args.price:
            if not (args.ticker or args.figi):
                raise Exception("`--ticker` key or `--figi` key is required for this operation!")

            server.GetCurrentPrices(showPrice=True)

        elif args.prices is not None:
            if args.output is not None:
                server.pricesFile = args.output

            server.GetListOfPrices(instruments=args.prices, showPrices=True)  # WARNING: too long wait for a lot of instruments prices

        elif args.overview:
            if args.output is not None:
                server.overviewFile = args.output

            server.Overview(showStatistics=True)

        elif args.deals is not None:
            if args.output is not None:
                server.reportFile = args.output

            if 0 <= len(args.deals) < 3:
                server.Deals(
                    start=args.deals[0] if len(args.deals) >= 1 else None,
                    end=args.deals[1] if len(args.deals) == 2 else None,
                    printDeals=True,  # Always show deals report in console
                    showCancelled=not args.no_cancelled,  # If --no-cancelled key then remove cancelled operations from the deals report. False by default.
                )

            else:
                raise Exception("You must specify 0-2 parameters: [DATE_START] [DATE_END]")

        # TODO: implement history download and view
        # elif args.history:
        #     if args.output is not None:
        #         server.historyFile = args.output
        #
        #     server.History(onlyMissing=args.only_missing)

        elif args.trade is not None:
            if 1 <= len(args.trade) <= 5:
                server.Trade(
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
                server.Buy(
                    lots=int(args.buy[0]) if len(args.buy) >= 1 else 1,
                    tp=float(args.buy[1]) if len(args.buy) >= 2 else 0.,
                    sl=float(args.buy[2]) if len(args.buy) >= 3 else 0.,
                    expDate=args.buy[3] if len(args.buy) == 4 else "Undefined",
                )

            else:
                uLogger.error("You must specify 0-4 parameters to open buy position: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

        elif args.sell is not None:
            if 0 <= len(args.sell) <= 4:
                server.Sell(
                    lots=int(args.sell[0]) if len(args.sell) >= 1 else 1,
                    tp=float(args.sell[1]) if len(args.sell) >= 2 else 0.,
                    sl=float(args.sell[2]) if len(args.sell) >= 3 else 0.,
                    expDate=args.sell[3] if len(args.sell) == 4 else "Undefined",
                )

            else:
                uLogger.error("You must specify 0-4 parameters to open sell position: [lots, >= 1] [take profit, >= 0] [stop loss, >= 0] [expiration date for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See: `python TKSBrokerAPI.py --help`")

        elif args.order:
            if 4 <= len(args.order) <= 7:
                server.Order(
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
            server.BuyLimit(lots=int(args.buy_limit[0]), targetPrice=args.buy_limit[1])

        elif args.sell_limit:
            server.SellLimit(lots=int(args.sell_limit[0]), targetPrice=args.sell_limit[1])

        elif args.buy_stop:
            if 2 <= len(args.buy_stop) <= 7:
                server.BuyStop(
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
                server.SellStop(
                    lots=int(args.sell_stop[0]),
                    targetPrice=float(args.sell_stop[1]),
                    limitPrice=float(args.sell_stop[2]) if len(args.sell_stop) >= 3 else 0.,
                    stopType=args.sell_stop[3] if len(args.sell_stop) >= 4 else "Limit",
                    expDate=args.sell_stop[4] if len(args.sell_stop) == 5 else "Undefined",
                )

            else:
                uLogger.error("You must specify 2-5 parameters for sell stop-order: [lots] [target price] [limit price, >= 0] [stop type, Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d %H:%M:%S`]. See: python TKSBrokerAPI.py --help")

        # elif args.buy_order_grid is not None:
        #     # TODO: update order grid work with api v2
        #     if len(args.buy_order_grid) == 2:
        #         orderParams = server.ParseOrderParameters(operation="Buy", **dict(kw.split('=') for kw in args.buy_order_grid))
        #
        #         for order in orderParams:
        #             server.Order(operation="Buy", lots=order["lot"], price=order["price"])
        #
        #     else:
        #         uLogger.error("To open grid of pending BUY limit-orders (below current price) you must specified 2 parameters: l(ots)=[L_int,...] p(rices)=[P_float,...]. See: `python TKSBrokerAPI.py --help`")
        #
        # elif args.sell_order_grid is not None:
        #     # TODO: update order grid work with api v2
        #     if len(args.sell_order_grid) >= 2:
        #         orderParams = server.ParseOrderParameters(operation="Sell", **dict(kw.split('=') for kw in args.sell_order_grid))
        #
        #         for order in orderParams:
        #             server.Order(operation="Sell", lots=order["lot"], price=order["price"])
        #
        #     else:
        #         uLogger.error("To open grid of pending SELL limit-orders (above current price) you must specified 2 parameters: l(ots)=[L_int,...] p(rices)=[P_float,...]. See: `python TKSBrokerAPI.py --help`")

        elif args.close_order is not None:
            server.CloseOrders(args.close_order)  # close only one order

        elif args.close_orders is not None:
            server.CloseOrders(args.close_orders)  # close list of orders

        elif args.close_trade:
            if not args.ticker:
                raise Exception("`--ticker` key is required for this operation!")

            server.CloseTrades([args.ticker])  # close only one trade

        elif args.close_trades is not None:
            server.CloseTrades(args.close_trades)  # close trades for list of tickers

        elif args.close_all is not None:
            server.CloseAll(*args.close_all)

        else:
            uLogger.error("There is no command to execute! One of the possible commands must be selected. See: `python TKSBrokerAPI.py --help`")
            raise Exception("There is no command to execute!")

    except Exception:
        exc = tb.format_exc().split("\n")

        for line in exc:
            if line:
                uLogger.debug(line)

        uLogger.debug("Unknown error occurred, open a ticket for this issue, please! https://github.com/Tim55667757/TKSBrokerAPI/issues")
        exitCode = 255  # unknown error occurred, must be open a ticket for this issue

    finally:
        finish = datetime.now(tzutc())

        if exitCode == 0:
            uLogger.debug("All operations with Tinkoff Server using Open API are finished success (summary code is 0).")

        else:
            uLogger.error("TKSBrokerAPI module returns an error! See full debug log with key in run command `--debug-level 10`. Summary code: {}".format(exitCode))

        uLogger.debug("TKSBrokerAPI module work duration: [{}]".format(finish - start))
        uLogger.debug("TKSBrokerAPI module finished: [{}] (UTC), it is [{}] local time".format(
            finish.strftime("%Y-%m-%d %H:%M:%S"),
            finish.astimezone(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
        ))

        if not kwargs:
            sys.exit(exitCode)

        else:
            return exitCode


if __name__ == "__main__":
    Main()
