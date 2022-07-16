# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from tksbrokerapi import TKSEnums


class TestConstantsConsistent:
    """Checks consistent of constants"""

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        pass

    def test_ConsistentOfConstantsNames(self):
        mainConstantsNames = [
            "TKS_INSTRUMENTS",
            "TKS_OPERATION_STATES",
            "TKS_OPERATION_TYPES",
            "TKS_ORDER_DIRECTIONS",
            "TKS_ORDER_STATES",
            "TKS_ORDER_TYPES",
            "TKS_STOP_ORDER_DIRECTIONS",
            "TKS_STOP_ORDER_EXPIRATION_TYPES",
            "TKS_STOP_ORDER_TYPES",
            "TKS_TICKERS_OR_FIGI_EXCLUDED",
            "TKS_TICKER_ALIASES",
            "TKS_TIMEFRAMES",
            "TKS_TRADING_STATUSES",
        ]
        currentConstantsNames = list(dir(TKSEnums))
        for cName in mainConstantsNames:
            assert cName in currentConstantsNames, "Attention! One of main constants changed it's name! Before: [{}], but now it is not in constants list.".format(cName)

    def test_AvailableInstruments(self):
        mainInstruments = ["Currencies", "Shares", "Bonds", "Etfs", "Futures"]
        currentInstruments = TKSEnums.TKS_INSTRUMENTS
        for instrument in mainInstruments:
            assert instrument in currentInstruments, "Attention! Instrument [{}] not in available list or change it's name!".format(instrument)
