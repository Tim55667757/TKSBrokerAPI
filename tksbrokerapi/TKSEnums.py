# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
Module contains a lot of constants from enums sections of Tinkoff Open API documentation.

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


TKS_INSTRUMENTS = ["Currencies", "Shares", "Bonds", "Etfs", "Futures"]
"""Type of instrument for trade methods must be only one of supported types, listed in this constant. Default: `["Currencies", "Shares", "Bonds", "Etfs", "Futures"]`"""

TKS_TICKER_ALIASES = {
    "USD": "USD000UTSTOM", "usd": "USD000UTSTOM",  # FIGI: BBG0013HGFT4
    "EUR": "EUR_RUB__TOM", "eur": "EUR_RUB__TOM",  # FIGI: BBG0013HJJ31
    "GBP": "GBPRUB_TOM", "gbp": "GBPRUB_TOM",  # FIGI: BBG0013HQ5F0
    "CHF": "CHFRUB_TOM", "chf": "CHFRUB_TOM",  # FIGI: BBG0013HQ5K4
    "CNY": "CNYRUB_TOM", "cny": "CNYRUB_TOM",  # FIGI: BBG0013HRTL0
    "HKD": "HKDRUB_TOM", "hkd": "HKDRUB_TOM",  # FIGI: BBG0013HSW87
    "TRY": "TRYRUB_TOM", "try": "TRYRUB_TOM",  # FIGI: BBG0013J12N1
}
"""Some aliases instead official tickers for using in CLI. For example, you can use `"USD"` instead of `"USD000UTSTOM"`."""

# some tickers or FIGIs raised exception earlier when it sends to server, that is why we exclude there:
TKS_TICKERS_OR_FIGI_EXCLUDED = [
    # "ISSUANCEBRUS",  # now available
]

TKS_TIMEFRAMES = {
    "1min": {"minutes": 1, "maxCandles": 1439},  # max count in block for this API request: 1 day (and -1 minute)
    "2min": {"minutes": 2, "maxCandles": 719},  # max count in block for this API request: 1 day (and -2 minutes)
    "3min": {"minutes": 3, "maxCandles": 479},  # max count in block for this API request: 1 day (and and -3 minutes)
    "5min": {"minutes": 5, "maxCandles": 287},  # max count in block for this API request: 1 day (and -5 minutes)
    "10min": {"minutes": 10, "maxCandles": 143},  # max count in block for this API request: 1 day (and -10 minutes)
    "15min": {"minutes": 15, "maxCandles": 95},  # max count in block for this API request: 1 day (and -15 minutes)
    "30min": {"minutes": 30, "maxCandles": 47},  # max count in block for this API request: 1 day (and -30 minutes)
    "hour": {"minutes": 60, "maxCandles": 167},  # max count in block for this API request: 7 days (and -1 hour)
    "day": {"minutes": 1440, "maxCandles": 365},  # max count in block for this API request: 1 year
    "week": {"minutes": 10080, "maxCandles": 104},  # max count in block for this API request: 2 years
    "month": {"minutes": 43200, "maxCandles": 119},  # max count in block for this API request: 10 years
}
"""How many minutes in interval and maximum count of candles in one history block returns by Tinkoff API in one request.
See more: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetCandles
"""

TKS_TRADING_STATUSES = {
    "SECURITY_TRADING_STATUS_UNSPECIFIED": "Trading status undefined",
    "SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING": "Not available for trading",
    "SECURITY_TRADING_STATUS_OPENING_PERIOD": "Trade opening period",
    "SECURITY_TRADING_STATUS_CLOSING_PERIOD": "Trade closing period",
    "SECURITY_TRADING_STATUS_BREAK_IN_TRADING": "Break in trading",
    "SECURITY_TRADING_STATUS_NORMAL_TRADING": "Normal trading",
    "SECURITY_TRADING_STATUS_CLOSING_AUCTION": "Closing auction",
    "SECURITY_TRADING_STATUS_DARK_POOL_AUCTION": "Large package auction",
    "SECURITY_TRADING_STATUS_DISCRETE_AUCTION": "Discrete auction",
    "SECURITY_TRADING_STATUS_OPENING_AUCTION_PERIOD": "Opening auction",
    "SECURITY_TRADING_STATUS_TRADING_AT_CLOSING_AUCTION_PRICE": "Trading period at the closing auction price",
    "SECURITY_TRADING_STATUS_SESSION_ASSIGNED": "Session assigned",
    "SECURITY_TRADING_STATUS_SESSION_CLOSE": "Session closed",
    "SECURITY_TRADING_STATUS_SESSION_OPEN": "Session is open",
    "SECURITY_TRADING_STATUS_DEALER_NORMAL_TRADING": "Broker's internal liquidity mode trading",
    "SECURITY_TRADING_STATUS_DEALER_BREAK_IN_TRADING": "Break in trading in the broker's internal liquidity mode",
    "SECURITY_TRADING_STATUS_DEALER_NOT_AVAILABLE_FOR_TRADING": "Broker's internal liquidity mode is not available",
}
"""Security Trading Status enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/orders/#securitytradingstatus"""

TKS_OPERATION_TYPES = {
    "OPERATION_TYPE_UNSPECIFIED": "The operation type is not defined",
    "OPERATION_TYPE_INPUT": "Deposit on broker account",
    "OPERATION_TYPE_BOND_TAX": "Withholding personal income tax on bond coupons",
    "OPERATION_TYPE_OUTPUT_SECURITIES": "Securities output",
    "OPERATION_TYPE_OVERNIGHT": "Overnight REPO income",
    "OPERATION_TYPE_TAX": "Tax withholding",
    "OPERATION_TYPE_BOND_REPAYMENT_FULL": "Full bond redemption",
    "OPERATION_TYPE_SELL_CARD": "Sell securities from the card",
    "OPERATION_TYPE_DIVIDEND_TAX": "Withholding tax on dividends",
    "OPERATION_TYPE_OUTPUT": "Withdrawals",
    "OPERATION_TYPE_BOND_REPAYMENT": "Bonds partial redemption",
    "OPERATION_TYPE_TAX_CORRECTION": "Tax correction",
    "OPERATION_TYPE_SERVICE_FEE": "Brokerage account maintenance fee deduction",
    "OPERATION_TYPE_BENEFIT_TAX": "Withholding tax for material benefits",
    "OPERATION_TYPE_MARGIN_FEE": "Withholding commission for an uncovered position",
    "OPERATION_TYPE_BUY": "Buy securities",
    "OPERATION_TYPE_BUY_CARD": "Buy securities from a card",
    "OPERATION_TYPE_INPUT_SECURITIES": "Transfer securities from another depository",
    "OPERATION_TYPE_SELL_MARGIN": "Sell (by margin call)",
    "OPERATION_TYPE_BROKER_FEE": "Operation fee deduction",
    "OPERATION_TYPE_BUY_MARGIN": "Buy (by margin call)",
    "OPERATION_TYPE_DIVIDEND": "Dividends income",
    "OPERATION_TYPE_SELL": "Sell securities",
    "OPERATION_TYPE_COUPON": "Coupons income",
    "OPERATION_TYPE_SUCCESS_FEE": "Success fee deduction",
    "OPERATION_TYPE_DIVIDEND_TRANSFER": "Transfer of dividend income",
    "OPERATION_TYPE_ACCRUING_VARMARGIN": "Variation margin crediting",
    "OPERATION_TYPE_WRITING_OFF_VARMARGIN": "Withholding variation margin",
    "OPERATION_TYPE_DELIVERY_BUY": "Buy (futures contract expired)",
    "OPERATION_TYPE_DELIVERY_SELL": "Sell (futures contract expired)",
    "OPERATION_TYPE_TRACK_MFEE": "Autotrack account management fee",
    "OPERATION_TYPE_TRACK_PFEE": "Pay per result on auto follow score",
    "OPERATION_TYPE_TAX_PROGRESSIVE": "Tax withholding at the rate of 15%",
    "OPERATION_TYPE_BOND_TAX_PROGRESSIVE": "Withholding tax on coupons at the rate of 15%",
    "OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE": "Withholding tax on dividends at the rate of 15%",
    "OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE": "Withholding tax for material benefits at the rate of 15%",
    "OPERATION_TYPE_TAX_CORRECTION_PROGRESSIVE": "Tax correction at the rate of 15%",
    "OPERATION_TYPE_TAX_REPO_PROGRESSIVE": "Withholding tax on refunds on REPO transactions at the rate of 15%",
    "OPERATION_TYPE_TAX_REPO": "Tax withholding on REPO trade refunds",
    "OPERATION_TYPE_TAX_REPO_HOLD": "Tax hold on REPO transactions",
    "OPERATION_TYPE_TAX_REPO_REFUND": "Tax refund on REPO transactions",
    "OPERATION_TYPE_TAX_REPO_HOLD_PROGRESSIVE": "Withholding tax on REPO transactions at the rate of 15%",
    "OPERATION_TYPE_TAX_REPO_REFUND_PROGRESSIVE": "Tax refund on REPO transactions at the rate of 15%",
    "OPERATION_TYPE_DIV_EXT": "Payout dividends to the card",
    "OPERATION_TYPE_TAX_CORRECTION_COUPON": "Coupon tax correction",
}
"""Operation type enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/operations/#operationtype"""

TKS_OPERATION_STATES = {
    "OPERATION_STATE_UNSPECIFIED": "! Unknown",
    "OPERATION_STATE_EXECUTED": "√ Executed",
    "OPERATION_STATE_CANCELED": "× Canceled",
}
"""Operation state enums  in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/operations/#operationstate"""

TKS_ORDER_DIRECTIONS = {
    "ORDER_DIRECTION_UNSPECIFIED": "Undefined",
    "ORDER_DIRECTION_BUY": "↑ Buy",
    "ORDER_DIRECTION_SELL": "↓ Sell",
}
"""Order direction enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/orders/#orderdirection"""

TKS_STOP_ORDER_DIRECTIONS = {
    "STOP_ORDER_DIRECTION_UNSPECIFIED": "Undefined",
    "STOP_ORDER_DIRECTION_BUY": "↑ Buy",
    "STOP_ORDER_DIRECTION_SELL": "↓ Sell",
}
"""Stop-order direction enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/stoporders/#stoporderdirection"""

TKS_ORDER_TYPES = {
    "ORDER_TYPE_UNSPECIFIED": "Undefined",
    "ORDER_TYPE_LIMIT": "Limit",
    "ORDER_TYPE_MARKET": "Market",
}
"""Order type enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/orders/#ordertype"""

TKS_STOP_ORDER_TYPES = {
    "STOP_ORDER_TYPE_UNSPECIFIED": "Undefined",
    "STOP_ORDER_TYPE_TAKE_PROFIT": "Take profit",
    "STOP_ORDER_TYPE_STOP_LOSS": "Stop loss",
    "STOP_ORDER_TYPE_STOP_LIMIT": "Stop limit",
}
"""Stop-order type enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/stoporders/#stopordertype"""

TKS_ORDER_STATES = {
    "EXECUTION_REPORT_STATUS_UNSPECIFIED": "! Unknown",
    "EXECUTION_REPORT_STATUS_FILL": "Performed",
    "EXECUTION_REPORT_STATUS_REJECTED": "Rejected",
    "EXECUTION_REPORT_STATUS_CANCELLED": "Cancelled",
    "EXECUTION_REPORT_STATUS_NEW": "New order",
    "EXECUTION_REPORT_STATUS_PARTIALLYFILL": "Partially filled",
}
"""Order status enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/orders/#orderexecutionreportstatus"""

TKS_STOP_ORDER_EXPIRATION_TYPES = {
    "STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED": "Undefined",
    "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL": "Until cancel",
    "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE": "Until date",
}
"""Expiration type of stop-orders enums in Tinkoff Broker OpenAPI: https://tinkoff.github.io/investAPI/stoporders/#stoporderexpirationtype"""
