# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)

The **TradeRoutines** library contains some methods used by trade scenarios implemented with TKSBrokerAPI module.

- **TKSBrokerAPI module documentation:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
- **TKSBrokerAPI CLI examples:** https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md
- **About Tinkoff Invest API:** https://tinkoff.github.io/investAPI/
- **Tinkoff Invest API documentation:** https://tinkoff.github.io/investAPI/swagger-ui/
- **Open account for trading:** https://tinkoff.ru/sl/AaX1Et1omnH
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


from datetime import datetime, timedelta
from dateutil.tz import tzutc
import math
import pandas as pd
import numpy as np
from scipy.stats import norm
from numba import jit

from typing import Union, Optional, Any

from fuzzyroutines import FuzzyRoutines as fR  # Some routines to simplify working with fuzzy logic operators, fuzzy datasets and fuzzy scales.


# --- Main constants:

NANO = 0.000000001
"""SI-constant: `NANO = 10^-9`"""

FUZZY_SCALE = fR.UniversalFuzzyScale()
"""Universal Fuzzy Scale is a special set of fuzzy levels: `{Min, Low, Med, High, Max}`."""

FUZZY_LEVELS = list(FUZZY_SCALE.levelsNames.keys())
"""Level names on Universal Fuzzy Scale `FUZZY_SCALE`. Default: `["Min", "Low", "Med", "High", "Max"]`."""

for level in FUZZY_SCALE.levels:
    level["fSet"].mFunction.accuracy = 100  # Fast hack to increase speed of calculation with reduce accuracy.

SIGNAL_FILTER = {
    "Max": {"Max": "Max", "High": "High", "Med": "Med", "Low": "Low", "Min": "Min"},  # If [Max] probability, then stay signal as is.
    "High": {"Max": "High", "High": "Med", "Med": "Low", "Low": "Min", "Min": "Min"},  # If [High] probability, then reduce signal strength at 1 level.
    "Med": {"Max": "Med", "High": "Low", "Med": "Min", "Low": "Min", "Min": "Min"},  # If [Med] probability, then reduce signal strength at 2 level.
    "Low": {"Max": "Low", "High": "Min", "Med": "Min", "Low": "Min", "Min": "Min"},  # If [Low] probability, then reduce signal strength at 3 level.
    "Min": {"Max": "Min", "High": "Min", "Med": "Min", "Low": "Min", "Min": "Min"},  # If [Min] probability, then reduce signal strength at 4 level.
}
"""Signal filter by default is used to reduce signal strength."""

OPENING_RULES = pd.DataFrame([
    # Min    Low    Med   High  Max            (Reach →)
    [False, False, True, True, True],     # Min (Risk ↓)
    [False, False, True, True, True],     # Low
    [False, False, True, True, True],     # Med
    [False, False, False, False, False],  # High
    [False, False, False, False, False],  # Max
],
    index=FUZZY_LEVELS,  # Fuzzy Risk Levels (table's row index): ["Min", "Low", "Med", "High", "Max"]
    columns=FUZZY_LEVELS,  # Fuzzy Reach Levels (table's column index): ["Min", "Low", "Med", "High", "Max"]
    dtype=bool,
)
"""
Opening positions rules depend of fuzzy Risk/Reach levels.

This is the author's technique, proposed by [Timur Gilmullin](https://www.linkedin.com/in/tgilmullin) and [Mansur Gilmullin](https://www.linkedin.com/in/mgilmullin),
based on fuzzy scales for measuring the levels of fuzzy risk and reachable. The following simple diagram explains what do we mean as Open/Close Fuzzy Rules:

<img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/005-Open-Close-Rules-Matrix.png?raw=true" alt="Open-Close-Rules-Matrix" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />

Here in table `T` mean `True`, `F` mean `False`. 1st position is for Opening rules, 2nd position is for Closing rules.
These rules are defined as transposed matrix constants `OPENING_RULES` and `CLOSING_RULES`.

See also:
  - An Engineering View of Trading: How a Trading Robot's Signal Algorithm Works: [RU](https://teletype.in/@tgilmullin/trading-algorithm).
  - [FuzzyRoutines](https://github.com/devopshq/FuzzyRoutines) library.
  - How to work with Universal Fuzzy Scales: [EN](https://github.com/devopshq/FuzzyRoutines#Chapter_2_4), [RU](https://math-n-algo.blogspot.com/2014/08/FuzzyClassificator.html#chapter_3).
  - `CLOSING_RULES` constant, `CanOpen()` and `CanClose()` methods.

Default rules for opening positions:

| Risk \ Reach | Min   | Low   | Med   | High  | Max   |
|--------------|-------|-------|-------|-------|-------|
| Min          | False | False | True  | True  | True  |
| Low          | False | False | True  | True  | True  |
| Med          | False | False | True  | True  | True  |
| High         | False | False | False | False | False |
| Max          | False | False | False | False | False |
"""

CLOSING_RULES = pd.DataFrame([
    # Min    Low    Med   High  Max            (Reach →)
    [False, False, False, False, False],  # Min (Risk ↓)
    [False, False, False, False, False],  # Low
    [True, True, False, False, False],    # Med
    [True, True, True, False, False],     # High
    [True, True, True, False, False],     # Max
],
    index=FUZZY_LEVELS,  # Fuzzy Risk Levels (table's row index): ["Min", "Low", "Med", "High", "Max"]
    columns=FUZZY_LEVELS,  # Fuzzy Reach Levels (table's column index): ["Min", "Low", "Med", "High", "Max"]
    dtype=bool,
)
"""
Closing positions rules depend of fuzzy Risk/Reach levels. These rules are opposite for `OPENING_RULES`
(see explanation there what do we mean as Open/Close Fuzzy Rules).

See also: `CanClose()` method.

Default rules for closing positions:

| Risk \ Reach | Min   | Low   | Med   | High  | Max   |
|--------------|-------|-------|-------|-------|-------|
| Min          | False | False | False | False | False |
| Low          | False | False | False | False | False |
| Med          | True  | True  | False | False | False |
| High         | True  | True  | True  | False | False |
| Max          | True  | True  | True  | False | False |
"""


def CanOpen(fuzzyRisk: str, fuzzyReach: str) -> bool:
    """
    Checks opening positions rules in `OPENING_RULES` depend on fuzzy Risk/Reach levels.

    See also:
    - `OPENING_RULES` constant,
    - `FUZZY_LEVELS` and `FUZZY_SCALE` constants,
    - `RiskLong()` and `RiskShort()` methods,
    - `ReachLong()` and `ReachShort()` methods.

    :param fuzzyRisk: Fuzzy Risk level name.
    :param fuzzyReach: Fuzzy Reach level name.

    :return: Bool. If `True`, then possible to open position.
    """
    if fuzzyRisk not in FUZZY_LEVELS:
        raise Exception("Invalid fuzzy risk level name [{}]! Correct levels on Universal Fuzzy Scale: {}".format(fuzzyRisk, FUZZY_LEVELS))

    if fuzzyReach not in FUZZY_LEVELS:
        raise Exception("Invalid fuzzy reach level name [{}]! Correct levels on Universal Fuzzy Scale: {}".format(fuzzyReach, FUZZY_LEVELS))

    return bool(OPENING_RULES.loc[fuzzyRisk, fuzzyReach])


def CanClose(fuzzyRisk: str, fuzzyReach: str) -> bool:
    """
    Checks closing positions rules in `CLOSING_RULES` depend on fuzzy Risk/Reach levels.

    See also:
    - `CLOSING_RULES` constant,
    - `FUZZY_LEVELS` and `FUZZY_SCALE` constants,
    - `RiskLong()` and `RiskShort()` methods,
    - `ReachLong()` and `ReachShort()` methods.

    :param fuzzyRisk: Fuzzy Risk level name.
    :param fuzzyReach: Fuzzy Reach level name.

    :return: Bool. If `True`, then possible to close position.
    """
    if fuzzyRisk not in FUZZY_LEVELS:
        raise Exception("Invalid fuzzy risk level name [{}]! Correct levels on Universal Fuzzy Scale: {}".format(fuzzyRisk, FUZZY_LEVELS))

    if fuzzyReach not in FUZZY_LEVELS:
        raise Exception("Invalid fuzzy reach level name [{}]! Correct levels on Universal Fuzzy Scale: {}".format(fuzzyReach, FUZZY_LEVELS))

    return bool(CLOSING_RULES.loc[fuzzyRisk, fuzzyReach])


def RiskLong(curPrice: float, pHighest: float, pLowest: float) -> dict[str, float]:
    """
    Function returns Risk as fuzzy level and percents of Risk in the range [0, 100], if you want buy from current price.

    This is the author's method, proposed by [Timur Gilmullin](https://www.linkedin.com/in/tgilmullin) and [Mansur Gilmullin](https://www.linkedin.com/in/mgilmullin),
    based on fuzzy scales for measuring the levels of Fuzzy Risk. The following simple diagram explains what do we mean as Fuzzy Risk level:

    <img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/003-Risk.png?raw=true" alt="Fuzzy-Risk" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />

    - If open long (buy) position from current price: `RiskLong = Fuzzy(|P - L| / (H - L))`. Here:
      - `P` is the current price,
      - `L (H)` is the lowest (highest) price in forecasted movements of candles chain or prognoses diapason border of price movement,
      - `Fuzzy()` is the fuzzyfication function that convert real values to its fuzzy representation.

    See also:
    - An Engineering View of Trading: How a Trading Robot's Signal Algorithm Works: [RU](https://teletype.in/@tgilmullin/trading-algorithm).
    - [FuzzyRoutines](https://github.com/devopshq/FuzzyRoutines) library.
    - How to work with Universal Fuzzy Scales: [EN](https://github.com/devopshq/FuzzyRoutines#Chapter_2_4), [RU](https://math-n-algo.blogspot.com/2014/08/FuzzyClassificator.html#chapter_3).
    - `RiskShort()` method,
    - `CanOpen()` and `CanClose()` methods.
    - `ReachLong()` and `ReachShort()` methods.

    :param curPrice: Current actual price (usually the latest close price).
    :param pHighest: The highest close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement.
    :param pLowest: The lowest close price in forecasted movements of candles chain or prognosis of the lowest diapason border of price movement.

    :return: Dictionary with Fuzzy Risk level and Risk percents, e.g. `{"riskFuzzy": "High", "riskPercent": 66.67}`.
    """
    if pHighest < pLowest:
        raise Exception("The highest [{}] close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement must be greater than the lowest [{}] close price!".format(pHighest, pLowest))

    if curPrice < pLowest:
        curPrice = pLowest

    if curPrice > pHighest:
        curPrice = pHighest

    diapason = abs(pHighest - pLowest) if pHighest != pLowest else 1  # Prognosis diapason.
    riskBuy = abs(curPrice - pLowest) / diapason  # Risk if buy from current price in the range [0, 1].

    riskFuzzyBuy = FUZZY_SCALE.Fuzzy(riskBuy)["name"]  # Fuzzy Risk level if buy from current price.
    riskPercentBuy = 100 * riskBuy  # Risk percent if buy from current price in the range [0, 100].

    return {"riskFuzzy": riskFuzzyBuy, "riskPercent": riskPercentBuy}


def RiskShort(curPrice: float, pHighest: float, pLowest: float) -> dict[str, float]:
    """
    Function returns Risk as fuzzy level and percents of Risk in the range [0, 100], if you want sell from current price.
    This method is opposite for `RiskLong()` (see explanation there what do we mean as Fuzzy Risk).

    - If open short (sell) position from current price: `RiskShort = Fuzzy(|P - H| / (H - L))`. Here:
      - `P` is the current price,
      - `L (H)` is the lowest (highest) price in forecasted movements of candles chain or prognoses diapason border of price movement,
      - `Fuzzy()` is the fuzzyfication function that convert real values to its fuzzy representation.

    :param curPrice: Current actual price (usually the latest close price).
    :param pHighest: The highest close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement.
    :param pLowest: The lowest close price in forecasted movements of candles chain or prognosis of the lowest diapason border of price movement.

    :return: Dictionary with Fuzzy Risk level and Risk percents, e.g. `{"riskFuzzy": "Low", "riskPercent": 20.12}`.
    """
    if pHighest < pLowest:
        raise Exception("The highest [{}] close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement must be greater than the lowest [{}] close price!".format(pHighest, pLowest))

    if curPrice < pLowest:
        curPrice = pLowest

    if curPrice > pHighest:
        curPrice = pHighest

    diapason = abs(pHighest - pLowest) if pHighest != pLowest else 1  # Prognosis diapason.
    riskSell = abs(curPrice - pHighest) / diapason  # Risk if sell from current price in the range [0, 1].

    riskFuzzySell = FUZZY_SCALE.Fuzzy(riskSell)["name"]  # Fuzzy Risk level if sell from current price.
    riskPercentSell = 100 * riskSell  # Risk percent if sell from current price in the range [0, 100].

    return {"riskFuzzy": riskFuzzySell, "riskPercent": riskPercentSell}


def ReachLong(pClosing: pd.Series) -> dict[str, float]:
    """
    The Fuzzy Reach is a value of forecast reachable of price (highest or lowest close). In this function we calculate
    the reachability of the highest close price.

    This is the author's method, proposed by [Timur Gilmullin](https://www.linkedin.com/in/tgilmullin) and
    [Mansur Gilmullin](https://www.linkedin.com/in/mgilmullin), based on fuzzy scales for measuring the levels
    of Fuzzy Reach. The following simple diagram explains what is meant by the Fuzzy Reach level:

    <img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/004-Reachability.png?raw=true" alt="Fuzzy-Reach" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />

    There are fuzzy levels and percents in the range [0, 100] for the maximum and minimum forecasted close prices.
    Prognosis horizon is divided by 5 parts of time diapason: I, II, III, IV and V, from the first forecasted candle (or price)
    to the last forecasted candle (or price).

    Every part correlate with some fuzzy level, depending on the distance in time from current actual candle (or price):
    - `I = Max`,
    - `II = High`,
    - `III = Med`,
    - `IV = Low`,
    - `V = Min`.

    This function search for first fuzzy level appropriate to the part of time diapason, where the close price (highest or lowest)
    located in this diapason. Of course, you can use other price chains (open, high, low) instead of candle close prices,
    but usually this is not recommended.

    **Recommendation.** If you have no prognosis chain of candles just use `"Med"` Fuzzy Reach level.

    See also:
    - An Engineering View of Trading: How a Trading Robot's Signal Algorithm Works: [RU](https://teletype.in/@tgilmullin/trading-algorithm).
    - `OPENING_RULES` and `CLOSING_RULES` constants,
    - `CanOpen()` and `CanClose()` methods,
    - `FUZZY_LEVELS` and `FUZZY_SCALE` constants,
    - `RiskLong()` and `RiskShort()` methods,
    - `ReachShort()` method.

    :param pClosing: Pandas Series with prognosis chain of closing prices of candles. This is "close prices"
                     in OHLCV-formatted candles chain. The forecasted prices are indexed starting from zero,
                     this is the first candle of the forecast. The last price of the forecast is the "farthest"
                     relative to the current actual close price.

    :return: Dictionary with Fuzzy Reach level and Reach percents for the highest close price, e.g. `{"reachFuzzy": "Low", "reachPercent": 20.12}`.
    """
    count = pClosing.count()  # Length of candles chain

    if count == 0:
        raise Exception("Pandas Series can't be empty and must contain 1 or more elements!")

    elif count == 1:
        return {"reachFuzzy": "Max", "reachPercent": 100}

    else:
        indexHighest = pClosing.argmax()  # First occurrence of the highest close price in candles chain.

        # Reach of the highest prognosis close price (if buy from current price) in the range [0, 1]:
        if indexHighest == 0:
            reachBuy = 1

        elif indexHighest == count - 1:
            reachBuy = 0

        else:
            reachBuy = 1 - indexHighest / count

        reachFuzzyBuy = FUZZY_SCALE.Fuzzy(reachBuy)["name"]
        reachPercentBuy = 100 * reachBuy

        return {"reachFuzzy": reachFuzzyBuy, "reachPercent": reachPercentBuy}


def ReachShort(pClosing: pd.Series) -> dict[str, float]:
    """
    The Fuzzy Reach is a value of forecast reachable of price (highest or lowest close). This method is similar like
    `ReachLong()` (see explanation there what do we mean as Fuzzy Reach), but in this case we calculate the reachability
    of the lowest close price.

    :param pClosing: Pandas Series with prognosis chain of closing prices of candles. This is "close prices"
                     in OHLCV-formatted candles chain. The forecasted prices are indexed starting from zero,
                     this is the first candle of the forecast. The last price of the forecast is the "farthest"
                     relative to the current actual close price. **Recommendation.** If you have no prognosis chain
                     of candles just use `"Med"` Fuzzy Reach level.

    :return: Dictionary with Fuzzy Reach level and Reach percents for the lowest close price, e.g. `{"reachFuzzy": "High", "reachPercent": 66.67}`.
    """
    count = pClosing.count()  # Length of candles chain

    if count == 0:
        raise Exception("Pandas Series can't be empty and must contain 1 or more elements!")

    elif count == 1:
        return {"reachFuzzy": "Max", "reachPercent": 100}

    else:
        indexLowest = pClosing.argmin()  # First occurrence of the lowest close price in candles chain.

        # Reach of the lowest prognosis close price (if sell from current price) in the range [0, 1]:
        if indexLowest == 0:
            reachSell = 1

        elif indexLowest == count - 1:
            reachSell = 0

        else:
            reachSell = 1 - indexLowest / count

        reachFuzzySell = FUZZY_SCALE.Fuzzy(reachSell)["name"]
        reachPercentSell = 100 * reachSell

        return {"reachFuzzy": reachFuzzySell, "reachPercent": reachPercentSell}


def GetDatesAsString(start: str = None, end: str = None, userFormat: str = "%Y-%m-%d", outputFormat: str = "%Y-%m-%dT%H:%M:%SZ") -> tuple[str, str]:
    """
    Create tuple of date and time strings with timezone parsed from user-friendly date.

    Warning! All dates must be in UTC time zone!

    User dates format must be like: `"%Y-%m-%d"`, e.g. `"2020-02-03"` (3 Feb, 2020).

    Output date is UTC ISO time format by default: `"%Y-%m-%dT%H:%M:%SZ"`.

    Example input: `start="2022-06-01", end="2022-06-20"` -> output: `("2022-06-01T00:00:00Z", "2022-06-20T23:59:59Z")`.
    An error exception will occur if input date has incorrect format.

    If `start=None`, `end=None` then return dates from yesterday to the end of the day.

    If `start=some_date_1`, `end=None` then return dates from `some_date_1` to the end of the day.

    If `start=some_date_1`, `end=some_date_2` then return dates from start of `some_date_1` to end of `some_date_2`.

    Start day may be negative integer numbers: `-1`, `-2`, `-3` — how many days ago.

    Also, you can use keywords for start if `end=None`:
    - `today` (from 00:00:00 to the end of current day),
    - `yesterday` (-1 day from 00:00:00 to 23:59:59),
    - `week` (-7 day from 00:00:00 to the end of current day),
    - `month` (-30 day from 00:00:00 to the end of current day),
    - `year` (-365 day from 00:00:00 to the end of current day).

    :param start: start day in format defined by `userFormat` or keyword.
    :param end: end day in format defined by `userFormat`.
    :param userFormat: user-friendly date format, e.g. `"%Y-%m-%d"`.
    :param outputFormat: output string date format.

    :return: tuple with 2 strings `("start", "end")`. Example of return is `("2022-06-01T00:00:00Z", "2022-06-20T23:59:59Z")`.
             Second string is the end of the last day.
             Tuple ("", "") returned if errors occurred.
    """
    try:
        s = datetime.now(tzutc()).replace(hour=0, minute=0, second=0, microsecond=0)  # start of the current day
        e = s.replace(hour=23, minute=59, second=59, microsecond=0)  # end of the current day

        # time between start and the end of the current day:
        if start is None or start.lower() == "today":
            pass

        # from start of the last day to the end of the last day:
        elif start.lower() == "yesterday":
            s -= timedelta(days=1)
            e -= timedelta(days=1)

        # week (-7 day from 00:00:00 to the end of the current day):
        elif start.lower() == "week":
            s -= timedelta(days=6)  # +1 current day already taken into account

        # month (-30 day from 00:00:00 to the end of current day):
        elif start.lower() == "month":
            s -= timedelta(days=29)  # +1 current day already taken into account

        # year (-365 day from 00:00:00 to the end of current day):
        elif start.lower() == "year":
            s -= timedelta(days=364)  # +1 current day already taken into account

        # -N days ago to the end of current day:
        elif start.startswith('-') and start[1:].isdigit():
            s -= timedelta(days=abs(int(start)) - 1)  # +1 current day already taken into account

        # dates between start day at 00:00:00 and the end of the last day at 23:59:59:
        else:
            s = datetime.strptime(start, userFormat).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc())
            e = datetime.strptime(end, userFormat).replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=tzutc()) if end is not None else e

        # converting to UTC ISO time formatted with Z suffix for Tinkoff Open API:
        s = s.strftime(outputFormat)
        e = e.strftime(outputFormat)

        return s, e

    except Exception:
        return "", ""


def NanoToFloat(units: str, nano: int) -> float:
    """
    Convert number in nano-view mode with string parameter `units` and integer parameter `nano` to float view.

    Examples:
    - `NanoToFloat(units="2", nano=500000000) -> 2.5`
    - `NanoToFloat(units="0", nano=50000000) -> 0.05`

    :param units: integer string or integer parameter that represents the integer part of number
    :param nano: integer string or integer parameter that represents the fractional part of number

    :return: float view of number. If an error occurred, then returns `0.`.
    """
    try:
        return int(units) + int(nano) * NANO

    except Exception:
        return 0.


def FloatToNano(number: float) -> dict[str, int]:
    """
    Convert float number to nano-type view: dictionary with string `units` and integer `nano` parameters `{"units": "string", "nano": integer}`.

    Examples:
    - `FloatToNano(number=2.5) -> {"units": "2", "nano": 500000000}`
    - `FloatToNano(number=0.05) -> {"units": "0", "nano": 50000000}`

    :param number: float number.

    :return: nano-type view of number: `{"units": "string", "nano": integer}`.
             If an error occurred, then returns `{"units": "0", "nano": 0}`.
    """
    try:
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

    except Exception:
        return {"units": "0", "nano": 0}


def UpdateClassFields(instance: object, params: dict) -> None:
    """
    This method get config as dictionary (preloaded from YAML file) and apply `key: value` as names of class fields and
    values of class fields. Example for class `TradeScenario`:
    `config["tickers"] = ["TICKER1", "TICKER2"] ==> TradeScenario(TinkoffBrokerServer).tickers = ["TICKER1", "TICKER2"]`.

    :param instance: instance of class to parametrize.
    :param params: dict with all parameters in `key: value` format. It will be nothing with object if an error occurred.
    """
    try:
        for name in params:
            instance.__setattr__(name, params[name])

    except Exception:
        pass


def SeparateByEqualParts(elements: list[Any], parts: int = 2, union: bool = True) -> list[list[Any]]:
    """
    Gets input list and try to separate it by equal parts of elements.

    Examples:
    - `SeparateByEqualParts([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], parts=2) -> [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]`
    - `SeparateByEqualParts([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], parts=2, union=True) -> [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10]]`
    - `SeparateByEqualParts([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], parts=2, union=False) -> [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10]]]`
    - `SeparateByEqualParts([1, 2, 3], parts=2, union=True) -> [[1], [2, 3]]`
    - `SeparateByEqualParts([1, 2, 3], parts=2, union=False) -> [[1], [2], [3]]`

    If parts > length of elements:
    - `SeparateByEqualParts([1], parts=2, union=True) -> [[1]]`
    - `SeparateByEqualParts([1, 2, 3], parts=4, union=True) -> [[1], [2], [3]]`
    - `SeparateByEqualParts([1], parts=2, union=False) -> [[1], []]`
    - `SeparateByEqualParts([1, 2, 3], parts=4, union=False) -> [[1], [2], [3], []]`

    :param elements: list of objects.
    :param parts: int, numbers of equal parts of objects.
    :param union: bool, if True and if the remainder of the separating not empty, then remainder part union with the last part.

    :return: list of lists with equal parts of objects. If an error occurred, then returns empty list `[]`.
    """
    try:
        result = []
        if elements is not None and isinstance(elements, list) and elements and isinstance(parts, int) and isinstance(union, bool):
            count = len(elements)

            if parts == 1:
                result = [elements]

            elif parts > count:
                result = [[item] for item in elements]

                if not union:
                    result.extend([[] for _ in range(parts - count)])

            else:
                partsLen = count // parts
                for part in range(parts):
                    result.append(elements[part * partsLen: (part + 1) * partsLen])

                index = parts * partsLen
                if index < count:
                    if union:
                        result[-1].extend(elements[index:])

                    else:
                        result.append(elements[index:])

        return result

    except Exception:
        return []


def CalculateLotsForDeal(currentPrice: float, maxCost: float, volumeInLot: int = 1) -> int:
    """
    Calculates maximum lots for deal depends on current price and volume of instrument in one lot.

    Formula: `lots = maxCost // (currentPrice * volumeInLot)`, it means max count of lots, for which will be:
    `cost = lots * currentPrice * volumeInLot <= maxCost`.

    If `costOneLot = currentPrice * volumeInLot > maxCost`, then returned `lots = 1`.

    If an error occurred then returned `lots = 0`.

    :param currentPrice: the current price of instrument, >= 0.
    :param maxCost: the maximum cost of all lots of instrument in portfolio, >= 0.
    :param volumeInLot: volumes of instrument in one lot, >= 1.

    :return: integer number of lots, >= 0.
    """
    try:
        costOneLot = abs(currentPrice * volumeInLot)
        lots = abs(int(maxCost // costOneLot)) if costOneLot <= abs(maxCost) else 1

    except Exception:
        lots = 0

    return lots


def HampelFilter(series: Union[list, pd.Series], window: int = 5, sigma: float = 3, scaleFactor: float = 1.4826) -> pd.Series:
    """
    Outlier Detection with Hampel Filter. It can detect outliers based on a sliding window and counting difference
    between median values and input values of series. The Hampel filter is often considered extremely effective in practice.

    For each window, we calculate the Median and the Median Absolute Deviation (MAD). If the considered observation
    differs from the window median by more than sigma standard deviations multiple on scaleFactor, then we treat it
    as an outlier.

    Let Xi — elements of input series in the i-th window,
    s — sigma, the number of standard deviations,
    k — scale factor, depend on distribution (≈1.4826 for normal).

    How to calculate rolling MAD: `MAD(Xi) = Median(|x1 − Median (Xi)|, ..., |xn − Median(Xi)|)`

    What is an anomaly: `A = {a | |a − Median (Xi)| > s ∙ k ∙ MAD(Xi)}`

    References:

    1. Gilmullin T.M., Gilmullin M.F. How to quickly find anomalies in number series using the Hampel method:
       - Link (RU): https://teletype.in/@tgilmullin/anomaly
       - Link (EN): https://forworktests.blogspot.com/2023/01/how-to-quickly-find-anomalies-in-number.html
    2. Lewinson Eryk. Outlier Detection with Hampel Filter. September 26, 2019.
       - Link: https://towardsdatascience.com/outlier-detection-with-hampel-filter-85ddf523c73d
    3. Hancong Liu, Sirish Shah and Wei Jiang. On-line outlier detection and data cleaning. Computers and Chemical Engineering. Vol. 28, March 2004, pp. 1635–1647.
       - Link: https://sites.ualberta.ca/~slshah/files/on_line_outlier_det.pdf
    4. Hampel F. R. The influence curve and its role in robust estimation. Journal of the American Statistical Association, 69, 382–393, 1974.

    Examples:

    - `HampelFilter([1, 1, 1, 1, 1, 1], window=3) -> pd.Series([False, False, False, False, False, False])`
    - `HampelFilter([1, 1, 1, 2, 1, 1], window=3) -> pd.Series([False, False, False, True, False, False])`
    - `HampelFilter([0, 1, 1, 1, 1, 0], window=3) -> pd.Series([True, False, False, False, False, True])`
    - `HampelFilter([1], window=3) -> pd.Series([False])`
    - `HampelFilter([5, 5, 50, 5, 5], window=2) -> pd.Series([False, False, True, False, False])`
    - `HampelFilter([100, 1, 1, 1, 1, 100], window=2) -> pd.Series([True, False, False, False, False, True])`
    - `HampelFilter([1, 1, 10, 1, 10, 1, 1], window=2) -> pd.Series([False, False, True, False, True, False, False])`


    :param series: Pandas Series object with numbers in which we identify outliers.
    :param window: length of the sliding window (5 points by default), 1 <= window <= len(series).
    :param sigma: sigma is the number of standard deviations which identify the outlier (3 sigma by default), > 0.
    :param scaleFactor: constant scale factor (1.4826 by default for Gaussian distribution), > 0.

    :return: Pandas Series object with True/False values.
             `True` means that an outlier detected in that position of input series.
             If an error occurred, then empty series returned.
    """
    try:
        if isinstance(series, list):
            series = pd.Series(series)

        if window < 1:
            window = 1

        if window > len(series):
            window = len(series)

        if sigma <= 0:
            sigma = 3

        if scaleFactor <= 0:
            scaleFactor = 1.4826

        # Minimal non-zero MAD value to allow robust comparison. Slightly above float64 machine epsilon, robust for anomaly detection:
        epsilon = 1e-15

        # Special case: if `2 * window` exceeds series length, process all points manually:
        if 2 * window > len(series):
            new = pd.Series(False, index=series.index)

            for i in range(len(series)):
                start = max(0, i - window)
                end = min(len(series), i + window + 1)
                local = series.iloc[start:end]

                if len(local) >= 1 and not local.isna().all():
                    med = np.median(local)
                    mad = np.median(np.abs(local - med))
                    diff = abs(series.iloc[i] - med)

                    if not np.isfinite(mad) or mad < epsilon:
                        if diff > 0:
                            new.iloc[i] = True

                    else:
                        limit = sigma * scaleFactor * mad

                        if diff > limit:
                            new.iloc[i] = True

            return new

        # Step 1: Calculate rolling median and point-wise absolute deviation from it:
        rollingMedian = series.rolling(window=2 * window, center=True).median()
        delta = (series - rollingMedian).abs()

        # Step 2: Calculate rolling MAD (reusing delta for efficiency):
        rollingMAD = delta.rolling(window=2 * window, center=True).median()

        # Step 3: Detect anomalies for valid central values:
        new = pd.Series(False, index=series.index)
        threshold = sigma * scaleFactor * rollingMAD
        mask = rollingMAD.notna()
        new.loc[mask] = (delta[mask] > threshold[mask])

        # Step 4: Handle boundary values manually (first and last `window` points):
        for i in list(range(window)) + list(range(len(series) - window, len(series))):
            start = max(0, i - window)
            end = min(len(series), i + window + 1)
            local = series.iloc[start:end]

            if len(local) >= 1 and not local.isna().all():
                med = np.median(local)
                mad = np.median(np.abs(local - med))
                diff = abs(series.iloc[i] - med)

                if not np.isfinite(mad) or mad < epsilon:
                    if diff > 0:
                        new.iloc[i] = True

                else:
                    limit = sigma * scaleFactor * mad

                    if diff > limit:
                        new.iloc[i] = True

    except Exception:
        new = pd.Series()

    return new


def HampelAnomalyDetection(
    series: Union[list, pd.Series],
    compareWithMax: bool = True,
    **kwargs
) -> Optional[int]:
    """
    Anomaly Detection function using Hampel Filter. This function returns the minimum index of elements in an anomaly list
    or index of the first maximum element in the input series if this index is less than anomaly element index.
    If the series has no anomalies, then `None` will be returned.

    Anomaly filter is a function:
    F: X → {True, False}. F(xi) = True, if xi ∈ A; False, if xi ∉ A, where X — input series with xi elements, A — anomaly set.

    References:

    1. Gilmullin T.M., Gilmullin M.F. How to quickly find anomalies in number series using the Hampel method. December 27, 2022.
       - Link (RU): https://teletype.in/@tgilmullin/anomaly
       - Link (EN): https://forworktests.blogspot.com/2023/01/how-to-quickly-find-anomalies-in-number.html
    2. Jupyter Notebook with examples:
       - Link (EN): https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample_EN.ipynb
       - Link (RU): https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample.ipynb
    3. Simple Python script demonstrates how to use Hampel Filter to determine anomalies in time series:
       - Link: https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/TestAnomalyFilter.py

    Examples:

    - `HampelAnomalyDetection([1, 1, 1, 1, 1, 1]) -> None`
    - `HampelAnomalyDetection([1, 1, 1, 1, 111, 1]) -> 4`
    - `HampelAnomalyDetection([1, 1, 10, 1, 1, 1]) -> 2`
    - `HampelAnomalyDetection([111, 1, 1, 1, 1, 1]) -> 0`
    - `HampelAnomalyDetection([111, 1, 1, 1, 1, 111]) -> 0`
    - `HampelAnomalyDetection([1, 11, 1, 111, 1, 1]) -> 1`
    - `HampelAnomalyDetection([1, 1, 1, 111, 99, 11]) -> 3`
    - `HampelAnomalyDetection([1, 1, 11, 111, 1, 1, 1, 11111]) -> 2`
    - `HampelAnomalyDetection([1, 1, 1, 111, 111, 1, 1, 1, 1]) -> 3`
    - `HampelAnomalyDetection([1, 1, 1, 1, 111, 1, 1, 11111, 5555]) -> 4`
    - `HampelAnomalyDetection([9, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 13, 12, 12, 1, 1]) -> 0`
    - `HampelAnomalyDetection([9, 13, 12, 12, 13, 12, 1000, 13, 12, 12, 300000, 12, 12, 13, 12, 2000, 1, 1, 1, 1]) -> 0`

    Some **kwargs parameters you can pass to `HampelFilter()`:

    - `window` is the length of the sliding window (5 points by default), 1 <= window <= len(series).
    - `sigma` is the number of standard deviations which identify the outlier (3 sigma by default), > 0.
    - `scaleFactor` is the constant scale factor (1.4826 by default), > 0.

    :param series: List or Pandas Series of numeric values to check for anomalies.
    :param compareWithMax: If `True` (default), returns min(index of anomaly, index of first maximum).
                           If `False`, returns only the first anomaly index detected by `HampelFilter`.
    :param kwargs: Additional parameters are forwarded to `HampelFilter()`.

    :return: Index of the first anomaly (or intersection with maximum, if enabled). Returns `None` if no anomaly is found.
    """
    try:
        # Convert a list to Pandas Series for consistency:
        if isinstance(series, list):
            series = pd.Series(series)

        # Apply Hampel filter to get a mask of anomalies (True means anomaly):
        filtered = HampelFilter(series=series, **kwargs)
        anomalyIndexes = filtered[filtered].index  # Get indices where an anomaly is detected.

        # Get an index of the first anomaly, if any:
        indexAnomalyMin = next(iter(anomalyIndexes), None)

        # If compareWithMax is True — return the minimum between anomaly index and maximum index:
        if compareWithMax:
            if indexAnomalyMin is not None:
                indexFirstMax = int(series.values.argmax())  # Index of the first maximum value.

                return min(indexAnomalyMin, indexFirstMax)

            else:
                return None  # No anomaly found.

        else:
            return indexAnomalyMin  # If compareWithMax is False — return only the anomaly index.

    except Exception:
        return None  # Fallback in case of error.


def CalculateAdaptiveCacheReserve(
    drawdowns: list[float],
    curDrawdown: float,
    reserve: float,
    portfolioValue: float,
    amplificationFactor: float = 1.25,
    amplificationSensitivity: float = 0.1,
) -> float:
    """
    Calculates the adaptive target cash reserve based on current and historical portfolio drawdowns.

    This function dynamically adjusts the reserve allocated for averaging positions (e.g., during drawdowns).
    If the drawdown increases for several consecutive iterations, the reserve is amplified exponentially.
    If the drawdown stabilizes or decreases, the reserve is reset to the base level.

    The amplification is computed as:
        amplification = amplificationFactor × exp(growStreak × amplificationSensitivity)

    Where:
    - `growStreak` is the number of consecutive days the drawdown has been increasing, including the current day.
    - `amplificationFactor` is the base multiplier.
    - `amplificationSensitivity` controls how aggressively the amplification grows with each additional drawdown increase.

    Example:

    With amplificationFactor = 1.25 and amplificationSensitivity = 0.1, if the drawdown increases for 3 days:
        amplification = 1.25 × exp(0.3) ≈ 1.25 × 1.3499 ≈ 1.687

    :param drawdowns: historical portfolio drawdowns (fractions between 0 and 1);
                      drawdowns[0] is the oldest, drawdowns[-1] is the most recent.
    :param curDrawdown: current portfolio drawdown at the time of calculation.
    :param reserve: base reserve ratio (e.g., 0.05 means 5% of the portfolio value).
    :param portfolioValue: current portfolio value (in currency units).
    :param amplificationFactor: base multiplier for reserve amplification (default is 1.25).
    :param amplificationSensitivity: exponential growth rate of amplification per growStreak step (default is 0.1).

    :return: calculated target cash reserve in portfolio currency units.
    """
    # Check the type and validity of drawdowns:
    if not isinstance(drawdowns, list):
        raise ValueError("drawdowns must be a list or iterable of floats!")

    if any(not isinstance(d, (float, int)) or d is None for d in drawdowns):
        raise ValueError("drawdowns contains invalid data!")

    # Check the type and validity of curDrawdown:
    if not isinstance(curDrawdown, (float, int)):
        raise ValueError("curDrawdown must be a float or int!")

    # Check the type and validity of the reserve:
    if not isinstance(reserve, (float, int)) or reserve < 0:
        raise ValueError("reserve must be a positive float or int value!")

    # Check the type and validity of portfolioValue:
    if not isinstance(portfolioValue, (float, int)) or portfolioValue < 0:
        raise ValueError("portfolioValue must be a positive float or int value!")

    # Check the type and validity of the amplificationFactor:
    if not isinstance(amplificationFactor, (float, int)) or amplificationFactor <= 0:
        raise ValueError("amplificationFactor must be a positive float or int value!")

    # Check the type and validity of amplificationSensitivity:
    if not isinstance(amplificationSensitivity, (float, int)) or amplificationSensitivity < 0:
        raise ValueError("amplificationSensitivity must be a positive float or int value!")

    # --- Main function logic:
    if not drawdowns or all(d == 0.0 for d in drawdowns):
        return portfolioValue * reserve

    if curDrawdown <= drawdowns[-1]:
        return portfolioValue * reserve

    # Count how many consecutive iterations the drawdown has been increasing (including the current iteration):
    fullSequence = drawdowns + [curDrawdown]
    growStreak = 0

    for i in range(len(fullSequence) - 1, 0, -1):
        if fullSequence[i] > fullSequence[i - 1]:
            growStreak += 1

        else:
            break

    amplification = amplificationFactor * math.exp(growStreak * amplificationSensitivity)  # Current amplification factor.

    targetReserve = portfolioValue * reserve * amplification  # Count the reserve in portfolio currency units.

    return targetReserve


def HampelCleaner(
    series: pd.Series,
    window: int = 5,
    sigma: float = 3,
    scaleFactor: float = 1.4826,
    strategy: str = "neighborAvg",
    fallbackValue: float = 0.0,
    medianWindow: int = 3
) -> pd.Series:
    """
    Replaces outliers in a time series using the Hampel filter and a selected replacement strategy.

    This function detects anomalies using the Hampel method and replaces them according to the specified strategy.
    It is designed for use in financial time series, sensor data, or any numerical sequences requiring robust cleaning
    before further analysis (e.g., volatility estimation, trend modeling, probability forecasting).

    Available replacement strategies:

    - "neighborAvg": average of adjacent neighbors (default).
      Best for stable, low-noise time series where local continuity matters.

    - "prev": previous non-outlier value.
      Suitable for cumulative or trend-sensitive series, avoids abrupt distortions.

    - "const": fixed fallback value.
      Recommended when anomalies reflect technical failures (e.g., spikes due to API glitches).

    - "medianWindow": local window median (uses medianWindow size).
      Robust to single-point noise and short bursts of volatility; good for candle data.

    - "rollingMean": centered rolling mean over the window (same as a Hampel window).
      Applies smooth correction while preserving a general shape; works well for low-volatility assets.

    :param series: input time series as a Pandas Series of floats.
    :param window: sliding window size used in Hampel filtering (`5` by default).
    :param sigma: threshold multiplier for anomaly detection (`3` by default).
    :param scaleFactor: scaling factor for the MAD (`1.4826` by default, optimal for Gaussian data).
    :param strategy: strategy used to replace detected outliers (see the list above).
    :param fallbackValue: constantly used as a fallback in "const" strategy or when neighbors are missing.
    :param medianWindow: window size used for the "medianWindow" strategy.

    :return: cleaned time series as a Pandas Series with outliers replaced.
    """
    allowedStrategies = {"neighborAvg", "prev", "const", "medianWindow", "rollingMean"}

    if strategy not in allowedStrategies:
        raise ValueError(f"Unknown strategy '{strategy}'. Available options: {allowedStrategies}")

    # Step 1: Detect outliers using the Hampel filter:
    outlierMask = HampelFilter(series, window, sigma, scaleFactor)

    if not outlierMask.any():
        return series.copy()  # No anomalies detected — return untouched copy.

    # Step 2: Convert series and mask to NumPy arrays for faster access:
    seriesValues = series.to_numpy(copy=True)
    outlierMaskArray = outlierMask.to_numpy()
    n = len(seriesValues)
    result = seriesValues.copy()

    # Helper to compute window boundaries for rolling strategies:
    def GetBounds(pos, w):
        return max(0, pos - w), min(n, pos + w + 1)

    # Step 3: Process each outlier individually:
    outlierIndices = np.where(outlierMaskArray)[0]

    for i in outlierIndices:
        replacement = fallbackValue  # Default fallback.

        # Local neighbors for use in neighborAvg strategy:
        left = seriesValues[i - 1] if i - 1 >= 0 else None
        right = seriesValues[i + 1] if i + 1 < n else None

        if strategy == "neighborAvg":
            # Average of adjacent neighbors (if available):
            if left is not None and right is not None:
                replacement = (left + right) / 2.0

            elif left is not None:
                replacement = left

            elif right is not None:
                replacement = right

        elif strategy == "prev":
            # Walk back until non-outlier found:
            for j in range(i - 1, -1, -1):
                if not outlierMaskArray[j]:
                    replacement = seriesValues[j]

                    break

        elif strategy == "const":
            # Constant fallback (already assigned):
            replacement = fallbackValue

        elif strategy == "medianWindow":
            # Local median in a window (excluding outlier itself):
            start, end = GetBounds(i, medianWindow)
            values = np.delete(seriesValues[start:end], np.where(np.arange(start, end) == i))

            if len(values) > 0:
                replacement = np.median(values)

        elif strategy == "rollingMean":
            # Local mean in the rolling window (excluding outlier itself):
            start, end = GetBounds(i, window)
            values = np.delete(seriesValues[start:end], np.where(np.arange(start, end) == i))

            if len(values) > 0:
                replacement = np.mean(values)

        result[i] = replacement  # Replace outlier value.

    # Step 4: Return the cleaned Pandas series with the original index:
    return pd.Series(result, index=series.index)


def LogReturns(series: pd.Series) -> pd.Series:
    """
    Calculates logarithmic returns for a time series of prices.

    :param series: A series of close prices.

    :return: A series of log returns.
    """
    return np.log(series / series.shift(1)).dropna()


def MeanReturn(logReturns: pd.Series) -> float:
    """
    Computes the mean return from a log-return series.

    :param logReturns: A series of log returns.

    :return: The average return.
    """
    return logReturns.mean()


def Volatility(logReturns: pd.Series, ddof: int = 1) -> float:
    """
    Computes the sample standard deviation of log returns using specified Bessel correction.

    :param logReturns: A series of log returns.
    :param ddof: Degrees of freedom for Bessel's correction (1 by default, use 2 per methodology).

    :return: Volatility (standard deviation).
    """
    return logReturns.std(ddof=ddof)


def ZScore(logTargetRatio: float, meanReturn: float, volatility: float, horizon: int) -> float:
    """
    Computes the standardized deviation (z-score) using geometric Brownian motion with drift and volatility.

    :param logTargetRatio: Logarithm of (targetPrice / currentPrice).
    :param meanReturn: Estimated mean of log returns (μ).
    :param volatility: Estimated volatility of log returns (σ).
    :param horizon: Forecast horizon (number of candles).

    :return: z-score value (float).
    """
    effectiveDrift = meanReturn - 0.5 * (volatility ** 2)

    return (logTargetRatio - effectiveDrift * horizon) / (volatility * math.sqrt(horizon))


def BayesianAggregation(p1: float, p2: float) -> float:
    """
    Combines two conditional probabilities using Bayesian aggregation.

    :param p1: First probability.
    :param p2: Second probability.

    :return: Aggregated probability using Bayesian fusion.
    """
    numerator = p1 * p2
    denominator = numerator + (1 - p1) * (1 - p2)

    return numerator / denominator if denominator != 0 else 0.0


def VolatilityWeight(sigmaLow: float, sigmaHigh: float) -> float:
    """
    Computes a dynamic weight coefficient based on relative volatility of two timeframes.

    :param sigmaLow: Volatility from the lower timeframe (faster/shorter interval).
    :param sigmaHigh: Volatility from the higher timeframe (slower/longer interval).

    :return: Weight alpha in the range [0.0, 1.0], prioritizing a higher timeframe when its volatility is higher.
    """
    return sigmaHigh / (sigmaHigh + sigmaLow)


def EstimateTargetReachability(
    seriesLowTF: Union[list, pd.Series],
    seriesHighTF: Union[list, pd.Series],
    currentPrice: float,
    targetPrice: float,
    horizonLowTF: int,
    horizonHighTF: int,
    ddof: int = 2,
    cleanWithHampel: bool = False,
    **kwargs
) -> tuple[float, str]:
    """
    Estimates the probability of reaching a target price using two price series from different timeframes.
    Implements full methodology: log returns, volatility with Bessel correction, effective drift, z-score,
    cumulative probability, Bayesian aggregation, volatility-based weighting, and fuzzy classification.

    References:

    1. (RU article) https://teletype.in/@tgilmullin/target-probability
       Will the Price Hit the Target: Assessing Probability Instead of Guessing.

    2. (RU article on which the formulas are based)
       Statistical Estimation of the Probability of Reaching a Target Price Considering Volatility and Returns Across Different Timeframes.

    :param seriesLowTF: A close-price series from the lower timeframe.
    :param seriesHighTF: A close-price series from the higher timeframe.
    :param currentPrice: The current price of the asset.
    :param targetPrice: The target price to be reached or exceeded.
    :param horizonLowTF: The forecast horizon in candles for the lower timeframe.
    :param horizonHighTF: The forecast horizon in candles for the higher timeframe.
    :param ddof: Degrees of freedom for volatility estimation (use 2 as per article).
    :param cleanWithHampel: If `True`, applies outlier cleaning to both input series before computing log returns
                            using `HampelCleaner()` (`False` by default). Recommended for real market data where spikes,
                            anomalies, or gaps may distort volatility and probability estimates.
    :param kwargs: Optional keyword arguments are forwarded to `HampelCleaner()` if `cleanWithHampel` is `True`.

        Supported options (with default values):

        - `window` (5): Sliding window size for `HampelCleaner()`.
        - `sigma` (3): Threshold multiplier for anomaly detection.
        - `scaleFactor` (`1.4826`): Scaling factor for MAD.
        - `strategy` ("neighborAvg"): Outlier replacement strategy:
            • `"neighborAvg"` – average of adjacent neighbors. Good for a smooth, low-noise series.
            • `"prev"` – previous valid value. Preserves a trend direction.
            • `"const"` – constant fallback. Use for API glitches or corrupted data.
            • `"medianWindow"` – local median window. **Best default for real-world candles.**
            • `"rollingMean"` – centered mean smoothing for low-volatility series.
        - `fallbackValue` (`0.0`): Constant value for use in `"const"` strategy or edge cases.
        - `medianWindow` (`3`): Window size for `"medianWindow"` strategy.

    :return: A tuple `(pIntegral, fIntegral)`, where:
        - `pIntegral` is a float in range `[0.0, 1.0]` — estimated probability of reaching the target.
        - `fIntegral` is a fuzzy label: one of `["Min", "Low", "Med", "High", "Max"]`.
    """
    try:
        # Convert lists to Pandas Series if needed:
        if isinstance(seriesLowTF, list):
            seriesLowTF = pd.Series(seriesLowTF)

        if isinstance(seriesHighTF, list):
            seriesHighTF = pd.Series(seriesHighTF)

        # Validate input ranges:
        if (
            len(seriesLowTF) < 2 or len(seriesHighTF) < 2 or
            horizonLowTF <= 0 or horizonHighTF <= 0 or
            currentPrice <= 0 or targetPrice <= 0
        ):
            return 0.0, FUZZY_LEVELS[0]  # (0, "Min")

        # Optional Hampel-based outlier cleaning before log-return computation:
        if cleanWithHampel:
            seriesLowTF = HampelCleaner(seriesLowTF, **kwargs)
            seriesHighTF = HampelCleaner(seriesHighTF, **kwargs)

        # --- Formulas (2)–(3): Compute log returns and mean returns:
        rLow = LogReturns(seriesLowTF)
        rHigh = LogReturns(seriesHighTF)

        muL = MeanReturn(rLow)
        muH = MeanReturn(rHigh)

        # --- Formula (4): Compute volatility with Bessel correction (ddof):
        sigmaL = Volatility(rLow, ddof)
        sigmaH = Volatility(rHigh, ddof)

        # Validate computed statistics:
        if not all(map(np.isfinite, [muL, sigmaL, muH, sigmaH])) or sigmaL == 0 or sigmaH == 0:
            return 0.0, FUZZY_LEVELS[0]  # (0, "Min")

        # --- Formula (5): Log target ratio between target and current price:
        logTarget = math.log(targetPrice / currentPrice)

        # --- Formula (6): Compute z-scores using drift and volatility:
        zL = ZScore(logTarget, muL, sigmaL, horizonLowTF)
        zH = ZScore(logTarget, muH, sigmaH, horizonHighTF)

        # --- Formula (8): Compute cumulative probabilities:
        pL = 1 - norm.cdf(zL)
        pH = 1 - norm.cdf(zH)

        # --- Formula (9): Arithmetic mean of the two probabilities:
        pAverage = (pL + pH) / 2

        # --- Formula (10): Bayesian aggregation:
        pBayes = BayesianAggregation(pL, pH)

        # --- Formula (11): Compute alpha weight from volatilities:
        alpha = VolatilityWeight(sigmaL, sigmaH)

        # --- Formula (12): Final integrated probability:
        pIntegral = alpha * pBayes + (1 - alpha) * pAverage

        # --- Formula (15): Fuzzy classification of the final probability:
        fIntegral = FUZZY_SCALE.Fuzzy(pIntegral).name

        return pIntegral, fIntegral

    except Exception:
        return 0.0, FUZZY_LEVELS[0]  # (0, "Min")


@jit(nopython=True)
def RollingMean(array: np.ndarray, window: int) -> np.ndarray:
    """
    Calculates a simple moving average (SMA) using a sliding window over a NumPy array with running sum optimization.

    :param array: A NumPy array of input data (e.g., closing prices).
    :param window: The size of the rolling window for calculating the average. Must be a positive integer.

    :return: A NumPy array containing the rolling mean values, with NaNs for positions before the first full window.
    """
    result = np.full(array.shape, np.nan)  # Initialize the result array with NaNs.

    if array.size < window:
        return result  # Not enough data to form the first window.

    runningSum = np.sum(array[:window - 1])  # Calculate an initial sum for the first window (excluding the last element).

    for i in range(window - 1, array.size):
        runningSum += array[i]  # Add the new element entering the window.
        result[i] = runningSum / window  # Calculate the mean and assign it to the result array.
        runningSum -= array[i - window + 1]  # Subtract the oldest element exiting the window.

    return result


@jit(nopython=True)
def RollingStd(array: np.ndarray, window: int, ddof: int = 1) -> np.ndarray:
    """
    Calculates a rolling standard deviation over a NumPy array using a sliding window.

    :param array: A NumPy array of input data (e.g., closing prices).
    :param window: The size of the rolling window for calculating standard deviation.
    :param ddof: Delta degrees of freedom. Default is `1`.

    :return: A NumPy array containing the rolling standard deviation values.
    """
    result = np.full(array.shape, np.nan)  # Initialize the result array with NaNs.

    ddof = int(ddof)  # Ensure ddof is integer.

    for i in range(window - 1, array.size):
        slice_ = array[i - window + 1:i + 1]  # Extract the current sliding window.
        mean_ = np.mean(slice_)  # Calculate the mean of the window.
        diff = slice_ - mean_  # Calculate differences from the mean.
        squaredDiffs = diff ** 2  # Square the differences.

        sumSquared = np.sum(squaredDiffs)  # Sum of squared differences.
        divisor = window - ddof  # Degrees of freedom correction.

        variance = sumSquared / divisor  # type: ignore

        result[i] = np.sqrt(variance)  # Standard deviation is the square root of variance.

    return result


def FastBBands(
    close: Union[pd.Series, np.ndarray],
    length: int = 5,
    std: float = 2.0,
    ddof: int = 0,
    offset: int = 0,
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Calculates Bollinger Bands (BBANDS) using a fast NumPy-based implementation.

    :param close: Series or array of closing prices.
    :param length: Rolling window size for the moving average and standard deviation. The default is `5`.
    :param std: Number of standard deviations to determine the width of the bands. The default is `2.0`.
    :param ddof: Delta degrees of freedom for standard deviation calculation. Default is `0`.
    :param offset: How many periods to offset the resulting bands. The default is `0`.
    :param kwargs: Optional keyword arguments are forwarded for filling missing values.

        Supported options (with default values):

        - `fillna` (`None`): Value to fill missing data points (NaN values).
        - `fill_method` (`None`): Method to fill missing data points (e.g., `ffill`, `bfill`).

    :return: A pandas DataFrame containing the following columns:
        - `lower`: Lower Bollinger Band.
        - `mid`: Middle band (simple moving average).
        - `upper`: Upper Bollinger Band.
        - `bandwidth`: Percentage bandwidth between upper and lower bands.
        - `percent`: Position of the close price within the bands (from `0` to `1`).
        Returns `None` if the input is invalid.
    """
    # Input validation:
    if close is None or not isinstance(close, (pd.Series, np.ndarray)):
        return None

    closeArray = close.values if isinstance(close, pd.Series) else close

    lengthParam = int(length) if length and length > 0 else 5
    stdParam = float(std) if std and std > 0 else 2.0
    ddofParam = int(ddof) if 0 <= ddof < lengthParam else 1
    offsetParam = int(offset) if offset else 0

    # Calculate moving average and standard deviation:
    mid = RollingMean(closeArray, lengthParam)
    stdev = RollingStd(closeArray, lengthParam, ddof=ddofParam)
    deviations = stdParam * stdev

    # Calculate upper and lower bands:
    upper = mid + deviations
    lower = mid - deviations

    # Calculate bandwidth and percent:
    ulr = np.where((upper - lower) == 0, np.nan, upper - lower)
    bandwidth = 100 * ulr / mid
    percent = np.where(ulr == 0, np.nan, (closeArray - lower) / ulr)

    # Offset results if needed:
    if offsetParam != 0:
        lower = np.roll(lower, offsetParam)
        mid = np.roll(mid, offsetParam)
        upper = np.roll(upper, offsetParam)
        bandwidth = np.roll(bandwidth, offsetParam)
        percent = np.roll(percent, offsetParam)

    # Convert results to Pandas Series:
    lowerSeries = pd.Series(lower, name=f"BBL_{lengthParam}_{stdParam}")
    midSeries = pd.Series(mid, name=f"BBM_{lengthParam}_{stdParam}")
    upperSeries = pd.Series(upper, name=f"BBU_{lengthParam}_{stdParam}")
    bandwidthSeries = pd.Series(bandwidth, name=f"BBB_{lengthParam}_{stdParam}")
    percentSeries = pd.Series(percent, name=f"BBP_{lengthParam}_{stdParam}")

    # Handle fills:
    if "fillna" in kwargs:
        for series in [lowerSeries, midSeries, upperSeries, bandwidthSeries, percentSeries]:
            series.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        for series in [lowerSeries, midSeries, upperSeries, bandwidthSeries, percentSeries]:
            series.fillna(method=kwargs["fill_method"], inplace=True)

    # Create a final DataFrame:
    dataFrame = pd.DataFrame({
        lowerSeries.name: lowerSeries,
        midSeries.name: midSeries,
        upperSeries.name: upperSeries,
        bandwidthSeries.name: bandwidthSeries,
        percentSeries.name: percentSeries,
    })

    dataFrame.name = f"BBANDS_{lengthParam}_{stdParam}"
    dataFrame.category = "volatility"

    return dataFrame


@jit(nopython=True)
def _FastPSARCore(highArray: np.ndarray, lowArray: np.ndarray, af0: float, maxAf: float) -> tuple:
    """
    Core calculation of Parabolic SAR (PSAR) using NumPy arrays.

    :param highArray: Numpy array of `high` prices.
    :param lowArray: Numpy array of `low` prices.
    :param af0: Initial Acceleration Factor.
    :param maxAf: Maximum Acceleration Factor.

    :return: Tuple of arrays `(long, short, af, reversal)`.
    """
    size = highArray.shape[0]

    longSar = np.full(size, np.nan)
    shortSar = np.full(size, np.nan)
    afArray = np.full(size, np.nan)
    reversalArray = np.zeros(size, dtype=np.int32)

    # Initialize the trend direction based on the first two candles:
    upMove = highArray[1] - highArray[0]
    downMove = lowArray[0] - lowArray[1]
    falling = downMove > upMove  # True if the initial trend is falling.

    # Initialize SAR and EP:
    if falling:
        sar = highArray[0]
        ep = lowArray[0]

    else:
        sar = lowArray[0]
        ep = highArray[0]

    af = af0
    afArray[0] = af0

    for i in range(1, size):
        high = highArray[i]
        low = lowArray[i]

        newSar = sar + af * (ep - sar)  # Calculate the new SAR.

        if falling:
            reverse = high > newSar

            if low < ep:
                ep = low
                af = min(af + af0, maxAf)

            newSar = max(max(float(highArray[i - 1]), float(highArray[i - 2])), newSar)

        else:
            reverse = low < newSar

            if high > ep:
                ep = high
                af = min(af + af0, maxAf)

            newSar = min(min(float(lowArray[i - 1]), float(lowArray[i - 2])), newSar)

        if reverse:
            newSar = ep
            af = af0
            falling = not falling
            ep = low if falling else high

        sar = newSar

        # Assign SAR value to long or short arrays:
        if falling:
            shortSar[i] = sar

        else:
            longSar[i] = sar

        afArray[i] = af
        reversalArray[i] = int(reverse)

    return longSar, shortSar, afArray, reversalArray


def FastPSAR(
    high: Union[pd.Series, np.ndarray],
    low: Union[pd.Series, np.ndarray],
    af0: float = 0.02,
    af: Optional[float] = None,
    maxAf: float = 0.2,
    offset: int = 0,
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Calculates the Parabolic SAR (PSAR) indicator using a fast NumPy-based implementation.

    :param high: Series or array of high prices.
    :param low: Series or array of low prices.
    :param af0: Initial Acceleration Factor. The default is `0.02`.
    :param af: Acceleration Factor (not used separately, defaults to `af0`). Default is `None`.
    :param maxAf: Maximum Acceleration Factor. The default is `0.2`.
    :param offset: How many periods to offset the resulting arrays. The default is `0`.
    :param kwargs: Optional keyword arguments are forwarded for filling missing values.

        Supported options (with default values):

        - `fillna` (`None`): Value to fill missing data points (NaN values).
        - `fill_method` (`None`): Method to fill missing values (e.g., `ffill`, `bfill`).

    :return: A pandas DataFrame containing the following columns:
        - `long`: SAR points for long trends (upward movement).
        - `short`: SAR points for short trends (downward movement).
        - `af`: Acceleration Factor values over time.
        - `reversal`: `1` if reversal detected on this candle, otherwise `0`.
        Returns `None` if input is invalid.
    """
    # Input validation:
    if high is None or low is None or not isinstance(high, (pd.Series, np.ndarray)) or not isinstance(low, (pd.Series, np.ndarray)):
        return None

    highArray = high.values if isinstance(high, pd.Series) else high
    lowArray = low.values if isinstance(low, pd.Series) else low

    if highArray.size != lowArray.size:
        return None

    afStart = af0 if af is None else af

    # Core calculation:
    longSar, shortSar, afArray, reversalArray = _FastPSARCore(highArray, lowArray, afStart, maxAf)

    # Offset results if needed:
    if offset != 0:
        longSar = np.roll(longSar, offset)
        shortSar = np.roll(shortSar, offset)
        afArray = np.roll(afArray, offset)
        reversalArray = np.roll(reversalArray, offset)

    # Convert to Pandas Series:
    longSeries = pd.Series(longSar, name="long")
    shortSeries = pd.Series(shortSar, name="short")
    afSeries = pd.Series(afArray, name="af")
    reversalSeries = pd.Series(reversalArray, name="reversal")

    # Handle fills:
    if "fillna" in kwargs:
        for series in [longSeries, shortSeries, afSeries, reversalSeries]:
            series.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        for series in [longSeries, shortSeries, afSeries, reversalSeries]:
            series.fillna(method=kwargs["fill_method"], inplace=True)

    # Create the final DataFrame
    dataFrame = pd.DataFrame({
        "long": longSeries,
        "short": shortSeries,
        "af": afSeries,
        "reversal": reversalSeries,
    })

    dataFrame.name = "PSAR"
    dataFrame.category = "trend"

    return dataFrame
