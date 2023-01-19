# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
Anomaly Volumes Detector is a simple TG-bot for detecting anomaly volumes of Buyers and Sellers prices.

The bot monitors the volumes of Buyers and Sellers in the orders book (DOM), looks for anomalies in the number series
of volumes and notifies in Telegram. The notification contains: the current price and prices with anomaly volumes.
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

from datetime import datetime, timedelta
from dateutil.tz import tzlocal, tzutc

from tksbrokerapi.TKSBrokerAPI import TinkoffBrokerServer, uLogger  # Main module for trading operations: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
from tksbrokerapi.TKSEnums import TKS_PRINT_DATE_TIME_FORMAT


def Trade():
    pass


if __name__ == "__main__":
    Trade()  # Initialization, parametrization and run trading scenario
