# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
This library contains some methods used by trade scenarios implemented with TKSBrokerAPI module.

- **TKSBrokerAPI module documentation:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
- **TKSBrokerAPI CLI examples:** https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md
- **About Tinkoff Invest API:** https://tinkoff.github.io/investAPI/
- **Tinkoff Invest API documentation:** https://tinkoff.github.io/investAPI/swagger-ui/
- **Open account for trading:** http://tinkoff.ru/sl/AaX1Et1omnH
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


# --- Main constants:

NANO = 0.000000001  # SI-constant nano = 10^-9


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
    - `year` (-365 day from 00:00:00 to the end of current day),

    :param start: start day in format defined by `userFormat` or keyword.
    :param end: end day in format defined by `userFormat`.
    :param userFormat: user-friendly date format, e.g. `"%Y-%m-%d"`.
    :param outputFormat: output string date format.
    :return: tuple with 2 strings `("start", "end")`. Example of return is `("2022-06-01T00:00:00Z", "2022-06-20T23:59:59Z")`.
             Second string is the end of the last day.
    """
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
