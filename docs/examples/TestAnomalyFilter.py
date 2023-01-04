# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
This simple script demonstrate how to use Hampel Filter to determine anomalies in OHLCV-candlestick time series.
Just run this script.

See also:
- Article about Hampel Filter: ???
- Jupyter Notebook with another yet examples: https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/HampelFilteringExample_EN.ipynb

---

Этот скрипт демонстрирует простой пример, как можно использовать фильтр Хампеля для определения аномалий во временном ряду OHLCV-свечей.
Просто запустите этот скрипт.

Смотрите также:
- Статья про фильтр Хампеля: https://forworktests.blogspot.com/2022/12/blog-post.html
- Jupyter Notebook с дополнительными примерами: https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/HampelFilteringExample.ipynb
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


from pricegenerator.PriceGenerator import PriceGenerator, uLogger
from datetime import datetime, timedelta
import pandas as pd
from tksbrokerapi.TradeRoutines import HampelFilter


# Use debug lof from PriceGenerator (set to 20 or 30 to suppress log verbosity):
uLogger.setLevel(10)
uLogger.level = 10
uLogger.handlers[0].level = 10

# Initialize PriceGenerator:
priceModel = PriceGenerator()
priceModel.ticker = "TEST_PRICES"
priceModel.precision = 0
priceModel.timeframe = timedelta(days=1)
priceModel.timeStart = datetime.today()
priceModel.horizon = 100
priceModel.maxClose = 240
priceModel.minClose = 140
priceModel.initClose = 175
priceModel.maxOutlier = 20
priceModel.maxCandleBody = 10
priceModel.maxVolume = 400000
priceModel.upCandlesProb = 0.51
priceModel.outliersProb = 0.07
priceModel.trendDeviation = 0.005
priceModel.trendSplit = "/-/"
priceModel.splitCount = [50, 20, 30]

priceModel.Generate()  # Generating main candles series.
# priceModel.LoadFromFile("hampel.csv")  # Load exist series.

# Calculate upper and lower shadows, and body size:
priceModel.prices["body"] = abs(priceModel.prices.close - priceModel.prices.open)
priceModel.prices["upper"] = priceModel.prices.high - priceModel.prices[["open", "close"]].max(axis=1)
priceModel.prices["lower"] = priceModel.prices[["open", "close"]].min(axis=1) - priceModel.prices.low

# Let's draw new average line on the main chart and set markers on the top, center and bottom of candles:
fUpper = HampelFilter(priceModel.prices.upper, window=len(priceModel.prices.upper))
fBody = HampelFilter(priceModel.prices.body, window=len(priceModel.prices.body))
fLower = HampelFilter(priceModel.prices.lower, window=len(priceModel.prices.lower))

# Creating series with markers on anomaly elements (empty string mean no anomaly):
markers = pd.concat([pd.DataFrame.copy(priceModel.prices, deep=True)[["datetime"]], fUpper, fBody, fLower], axis=1)
markers["markersUpper"] = fUpper.apply(lambda isAnomaly: "↓" if isAnomaly else "")
markers["markersCenter"] = fBody.apply(lambda isAnomaly: "ⓧ" if isAnomaly else "")
markers["markersLower"] = fLower.apply(lambda isAnomaly: "↑" if isAnomaly else "")

# Generating chart:
priceModel.RenderBokeh(
    fileName="hampel.html",
    viewInBrowser=True,
    darkTheme=True,
    markers=markers,
    title="Detect Anomalies With Hampel Method",
    showControlsOnChart=True,  # Set `False` if you don't want to see switches on the legend tab.
    showStatOnChart=True,  # Set `False` to increase speed of chart generating.
    inline=False,  # Set `True` if you run script in Jupyter Notebook.
)
priceModel.SaveToFile("hampel.csv")  # Saving as CSV-file.
