# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)

Module **TKSEnums** contains a lot of constants from enums sections of Tinkoff Open API documentation used by TKSBrokerAPI module.

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


TKS_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
"""Date and time string format used by Tinkoff Open API. Default: `"%Y-%m-%dT%H:%M:%SZ"`."""

TKS_DATE_TIME_FORMAT_EXT = "%Y-%m-%dT%H:%M:%S.%fZ"
"""Extended date and time string format used by Tinkoff Open API. Default: `"%Y-%m-%dT%H:%M:%S.%fZ"`."""

TKS_DATE_FORMAT = "%Y-%m-%d"
"""Date string format for some methods. Default: `"%Y-%m-%d"`."""

TKS_PRINT_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
"""Human-readable format of date and time string. Default: `"%Y-%m-%d %H:%M:%S"`."""

TKS_INSTRUMENTS = ["Currencies", "Shares", "Bonds", "Etfs", "Futures"]
"""Type of instrument for trade methods must be only one of supported types, listed in this constant. Default: `["Currencies", "Shares", "Bonds", "Etfs", "Futures"]`"""

TKS_TICKER_ALIASES = {
    "USD": "USD000UTSTOM",  # FIGI: BBG0013HGFT4
    "EUR": "EUR_RUB__TOM",  # FIGI: BBG0013HJJ31
    "GBP": "GBPRUB_TOM",  # FIGI: BBG0013HQ5F0
    "CHF": "CHFRUB_TOM",  # FIGI: BBG0013HQ5K4
    "CNY": "CNYRUB_TOM",  # FIGI: BBG0013HRTL0
    "HKD": "HKDRUB_TOM",  # FIGI: BBG0013HSW87
    "TRY": "TRYRUB_TOM",  # FIGI: BBG0013J12N1
}
"""Some aliases instead official tickers for using in CLI. For example, you can use `"USD"` instead of `"USD000UTSTOM"`."""

# some tickers or FIGIs raised exception earlier when it sends to server, that is why we exclude there:
TKS_TICKERS_OR_FIGI_EXCLUDED = [
    "ISSUANCEBRUS",
]

TKS_CANDLE_INTERVALS = {  # List values: 1st - Tinkoff API parameter, 2nd - minutes count, 3rd - max candles in block
    "Undefined": ["CANDLE_INTERVAL_UNSPECIFIED", 0, 0],
    "1min": ["CANDLE_INTERVAL_1_MIN", 1, 1438],  # max count in API request block: 1 day (1440 min) and -2 minute
    "5min": ["CANDLE_INTERVAL_5_MIN", 5, 287],  # max count in API request block: 1 day (288 by 5 min) and -5 minute
    "15min": ["CANDLE_INTERVAL_15_MIN", 15, 95],  # max count in API request block: 1 day (96 by 15 min) and -15 minute
    "hour": ["CANDLE_INTERVAL_HOUR", 60, 167],  # max count in API request block: 1 week (168 hours) and -1 hour
    "day": ["CANDLE_INTERVAL_DAY", 1440, 364],  # max count in API request block: 1 year (365 days) and -1 day
}
"""Candles interval for requesting history data with Tinkoff API. Current available keys are `"1min"`, `"5min"`, `"15min"`, `"hour"`, `"day"`.
See more: https://tinkoff.github.io/investAPI/swagger-ui/#/MarketDataService/MarketDataService_GetCandles
"""

TKS_ACCOUNT_STATUSES = {
    "ACCOUNT_STATUS_UNSPECIFIED": "Account status undefined",
    "ACCOUNT_STATUS_NEW": "New, open in progress...",
    "ACCOUNT_STATUS_OPEN": "Opened and active account",
    "ACCOUNT_STATUS_CLOSED": "Closed account",
}
"""Account status, enums: https://tinkoff.github.io/investAPI/users/#accountstatus"""

TKS_ACCOUNT_TYPES = {
    "ACCOUNT_TYPE_UNSPECIFIED": "Account type undefined",
    "ACCOUNT_TYPE_TINKOFF": "Tinkoff brokerage account",
    "ACCOUNT_TYPE_TINKOFF_IIS": "IIS account",
    "ACCOUNT_TYPE_INVEST_BOX": "Investment \"piggy bank\"",
}
"""Account type, enums: https://tinkoff.github.io/investAPI/users/#accounttype"""

TKS_ACCESS_LEVELS = {
    "ACCOUNT_ACCESS_LEVEL_UNSPECIFIED": "Access level undefined",
    "ACCOUNT_ACCESS_LEVEL_FULL_ACCESS": "Full access",
    "ACCOUNT_ACCESS_LEVEL_READ_ONLY": "Read-only access",
    "ACCOUNT_ACCESS_LEVEL_NO_ACCESS": "No access",
}
"""Access level, enums: https://tinkoff.github.io/investAPI/users/#accesslevel"""

TKS_QUALIFIED_TYPES = {
    "derivative": "Futures and Options",
    "structured_bonds": "Structured bonds",
    "closed_fund": "Closed-ended funds",
    "bond": "Bonds with low rating",
    "structured_income_bonds": "Structured income bonds",
    "foreign_shares": "Foreign shares not included in the exchange quotation lists",
    "foreign_etf": "Foreign ETF",
    "foreign_bond": "Euro-bonds",
    "russian_shares": "Russian shares not included in quotation lists",
    "leverage": "Margin trading, unsecured leveraged trades",
    "repo": "REPO agreements",
    "convertible_bonds": "Convertible bonds",
    "foreign_bonds_russian_law": "Foreign bonds by Russian law",
    "russian_bonds_foreign_law": "Russian bonds by foreign law",
    "non_quoted_instruments": "Non quoted instruments",
    "option": "Option",
}
"""Values of `qualified_for_work_with`, field: https://tinkoff.github.io/investAPI/faq_users/#qualified_for_work_with"""

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
"""Security Trading Status, enums: https://tinkoff.github.io/investAPI/orders/#securitytradingstatus"""

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
"""Operation type, enums: https://tinkoff.github.io/investAPI/operations/#operationtype"""

TKS_OPERATION_STATES = {
    "OPERATION_STATE_UNSPECIFIED": "! Unknown",
    "OPERATION_STATE_EXECUTED": "√ Executed",
    "OPERATION_STATE_CANCELED": "× Canceled",
    "OPERATION_STATE_PROGRESS": "↻ Progress",
}
"""Operation state, enums: https://tinkoff.github.io/investAPI/operations/#operationstate"""

TKS_ORDER_DIRECTIONS = {
    "ORDER_DIRECTION_UNSPECIFIED": "Undefined",
    "ORDER_DIRECTION_BUY": "↑ Buy",
    "ORDER_DIRECTION_SELL": "↓ Sell",
}
"""Order direction, enums: https://tinkoff.github.io/investAPI/orders/#orderdirection"""

TKS_STOP_ORDER_DIRECTIONS = {
    "STOP_ORDER_DIRECTION_UNSPECIFIED": "Undefined",
    "STOP_ORDER_DIRECTION_BUY": "↑ Buy",
    "STOP_ORDER_DIRECTION_SELL": "↓ Sell",
}
"""Stop-order direction, enums: https://tinkoff.github.io/investAPI/stoporders/#stoporderdirection"""

TKS_ORDER_TYPES = {
    "ORDER_TYPE_UNSPECIFIED": "Undefined",
    "ORDER_TYPE_LIMIT": "Limit",
    "ORDER_TYPE_MARKET": "Market",
}
"""Order type, enums: https://tinkoff.github.io/investAPI/orders/#ordertype"""

TKS_STOP_ORDER_TYPES = {
    "STOP_ORDER_TYPE_UNSPECIFIED": "Undefined",
    "STOP_ORDER_TYPE_TAKE_PROFIT": "Take profit",
    "STOP_ORDER_TYPE_STOP_LOSS": "Stop loss",
    "STOP_ORDER_TYPE_STOP_LIMIT": "Stop limit",
}
"""Stop-order type, enums: https://tinkoff.github.io/investAPI/stoporders/#stopordertype"""

TKS_ORDER_STATES = {
    "EXECUTION_REPORT_STATUS_UNSPECIFIED": "! Unknown",
    "EXECUTION_REPORT_STATUS_FILL": "Performed",
    "EXECUTION_REPORT_STATUS_REJECTED": "Rejected",
    "EXECUTION_REPORT_STATUS_CANCELLED": "Cancelled",
    "EXECUTION_REPORT_STATUS_NEW": "New order",
    "EXECUTION_REPORT_STATUS_PARTIALLYFILL": "Partially filled",
}
"""Order status, enums: https://tinkoff.github.io/investAPI/orders/#orderexecutionreportstatus"""

TKS_STOP_ORDER_EXPIRATION_TYPES = {
    "STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED": "Undefined",
    "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL": "Until cancel",
    "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE": "Until date",
}
"""Expiration type of stop-orders, enums: https://tinkoff.github.io/investAPI/stoporders/#stoporderexpirationtype"""

TKS_COUPON_TYPES = {
    "COUPON_TYPE_UNSPECIFIED": "Undefined",
    "COUPON_TYPE_CONSTANT": "Constant",
    "COUPON_TYPE_FLOATING": "Floating",
    "COUPON_TYPE_DISCOUNT": "Discount",
    "COUPON_TYPE_MORTGAGE": "Mortgage",
    "COUPON_TYPE_FIX": "Fixed",
    "COUPON_TYPE_VARIABLE": "Variable",
    "COUPON_TYPE_OTHER": "Other",
}
"""Coupon type of bonds, enums: https://tinkoff.github.io/investAPI/instruments/#coupontype"""

TKS_REAL_EXCHANGES = {
    "REAL_EXCHANGE_UNSPECIFIED": "Undefined",
    "REAL_EXCHANGE_MOEX": "MOEX",
    "REAL_EXCHANGE_RTS": "SPBEX",
    "REAL_EXCHANGE_OTC": "OTC",
}
"""The real exchange for the execution of trades, enums: https://tinkoff.github.io/investAPI/instruments/#realexchange"""

TKS_SHARE_TYPES = {
    "SHARE_TYPE_UNSPECIFIED": "Undefined",
    "SHARE_TYPE_COMMON": "Ordinary",
    "SHARE_TYPE_PREFERRED": "Privileged",
    "SHARE_TYPE_ADR": "American Depositary Receipts (ADR)",
    "SHARE_TYPE_GDR": "Global Depositary Receipts (GDR)",
    "SHARE_TYPE_MLP": "Master Limited Partnership (MLP)",
    "SHARE_TYPE_NY_REG_SHRS": "New York registered shares",
    "SHARE_TYPE_CLOSED_END_FUND": "Closed investment fund",
    "SHARE_TYPE_REIT": "Real estate trust",
}
"""Share type, enums: https://tinkoff.github.io/investAPI/instruments/#sharetype"""
