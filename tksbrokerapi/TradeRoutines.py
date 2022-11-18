# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
This library contains some methods used by trade scenarios implemented with TKSBrokerAPI module.

- **TKSBrokerAPI module documentation:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
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
