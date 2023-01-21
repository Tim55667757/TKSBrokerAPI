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
import yaml
from dateutil.tz import tzlocal
from math import ceil
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger  # Main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSEnums import TKS_PRINT_DATE_TIME_FORMAT, TKS_TICKER_ALIASES, TKS_ORDER_DIRECTIONS, TKS_STOP_ORDER_DIRECTIONS
from tksbrokerapi.TradeRoutines import *


def Trade():
    pass


if __name__ == "__main__":
    Trade()  # Initialization, parametrization and run trading scenario
