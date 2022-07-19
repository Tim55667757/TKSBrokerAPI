# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from tksbrokerapi import TKSBrokerAPI


class TestTKSBrokerAPIMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        TKSBrokerAPI.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        TKSBrokerAPI.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        TKSBrokerAPI.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt
        # set up default parameters:
        self.server = r"https://invest-public-api.tinkoff.ru/rest"
        self.token = "demo"
        self.timeout = 3
        self.tickers = ["IBM", "YNDX", "USD", "RU000A101YV8", "TGLD"]
        self.figis = ["BBG000BLNNH6", "BBG006L8G4H1", "BBG0013HGFT4", "TCS00A101YV8", "BBG222222222"]
        self.depth = 3

    def test_NanoToFloatCheckType(self):
        assert isinstance(TKSBrokerAPI.NanoToFloat("123", 456789000), float), "Not float type returned!"

    def test_NanoToFloatPositive(self):
        testData = [
            ("2", 500000000, 2.5), ("0", 50000000, 0.05), ("0", 0, 0.),
            ("0", 100000000, 0.1), ("0", 1, 0.000000001), ("0", -100000000, -0.1), ("0", -1, -0.000000001),
            ("-10", -100000000, -10.1), ("-10", -1, -10.000000001), ("1", 1, 1.000000001), ("-1", -9, -1.000000009),
            ("-100", -10000000, -100.01), ("-100", -10, -100.00000001), ("10", 2, 10.000000002), ("-10", -8, -10.000000008),
            ("-1000", -1000000, -1000.001), ("-1000", -100, -1000.0000001), ("100", 3, 100.000000003), ("-100", -7, -100.000000007),
            ("-10000", -100000, -10000.0001), ("-10000", -1000, -10000.000001), ("1000", 4, 1000.000000004), ("-1000", -6, -1000.000000006),
            ("-100000", -10000, -100000.00001), ("-100000", -10000, -100000.00001), ("10000", 5, 10000.000000005), ("-10000", -5, -10000.000000005),
            ("-1000000", -1000, -1000000.000001), ("-1000000", -100000, -1000000.0001), ("100000", 6, 100000.000000006), ("-100000", -4, -100000.000000004),
            ("-10000000", -100, -10000000.0000001), ("-10000000", -1000000, -10000000.001), ("1000000", 7, 1000000.000000007), ("-1000000", -3, -1000000.000000003),
            ("-100000000", -10, -100000000.00000001), ("-100000000", -10000000, -100000000.01), ("10000000", 8, 10000000.000000008), ("-10000000", -2, -10000000.000000002),
            ("-1000000000", -1, -1000000000.000000001), ("-1000000000", -100000000, -1000000000.1), ("100000000", 9, 100000000.000000009), ("-100000000", -1, -100000000.000000001),
        ]
        for test in testData:
            result = TKSBrokerAPI.NanoToFloat(units=test[0], nano=test[1])
            assert result == test[2], 'Expected `NanoToFloat(units="{}", nano={}) == {}`, but `result == {}`'.format(test[0], test[1], test[2], result)
