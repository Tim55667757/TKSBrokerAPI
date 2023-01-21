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
import pandas as pd
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

    For each window we calculate the Median and the Median Absolute Deviation (MAD). If the considered observation
    differs from the window median by more than sigma standard deviations multiple on scaleFactor, then we treat it
    as an outlier.

    Let Xi — elements of input series in i-th window,
    s — sigma, the number of standard deviations,
    k — scale factor, depends on distribution (≈1.4826 for normal).

    How to calculate rolling MAD: `MAD(Xi) = Median(|x1 − Median (Xi)|, ..., |xn − Median(Xi)|)`

    What is an anomaly: `A = {a | |a − Median (Xi)| > s ∙ k ∙ MAD(Xi)}`

    References:

    1. Gilmullin T.M., Gilmullin M.F. How to quickly find anomalies in number series using the Hampel method. December 27, 2022.
       - Link (EN): https://forworktests.blogspot.com/2023/01/how-to-quickly-find-anomalies-in-number.html
       - Link (RU): https://forworktests.blogspot.com/2022/12/blog-post.html
    2. Lewinson Eryk. Outlier Detection with Hampel Filter. September 26, 2019.
       - Link: https://towardsdatascience.com/outlier-detection-with-hampel-filter-85ddf523c73d
    3. Hancong Liu, Sirish Shah and Wei Jiang. On-line outlier detection and data cleaning. Computers and Chemical Engineering. Vol. 28, March 2004, pp. 1635–1647.
       - Link: https://sites.ualberta.ca/~slshah/files/on_line_outlier_det.pdf
    4. Hampel F. R. The influence curve and its role in robust estimation. Journal of the American Statistical Association, 69, 382–393, 1974.

    Examples:

    - `HampelFilter([1, 1, 1, 1, 1, 1], window=3) -> pd.Series([False, False, False, False, False, False])`
    - `HampelFilter([1, 1, 1, 2, 1, 1], window=3) -> pd.Series([False, False, False, True, False, False])`
    - `HampelFilter([0, 1, 1, 1, 1, 0], window=3) -> pd.Series([True, False, False, False, False, True])`
    - `HampelFilter([1]) -> pd.Series([False])`

    :param series: Pandas Series object with numbers in which we identify outliers.
    :param window: length of the sliding window (5 points by default), 1 <= window <= len(series).
    :param sigma: sigma is the number of standard deviations which identify the outlier (3 sigma by default), > 0.
    :param scaleFactor: constant scale factor (1.4826 by default for Gaussian distribution), > 0.
    :return: Pandas Series object with True/False values.
             `True` mean that an outlier detected in that position of input series.
             If an error occurred then empty series returned.
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

        # Extending data to avoid undetected anomaly in first and last elements by original algorithm:
        series = pd.concat([series.iloc[: window], series, series.iloc[-window:]])

        # Calculating rolling Median and difference between it and series elements in window:
        rollingMedian = series.rolling(window=2 * window, center=True).median()
        delta = pd.Series.abs(series - rollingMedian)

        # Calculating rolling MAD: MAD(Xi) = Median(|x1 − Median(Xi)|, ..., |xn − Median(Xi)|)
        # where Xi — elements of input series in i-th window
        rollingMAD = series.rolling(window=2 * window, center=True).apply(
            lambda x: pd.Series.median(pd.Series.abs(x - pd.Series.median(x)))
        )

        # Checking for anomaly: A = {a | |a − Median(Xi)| > s ∙ k ∙ MAD(Xi)}
        new = delta > sigma * scaleFactor * rollingMAD
        new = new.iloc[window: -window]

    except Exception:
        new = pd.Series()

    return new


def HampelAnomalyDetection(series: Union[list, pd.Series], **kwargs) -> Optional[int]:
    """
    Anomaly Detection function using Hampel Filter. This function returns the minimum index of elements in anomaly list
    or index of the first maximum element in input series if this index less than anomaly element index. If series has
    no anomalies then `None` will be return.

    Anomaly filter is a function:
    F: X → {True, False}. F(xi) = True, if xi ∈ A; False, if xi ∉ A, where X — input series with xi elements, A — anomaly set.

    References:

    1. Gilmullin T.M., Gilmullin M.F. How to quickly find anomalies in number series using the Hampel method. December 27, 2022.
       - Link (EN): https://forworktests.blogspot.com/2023/01/how-to-quickly-find-anomalies-in-number.html
       - Link (RU): https://forworktests.blogspot.com/2022/12/blog-post.html
    2. Jupyter Notebook with examples:
       - Link (EN): https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample_EN.ipynb
       - Link (RU): https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample.ipynb
    3. Simple Python script demonstrate how to use Hampel Filter to determine anomalies in time series:
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
    - `HampelAnomalyDetection([9, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 13, 12, 12, 1, 1]) -> 1`
    - `HampelAnomalyDetection([9, 13, 12, 12, 13, 12, 1000, 13, 12, 12, 300000, 12, 12, 13, 12, 2000, 1, 1, 1, 1]) -> 6`

    Some **kwargs parameters you can pass to `HampelFilter()`:

    - `window` is the length of the sliding window (5 points by default), 1 <= window <= len(series).
    - `sigma` is the number of standard deviations which identify the outlier (3 sigma by default), > 0.
    - `scaleFactor` is the constant scale factor (1.4826 by default), > 0.

    :param series: list of numbers or Pandas Series object with numbers in which we identify index of first anomaly (outlier's index).
    :param kwargs: See `HampelFilter()` docstring with all possible parameters.
    :return: index of the first element with anomaly in series will be return or `None` if no anomaly.
    """
    try:
        if isinstance(series, list):
            series = pd.Series(series)

        indexFirstMax = series.idxmax()  # Index of the first maximum in series

        filtered = HampelFilter(series=series, **kwargs)  # The bool series with filtered data (if True then anomaly present in that place of input series)
        anomalyIndexes = filtered[filtered].index  # Indexes list of all found anomalies (if True)

        indexAnomalyMin = min(anomalyIndexes) if len(anomalyIndexes) > 0 else None  # Index of the first True in filtered series or None

        # We need to take the element whose index is less (see examples in docstring):
        result = pd.Series([indexAnomalyMin, indexFirstMax]).min() if indexAnomalyMin is not None else None

    except Exception:
        result = None

    return result
