# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from tksbrokerapi import TKSBrokerAPI


class TestTKSBrokerAPIMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        TKSBrokerAPI.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        TKSBrokerAPI.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        TKSBrokerAPI.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt
        # set up default parameters:
        # self.server = r"https://invest-public-api.tinkoff.ru/rest"
        # self.token = "demo"
        # self.timeout = 3
        # self.tickers = ["IBM", "YNDX", "USD", "RU000A101YV8", "TGLD"]
        # self.figis = ["BBG000BLNNH6", "BBG006L8G4H1", "BBG0013HGFT4", "TCS00A101YV8", "BBG222222222"]
        # self.depth = 3

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

    def test_FloatToNanoCheckType(self):
        assert isinstance(TKSBrokerAPI.FloatToNano(123.456789), dict), "Not dict type returned!"

    def test_FloatToNanoPositive(self):
        testData = [
            (2.5, {"units": "2", "nano": 500000000}), (0.05, {"units": "0", "nano": 50000000}), (0, {"units": "0", "nano": 0}),
            (1.9, {"units": "1", "nano": 900000000}), (1.000000009, {"units": "1", "nano": 9}),
            (-1.9, {"units": "-1", "nano": -900000000}), (-1.000000009, {"units": "-1", "nano": -9}),
            (0.1, {"units": "0", "nano": 100000000}), (-0.1, {"units": "0", "nano": -100000000}),
            (1.01, {"units": "1", "nano": 10000000}), (-1.01, {"units": "-1", "nano": -10000000}),
            (10.001, {"units": "10", "nano": 1000000}), (-10.001, {"units": "-10", "nano": -1000000}),
            (100.0001, {"units": "100", "nano": 100000}), (-100.0001, {"units": "-100", "nano": -100000}),
            (1000.00001, {"units": "1000", "nano": 10000}), (-1000.00001, {"units": "-1000", "nano": -10000}),
            (10000.000001, {"units": "10000", "nano": 1000}), (-10000.000001, {"units": "-10000", "nano": -1000}),
            (100000.0000001, {"units": "100000", "nano": 100}), (-100000.0000001, {"units": "-100000", "nano": -100}),
            (1000000.00000001, {"units": "1000000", "nano": 10}), (-1000000.00000001, {"units": "-1000000", "nano": -10}),
            (1.000000001, {"units": "1", "nano": 1}), (-1.000000001, {"units": "-1", "nano": -1}),
            (1.0000000001, {"units": "1", "nano": 0}), (-1.0000000001, {"units": "-1", "nano": 0}),
        ]
        for test in testData:
            result = TKSBrokerAPI.FloatToNano(number=test[0])
            assert result == test[1], 'Expected `FloatToNano(number="{}") == {}`, but `result == {}`'.format(test[0], test[1], result)

    def test_GetDatesAsStringCheckType(self):
        result = TKSBrokerAPI.GetDatesAsString(None, None)
        assert isinstance(result, tuple), "Not tuple type returned!"
        assert isinstance(result[0], str), "Not str type in first parameter returned!"
        assert isinstance(result[1], str), "Not str type in second parameter returned!"

    def test_GetDatesAsStringPositive(self):
        now = datetime.now(tzutc())
        delta = timedelta(seconds=1)  # diff between expected and actual results must be less than this value
        testData = [
            (None, None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                now,
            )),
            ("today", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                now,
            )),
            ("yesterday", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1),
                now.replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1),
            )),
            ("week", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7),
                now,
            )),
            ("month", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30),
                now,
            )),
            ("year", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=365),
                now,
            )),
            ("-1", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1),
                now,
            )),
            ("-2", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2),
                now,
            )),
            ("-365", None, (
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=365),
                now,
            )),
            ("2020-02-20", None, (
                datetime.strptime("2020-02-20", "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                now,
            )),
            ("2020-02-20", "2022-02-22", (
                datetime.strptime("2020-02-20", "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                datetime.strptime("2022-02-22", "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=tzutc()),
            )),
        ]
        for test in testData:
            result = TKSBrokerAPI.GetDatesAsString(start=test[0], end=test[1])
            dateFormat = "%Y-%m-%dT%H:%M:%SZ"
            resultDates = (
                datetime.strptime(result[0], dateFormat).replace(tzinfo=tzutc()),
                datetime.strptime(result[1], dateFormat).replace(tzinfo=tzutc()),
            )
            delta0 = resultDates[0] - test[2][0] if resultDates[0] >= test[2][0] else test[2][0] - resultDates[0]
            delta1 = resultDates[1] - test[2][1] if resultDates[1] >= test[2][1] else test[2][1] - resultDates[1]
            assert delta0 <= delta, 'Expected output ("{}", "{}") and delta must be <= 1 sec!\nActual: `GetDatesAsString(start="{}", end="{}") -> ("{}", "{}")`'.format(
                test[2][0].strftime(dateFormat), test[2][1].strftime(dateFormat), test[0], test[1], result[0], result[1],
            )
            assert delta1 <= delta, 'Expected output ("{}", "{}") and delta must be <= 1 sec!\nActual: `GetDatesAsString(start="{}", end="{}") -> ("{}", "{}")`'.format(
                test[2][0].strftime(dateFormat), test[2][1].strftime(dateFormat), test[0], test[1], result[0], result[1],
            )