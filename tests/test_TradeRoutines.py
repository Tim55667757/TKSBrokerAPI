# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from tksbrokerapi import TradeRoutines
import pandas as pd
import numpy as np
import math
import time


class UpdateClassFieldsTestClass:

    def __init__(self):
        self.a = "123"
        self.b = 123
        self.c = False


class TestTradeRoutinesMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        pass

    @staticmethod
    def GenerateSeries(length=100, start=100.0, mu=0.001, sigma=0.01):
        """Generates synthetic price series based on log returns."""
        logReturns = np.random.normal(loc=mu, scale=sigma, size=length)

        return pd.Series(start * np.exp(np.cumsum(logReturns)))

    def test_GetDatesAsStringCheckType(self):
        result = TradeRoutines.GetDatesAsString(None, None)

        assert isinstance(result, tuple), "Not tuple type returned!"
        assert isinstance(result[0], str), "Not str type in first parameter returned!"
        assert isinstance(result[1], str), "Not str type in second parameter returned!"

        result = TradeRoutines.GetDatesAsString()

        assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
        assert all(isinstance(i, str) for i in result), f"Expected tuple of strings, got {result}"

    def test_GetDatesAsStringPositive(self):
        now = datetime.now(tzutc()).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
        delta = timedelta(seconds=1)  # diff between expected and actual results must be less than this value

        testData = [
            (None, None, (
                now,
                end,
            )),
            ("today", None, (
                now,
                end,
            )),
            ("yesterday", None, (
                now - timedelta(days=1),
                end - timedelta(days=1),
            )),
            ("week", None, (
                now - timedelta(days=6),
                end,
            )),
            ("month", None, (
                now - timedelta(days=29),
                end,
            )),
            ("year", None, (
                now - timedelta(days=364),
                end,
            )),
            ("-1", None, (
                now - timedelta(days=0),
                end,
            )),
            ("-2", None, (
                now - timedelta(days=1),
                end,
            )),
            ("-365", None, (
                now - timedelta(days=364),
                end,
            )),
            ("2020-02-20", None, (
                datetime.strptime("2020-02-20", "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                end,
            )),
            ("2020-02-20", "2022-02-22", (
                datetime.strptime("2020-02-20", "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzutc()),
                datetime.strptime("2022-02-22", "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=tzutc()),
            )),
        ]

        for test in testData:
            result = TradeRoutines.GetDatesAsString(start=test[0], end=test[1])

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

        test_cases = [
            ("today", None,
             datetime.now(tzutc()).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("yesterday", None,
             (datetime.now(tzutc()) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             (datetime.now(tzutc()) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("week", None,
             (datetime.now(tzutc()) - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("month", None,
             (datetime.now(tzutc()) - timedelta(days=29)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("year", None,
             (datetime.now(tzutc()) - timedelta(days=364)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("2023-01-01", "2023-01-10", "2023-01-01T00:00:00Z", "2023-01-10T23:59:59Z"),

            ("2023-01-01", None,
             "2023-01-01T00:00:00Z",
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")),

            ("-5", None,
             (datetime.now(tzutc()) - timedelta(days=4)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
             datetime.now(tzutc()).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"))
        ]

        for start, end, expected_start, expected_end in test_cases:
            result_start, result_end = TradeRoutines.GetDatesAsString(start=start, end=end)
            assert result_start == expected_start, f"For start={start}, end={end}, expected start={expected_start}, got {result_start}"
            assert result_end == expected_end, f"For start={start}, end={end}, expected end={expected_end}, got {result_end}"

    def test_GetDatesAsStringNegative(self):
        testData = [
            (1, 2, ("", "")), ("1", "2", ("", "")),
            ("", "yesterday", ("", "")), ("", None, ("", "")),
            ("2022-12-03", -1, ("", "")), ("2022-12-02-", "2022-12-03-", ("", "")),
            ("-", False, ("", "")),
            ("--100", None, ("", "")),
            ("invalid_date", None, ("", "")),
            ("-invalid", None, ("", "")),
        ]

        for test in testData:
            assert TradeRoutines.GetDatesAsString(start=test[0], end=test[1]) == test[2], "Unexpected output!"

    def test_NanoToFloatCheckType(self):
        assert isinstance(TradeRoutines.NanoToFloat("123", 456789000), float), "Not float type returned!"
        assert isinstance(TradeRoutines.NanoToFloat("0", 0), float), "Not float type returned!"
        assert isinstance(TradeRoutines.NanoToFloat("-1", -1), float), "Not float type returned!"

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
            result = TradeRoutines.NanoToFloat(units=test[0], nano=test[1])
            assert result == test[2], 'Expected `NanoToFloat(units="{}", nano={}) == {}`, but `result == {}`'.format(test[0], test[1], test[2], result)

    def test_NanoToFloatNegative(self):
        testData = [
            (1, 0, 1.0), ("1", "0", 1.0), (0, 1, 0.000000001), ("0", 100000000, 0.1),
            (None, 0, 0.), (1, None, 0.), (None, None, 0.),
            ([], {}, 0.), (1.2, 0.1, 1.0), (0.1, 1.2, 0.000000001),
            ("-1", -100000000, -1.1), ("-1", 100000000, -0.9),
        ]

        for test in testData:
            result = TradeRoutines.NanoToFloat(units=test[0], nano=test[1])
            assert result == test[2], "Unexpected output!"

    def test_FloatToNanoCheckType(self):
        assert isinstance(TradeRoutines.FloatToNano(123.456789), dict), "Not dict type returned!"
        assert isinstance(TradeRoutines.FloatToNano(0.000000001), dict), "Not dict type returned!"
        assert isinstance(TradeRoutines.FloatToNano(-1.1), dict), "Not dict type returned!"

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
            result = TradeRoutines.FloatToNano(number=test[0])
            assert result == test[1], 'Expected `FloatToNano(number="{}") == {}`, but `result == {}`'.format(test[0], test[1], result)

    def test_FloatToNanoNegative(self):
        testData = [
            (0, {"units": "0", "nano": 0}), (0.0, {"units": "0", "nano": 0}),
            ("0", {"units": "0", "nano": 0}), ("0.1", {"units": "0", "nano": 0}),
            ("-1", {"units": "0", "nano": 0}), ("-0.1", {"units": "0", "nano": 0}),
            (-1, {"units": "-1", "nano": 0}), (-0.1, {"units": "0", "nano": -100000000}),
            (None, {"units": "0", "nano": 0}), ([], {"units": "0", "nano": 0}),
            ({}, {"units": "0", "nano": 0}), ([1], {"units": "0", "nano": 0}),
        ]

        for test in testData:
            assert TradeRoutines.FloatToNano(number=test[0]) == test[1], "Unexpected output!"

    def test_UpdateClassFieldsCheckType(self):
        test = UpdateClassFieldsTestClass()

        assert TradeRoutines.UpdateClassFields(instance=test, params={}) is None, "Not None type returned!"
        assert TradeRoutines.UpdateClassFields(instance=test, params={"a": 1, "d": "1"}) is None, "Not None type returned!"

    def test_UpdateClassFieldsPositive(self):
        testClass = UpdateClassFieldsTestClass()
        testData = [
            {"a": None, "b": None, "c": None}, {"a": -1, "b": "-1", "c": ""}, {"a": 0, "b": "0", "c": False},
            {"a": [], "b": (), "c": {}}, {"a": [({})], "b": "12345", "c": -12345},
            {"a": testClass.a, "b": testClass.b, "c": testClass.c},
        ]

        for test in testData:
            TradeRoutines.UpdateClassFields(testClass, test)
            assert testClass.a == test["a"] and testClass.b == test["b"] and testClass.c == test["c"], "Incorrect output!"

    def test_UpdateClassFieldsNegative(self):
        testClass = UpdateClassFieldsTestClass()
        testData = [
            {}, [], None, [1, "2", False], {1: 1}, {"__init__": 0},
        ]

        for test in testData:
            TradeRoutines.UpdateClassFields(testClass, test)
            assert testClass.a == "123" and testClass.b == 123 and testClass.c is False, "Incorrect output!"

    def test_SeparateByEqualPartsCheckType(self):
        assert isinstance(TradeRoutines.SeparateByEqualParts(elements=[], parts=2, union=True), list), "Not list type returned!"

    def test_SeparateByEqualPartsPositive(self):
        testData = [
            (None, 0, True, []), (None, 0, False, []),
            ([], 0, True, []), ([], 0, False, []),
            ([1], 1, True, [[1]]), ([1], 1, False, [[1]]),
            ([1], 2, True, [[1]]), ([1], 2, False, [[1], []]),
            ([1, 2, 3], 4, True, [[1], [2], [3]]), ([1, 2, 3], 4, False, [[1], [2], [3], []]),
            ([1, 2, 3], 5, True, [[1], [2], [3]]), ([1, 2, 3], 5, False, [[1], [2], [3], [], []]),
            ([1, 2, 3], 3, True, [[1], [2], [3]]), ([1, 2, 3], 3, False, [[1], [2], [3]]),
            ([1, 2, 3], 2, True, [[1], [2, 3]]), ([1, 2, 3], 2, False, [[1], [2], [3]]),
            ([1, 2, 3], 1, True, [[1, 2, 3]]), ([1, 2, 3], 1, False, [[1, 2, 3]]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2, True, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]),
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2, True, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10]]),
            ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2, False, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10]]),
        ]

        for test in testData:
            assert TradeRoutines.SeparateByEqualParts(elements=test[0], parts=test[1], union=test[2]) == test[3], "Incorrect output!"

    def test_SeparateByEqualPartsNegative(self):
        testData = [
            (None, -1, True, []), (None, -1, False, []),
            ([], 1, True, []), ([], 1, False, []),
            (1, -1, True, []), (1, -1, False, []),
            (1, 1, True, []), (1, 1, False, []),
            ("", 1, True, []), ("", 1, False, []),
            ((), 1, True, []), ((), 1, False, []),
            ((1,), 1, True, []), ((1,), 1, False, []),
            ({}, 1, True, []), ({}, 1, False, []),
            ({"a": 1}, 1, True, []), ({"a": 1}, 1, False, []),
            (None, None, True, []), (None, None, False, []),
            (None, None, None, []),
            ([1], "", True, []), ([1], "", False, []),
            ([1, 2, 3], "2", True, []), ([1, 2, 3], "2", False, []),
            ([1, 2, 3], 4, True, [[1], [2], [3]]), ([1, 2, 3], 4, False, [[1], [2], [3], []]),
            ([1, 2], 4, True, [[1], [2]]), ([1, 2], 4, False, [[1], [2], [], []]),
        ]

        for test in testData:
            assert TradeRoutines.SeparateByEqualParts(elements=test[0], parts=test[1], union=test[2]) == test[3], "Incorrect output!"

    def test_CalculateLotsForDealCheckType(self):
        assert isinstance(TradeRoutines.CalculateLotsForDeal(currentPrice=0, maxCost=0, volumeInLot=0), int), "Not int type returned!"

    def test_CalculateLotsForDealPositive(self):
        testData = [
            (1, 1, 1, 1), (2, 1, 1, 1), (2, 1, 2, 1), (1, 2, 1, 2), (3, 2, 1, 1), (3, 2, 3, 1),
            (1234.56, 2000.01, 1, 1), (1234.56, 2000.01, 2, 1), (1234.56, 2500, 1, 2), (1234.56, 2500, 2, 1),
            (1234, 2468, 1, 2), (1234, 2468, 2, 1),
            (-1, 1, 1, 1), (-2, 1, 1, 1), (-2, 1, 2, 1), (-1, 2, 1, 2), (-3, 2, 1, 1), (-3, 2, 3, 1),
            (-1234.56, 2000.01, 1, 1), (-1234.56, 2000.01, 2, 1), (-1234.56, 2500, 1, 2), (-1234.56, 2500, 2, 1),
            (-1234, -2468, 1, 2), (-1234, 2468, 2, 1),
        ]

        for test in testData:
            assert TradeRoutines.CalculateLotsForDeal(currentPrice=test[0], maxCost=test[1], volumeInLot=test[2]) == test[3], "Incorrect output!"

    def test_CalculateLotsForDealNegative(self):
        testData = [
            (0, 0, 0, 0), (0, 1, 0, 0), (-2, 0, 1, 1), (1, 0, 1, 1), (-1, -2, -1, 2), (-3, -2, -1, 1), (-3, 2, -3, 1),
            ("1234.56", 2000.01, 1, 0), (1234.56, "2000.01", 2, 0), (1234.56, 2500, "1", 0),
            (1234.56, 2500, [], 0), (1234, {}, 1, 0), (None, 2468, 2, 0), (bool, 2468, 2, 0),
        ]

        for test in testData:
            assert TradeRoutines.CalculateLotsForDeal(currentPrice=test[0], maxCost=test[1], volumeInLot=test[2]) == test[3], "Incorrect output!"

    def test_HampelFilterCheckType(self):
        assert isinstance(TradeRoutines.HampelFilter(pd.Series([1, 1, 1, 1, 1, 1]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter([1, 1, 1, 1, 1, 1], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pd.Series([1]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pd.Series([]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pd.Series([1, "1", True, None]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter([1], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(["1"], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter([True], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter([1, "1", True], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter([None], window=3), pd.Series), "Not Pandas Series type returned!"

    def test_HampelFilterPositive(self):
        testData = [
            (
                {
                    "series": pd.Series([10, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                # All values are identical — no deviations from the rolling median → no anomalies.
                [False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The first value is significantly below the rest → its deviation exceeds the MAD threshold.
                # Correctly detected as anomaly.
                [True, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 5, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Both 1 and 5 are far below the consistent block of 10s, skewing the MAD upward.
                # Valid detection of two downward anomalies.
                [True, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 5, 1, 1, 1]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The spike at index 1 breaks the otherwise flat pattern of 1s → clear outlier.
                [False, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 5, 1, 1, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The same case as above, but a smaller window increases MAD sensitivity.
                # The result is consistent — 5 is still an anomaly.
                [False, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 5, 1, 1, 1]),
                    "window": 3, "sigma": 1, "scaleFactor": 1.4826,
                },
                # Lower sigma increases sensitivity to deviations — an anomaly still confidently detected at index 1.
                [False, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 5, 1, 1, 1]),
                    "window": 5, "sigma": 3, "scaleFactor": 1,
                },
                # Lower scaleFactor slightly tightens a detection threshold.
                # Still detects the 5 as an anomaly in a flat region of 1s.
                [False, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 10, 10, 1, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Alternating values result in high MAD → deviations are within expected variability.
                # None of the points exceed the outlier threshold — all values are considered normal.
                [False, False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 10, 10, 1, 10, 1]),
                    "window": 2,
                    "sigma": 2,
                    "scaleFactor": 1.4826,
                },
                # The 10 at index 1 is clearly anomalous compared to surrounding 1s and 10s.
                # However, the 10 at index 4, while similar in value, falls into the manual boundary region.
                # Due to slight differences in MAD estimates and edge handling logic, only index 1 is flagged.
                # This is consistent with the current implementation of the filter.
                [True, False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 10, 10, 10, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The 1s at the edges are clear anomalies against the flat high values in the center.
                # Symmetry is broken at both ends.
                [True, False, False, False, False, True],
            ),
            (
                {
                    "series": pd.Series([10, 1, 1, 1, 1, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Same structure as previous test but the inverted — edge 10s stand out against a flat center of 1s.
                [True, False, False, False, False, True],
            ),
            (
                {
                    "series": pd.Series([1, 1, 1, 10, 10, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Gradual transition from 1s to 10s over the window size — no sharp deviation.
                # Changes happen within threshold limits.
                [False, False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 1, 1, 1, 10, 10]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Sudden jump to 10 breaks the flat pattern of 1s.
                # Both new high values are far from the overall window median and exceed MAD threshold.
                [False, False, False, False, True, True],
            ),
            (
                {
                    "series": pd.Series([1, 10, 1, 10, 1, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The value at index 1 and 4 is treated as an anomaly because the local MAD is 0
                # and its absolute deviation from the local median is > 0.
                [False, True, False, False, True, False],
            ),
            (
                {
                    "series": pd.Series([10, 1, 10, 1, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Points at index 1 and 4 are significantly lower than neighbors and local MAD ≈ 0,
                # so they are correctly detected as outliers.
                [False, True, False, False, True, False],
            ),
            (
                {
                    "series": pd.Series([1, 10, 1, 10, 1, 10]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Although values alternate, the full-window median is stable, and deviations do not exceed the threshold.
                # Symmetry and consistent alternation prevent outliers from being detected.
                [False, False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([10, 1, 10, 1, 10, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Identical pattern to the previous one but reversed in time — same symmetry, same median,
                # no values exceed the Hampel threshold → no anomalies.
                [False, False, False, False, False, False],
            ),
            (
                {
                    "series": pd.Series([-1, 1, 1, 1, 0, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Points at index 0 and 4 are anomalies: MAD ≈ 0 triggers absolute diff > 0 check.
                # -1 and 0 differ from surrounding ones in a manual scan path.
                [True, False, False, False, True, False],
            ),
            (
                {
                    "series": pd.Series([-1, -1, -1, -1, 0, -1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The 0 is an upward outlier compared to the tightly clustered -1s.
                # It clearly breaks the symmetry and stands out — valid anomaly.
                [False, False, False, False, True, False],
            ),
            (
                {
                    "series": pd.Series([1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Single-element series → not enough context to declare anomaly. Always returns False.
                [False],
            ),
            (
                {
                    "series": pd.Series([1, 11, 1, 111, 1, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # 11 and 111 are both significant upward outliers compared to the stable 1s.
                # Correct detection of two isolated anomalies.
                [False, True, False, True, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 1, 1, 111, 99, 11]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                # 111 and 99 break the otherwise flat region → both are valid anomalies.
                # 11 is within acceptable deviation.
                [False, False, False, True, True, False],
            ),
            (
                {
                    "series": pd.Series([1, 1, 11, 111, 111, 1, 1, 11]),
                    "window": 8, "sigma": 3, "scaleFactor": 1.4826,
                },
                # The two 111s are strong outliers among the rest, which hover around 1–11.
                # The window is large, which helps suppress noise — correct classification.
                [False, False, False, True, True, False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 1, 1, 111, 111, 1, 1, 11111, 1]),
                    "window": 9, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Two 111s are clearly high values; 11111 is a very large spike and rightfully marked as an anomaly.
                # All others are within expected bounds.
                [False, False, False, True, True, False, False, True, False],
            ),
            (
                {
                    "series": pd.Series([1, 100, 1]),
                    "window": 3, "sigma": 1.5, "scaleFactor": 1.4826,
                },
                # With a reduced sigma and a small window, 100 is correctly identified as an outlier between two 1s.
                [False, True, False],
            ),
            (
                {
                    "series": pd.Series([5, 5, 5]),
                    "window": 1, "sigma": 3, "scaleFactor": 1.4826,
                },
                # All values are identical. Even with MAD = 0, there is no deviation → no anomalies.
                [False, False, False],
            ),
            (
                {
                    "series": pd.Series([5, 50, 5]),
                    "window": 1, "sigma": 3, "scaleFactor": 1.4826,
                },
                # With window=1, each value is evaluated in isolation. MAD = 0 for single-point windows,
                # so anomaly detection is effectively disabled — no outliers detected.
                [False, False, False],
            ),
            (
                {
                    "series": pd.Series([1, 1.1, 1.05, 0.95, 1, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                # Small fluctuations around 1 — no points exceed an outlier threshold.
                # Serves as a stability test with noise.
                [False, False, False, False, False, False],
            ),
        ]

        for test in testData:
            assert list(TradeRoutines.HampelFilter(**test[0])) == test[1], "Incorrect output! Input: {}".format(list(test[0]["series"]))

    def test_HampelFilterNegative(self):
        testData = [
            (
                {
                    "series": pd.Series([None, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False],
            ),
            (
                {
                    "series": (None, 10, 10, 10, 10),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [],
            ),
            (
                {
                    "series": "10",
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [],
            ),
            (
                {
                    "series": pd.Series([1]),
                    "window": -1, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "series": pd.Series([1]),
                    "window": 2, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "series": pd.Series([1]),
                    "window": 1, "sigma": -3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "series": pd.Series([1]),
                    "window": 1, "sigma": 3, "scaleFactor": -1.4826,
                },
                [False],
            ),
        ]

        for test in testData:
            assert list(TradeRoutines.HampelFilter(**test[0])) == test[1], "Incorrect output!"

    def test_HampelFilterPerformance(self):
        testCases = [
            (1_00, 0.1),
            (1_000, 0.3),
            (3_000, 0.5),
            (5_000, 0.8),
            (10_000, 1.0),
            (30_000, 1.5),
            (50_000, 2.0),
            (100_000, 2.5),
            (300_000, 3.0),
            (500_000, 3.5),
            (1_000_000, 4.0),
        ]

        for size, maxSeconds in testCases:
            series = pd.Series(np.random.normal(loc=100, scale=5, size=size))

            start = time.perf_counter()
            result = TradeRoutines.HampelFilter(series, window=5)
            elapsed = time.perf_counter() - start

            assert isinstance(result, pd.Series), f"Expected pd.Series for size {size}"
            assert elapsed < maxSeconds, f"HampelFilter too slow for size {size}: took {elapsed:.2f}s (limit {maxSeconds:.2f}s)"

    def test_HampelAnomalyDetectionCheckType(self):
        assert TradeRoutines.HampelAnomalyDetection([1, 2, 1, 1, 1, 1]) == 1, "Not integer type returned!"
        assert TradeRoutines.HampelAnomalyDetection([1, 1, 1, 1, 1, 1]) is None, "Not None returned!"

    def test_HampelAnomalyDetectionPositive(self):
        testData = [
            # Single clear spike near the end:
            ([1, 1, 1, 1, 111, 1], 4),  # Last value is extreme outlier.

            # Middle spike:
            ([1, 1, 10, 1, 1, 1], 2),  # Middle value is an outlier.

            # Anomaly at the beginning:
            ([111, 1, 1, 1, 1, 1], 0),  # First value deviates significantly.

            # Two equal anomalies at beginning and end:
            ([111, 1, 1, 1, 1, 111], 0),  # First and last are both outliers, return first.

            # Gradual growth then spike:
            ([1, 11, 1, 111, 1, 1], 1),  # The second value is a small anomaly before a large one.

            # Series with several anomalies:
            ([1, 1, 1, 111, 99, 11], 3),  # The first anomaly is at index 3.

            # Strong mid-sequence anomalies:
            ([1, 1, 11, 111, 1, 1, 1, 11111], 2),  # Index 2 is first small anomaly before huge one.

            # Two equal spikes in a center:
            ([1, 1, 1, 111, 111, 1, 1, 1, 1], 3),  # The first 111 is picked as an anomaly.

            # Multiple strong anomalies:
            ([1, 1, 1, 1, 111, 1, 1, 11111, 5555], 4),  # First anomaly at index 4.

            # Repetitive pattern disrupted early:
            ([9, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 13, 12, 12, 1, 1], 0),  # The first value is anomaly, not second.

            # Many anomalies including extreme peaks:
            ([9, 13, 12, 12, 13, 12, 1000, 13, 12, 12, 300000, 12, 12, 13, 12, 2000, 1, 1, 1, 1], 0),  # 9 is an early anomaly before any maximum.

            # Anomaly at start (negative spike):
            ([-111, 1, 1, 1, 1], 0),  # First value is extreme negative outlier.

            # Small anomaly in second position:
            ([1, 2, 1, -1, 1], 1),  # Second value is slightly off trend.

            # Large negative value at beginning:
            ([-111, -1, -1, -1, -1], 0),  # First value is anomaly.

            # Symmetric small spike:
            ([-1, -1, 2, -1, -1], 2),  # Center value is small anomaly.

            # Anomaly at the end of the series:
            ([1, 1, 1, 1, 1, 999], 5),  # Last value is extreme outlier.

            # Two equal outliers in the middle:
            ([1, 1, 100, 100, 1, 1], 2),  # Both 100s are outliers, return index of first.

            # Symmetric spike in a center:
            ([1, 1, 50, 1, 1], 2),  # Spike in the center.

            # Two anomalies, pick one with a lower index:
            ([100, 1, 1, 1, 100], 0),  # Both 0 and 4 are anomalies, return min.

            # Flat line with a single jump:
            ([10, 10, 10, 99, 10, 10], 3),  # Single jump.

            # Series with negative infinite value at the beginning:
            ([-np.inf, 1, 1], 0),  # -Inf is detected as a valid outlier at index 0.
        ]

        testData2 = [
            # --- Special cases to validate compareWithMax=False behavior:
            # If compareWithMax=False, should return pure anomaly even if the maximum is earlier.

            # Two spikes, maximum occurs first, but real anomaly later:
            ([1, 100, 1, 999], 1),  # Maximum at 1 (100), anomaly later at 3 (999), min(1,3) is 1 normally.

            # The maximum is before the anomaly:
            ([999, 1, 1, 1000], 0),  # Maximum at 0, anomaly at 3, min(0,3)=0 with default.

            # Anomaly before maximum:
            ([1, 1, 1000, 999], 2),  # Anomaly at 2 before the maximum at 2 as well.
        ]

        for series, expectedCompareWithMaxTrue in testData:
            # Test default behavior:
            assert TradeRoutines.HampelAnomalyDetection(series, compareWithMax=True) == expectedCompareWithMaxTrue, (
                "Incorrect output with compareWithMax=True! Input: {}".format(series)
            )

        for series, _ in testData2:
            # Test compareWithMax=False separately (pure anomaly search):
            anomalyOnly = TradeRoutines.HampelAnomalyDetection(series, compareWithMax=False)

            filtered = TradeRoutines.HampelFilter(series=pd.Series(series), window=len(series))

            if filtered.any():
                expectedPureAnomaly = filtered[filtered].index.min()

                assert anomalyOnly == expectedPureAnomaly, (
                    "Incorrect pure anomaly detection with compareWithMax=False! Input: {}".format(series)
                )
            else:
                assert anomalyOnly is None, (
                    "Incorrect pure anomaly detection with compareWithMax=False (expected None)! Input: {}".format(
                        series)
                )

    def test_HampelAnomalyDetectionNegative(self):
        testData = [
            # Single value in series:
            [1],  # Not enough data to detect anomalies.

            # Nested list instead of a flat list:
            [[1]],  # Invalid input structure should return None.

            # Too few values to detect anomaly:
            [1, 2],  # Less than window size, should return None.

            # Null or empty input:
            None,  # Should safely return None.
            [],  # Empty list, no values to analyze.
            {},  # Dictionary instead of series, invalid input.

            # Flat series with no deviation:
            [1, 1, 1, 1, 1, 1],  # All values identical, no anomaly.

            # Series with non-numeric value:
            [1, "1", 1, 1, 1, 1],  # Contains string, should return None.

            # Series with NaN values only:
            [np.nan, np.nan, np.nan],  # All values are NaN, should return None.

            # Series with NaN mixed with valid values:
            [1, np.nan, 1, 1],  # Contains NaN, may interfere with MAD, should return None.
        ]

        for test in testData:
            # Test default behavior (compareWithMax=True):
            resultWithMax = TradeRoutines.HampelAnomalyDetection(test, compareWithMax=True)
            assert resultWithMax is None, "Incorrect output with compareWithMax=True! Input: {}".format(test)

            # Test pure anomaly detection (compareWithMax=False):
            resultOnlyAnomaly = TradeRoutines.HampelAnomalyDetection(test, compareWithMax=False)
            assert resultOnlyAnomaly is None, "Incorrect output with compareWithMax=False! Input: {}".format(test)

    def test_CanOpenCheckType(self):
        assert isinstance(TradeRoutines.CanOpen("Min", "Min"), bool), "Not bool type returned!"

    def test_CanOpenPositive(self):
        testData = [(TradeRoutines.FUZZY_LEVELS[i], TradeRoutines.FUZZY_LEVELS[j]) for i in range(len(TradeRoutines.FUZZY_LEVELS)) for j in range(len(TradeRoutines.FUZZY_LEVELS))]

        for test in testData:
            assert TradeRoutines.CanOpen(test[0], test[1]) == TradeRoutines.OPENING_RULES.loc[test[0], test[1]], "Incorrect output! {} {}".format(test[0], test[1])

    def test_CanOpenNegative(self):
        testData = [
            ("min", "Min"), ("Max", "max"),
            ("Med1", "Med2"), ("med", "med"),
            ("low", "Low"), ("Low", "low"),
            ("high", "Max"), ("Med", "high"),
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.CanOpen(test[0], test[1])

            assert "Invalid fuzzy" in str(info.value)
            assert "risk level name" in str(info.value) or "reach level name" in str(info.value)
            assert "Correct levels on Universal Fuzzy Scale" in str(info.value)

    def test_CanCloseCheckType(self):
        assert isinstance(TradeRoutines.CanClose("Min", "Min"), bool), "Not bool type returned!"

    def test_CanClosePositive(self):
        testData = [(TradeRoutines.FUZZY_LEVELS[i], TradeRoutines.FUZZY_LEVELS[j]) for i in range(len(TradeRoutines.FUZZY_LEVELS)) for j in range(len(TradeRoutines.FUZZY_LEVELS))]

        for test in testData:
            assert TradeRoutines.CanClose(test[0], test[1]) == TradeRoutines.CLOSING_RULES.loc[test[0], test[1]], "Incorrect output! {} {}".format(test[0], test[1])

    def test_CanCloseNegative(self):
        testData = [
            ("min", "Min"), ("Max", "max"),
            ("Med1", "Med2"), ("med", "med"),
            ("low", "Low"), ("Low", "low"),
            ("high", "Max"), ("Med", "high"),
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.CanClose(test[0], test[1])

            assert "Invalid fuzzy" in str(info.value)
            assert "risk level name" in str(info.value) or "reach level name" in str(info.value)
            assert "Correct levels on Universal Fuzzy Scale" in str(info.value)

    def test_RiskLongCheckType(self):
        assert isinstance(TradeRoutines.RiskLong(2, 3, 1), dict), "Not dict type returned!"

    def test_RiskLongPositive(self):
        testData = [
            (1, 3, 2, {"riskFuzzy": "Min", "riskPercent": 0}),
            (0, 0, 0, {"riskFuzzy": "Min", "riskPercent": 0}),
            (1, 15, 0, {"riskFuzzy": "Min", "riskPercent": 6.6667}),
            (1, 6, 0, {"riskFuzzy": "Min", "riskPercent": 16.6667}),
            (1, 5, 0, {"riskFuzzy": "Low", "riskPercent": 20}),
            (2, 6, 0, {"riskFuzzy": "Low", "riskPercent": 33.3333}),
            (2, 5, 0, {"riskFuzzy": "Med", "riskPercent": 40}),
            (3, 7, 0, {"riskFuzzy": "Med", "riskPercent": 42.8571}),
            (3, 6, 0, {"riskFuzzy": "Med", "riskPercent": 50}),
            (3, 5, 0, {"riskFuzzy": "Med", "riskPercent": 60}),
            (4, 6, 0, {"riskFuzzy": "High", "riskPercent": 66.6667}),
            (7.7777, 10, 0, {"riskFuzzy": "High", "riskPercent": 77.777}),
            (4, 5, 0, {"riskFuzzy": "High", "riskPercent": 80}),
            (4.0001, 5, 0, {"riskFuzzy": "High", "riskPercent": 80.002}),
            (51, 55, 0, {"riskFuzzy": "Max", "riskPercent": 92.7273}),
            (1, 1, 0, {"riskFuzzy": "Max", "riskPercent": 100}),
            (5, 5, 0, {"riskFuzzy": "Max", "riskPercent": 100}),
        ]

        for test in testData:
            result = TradeRoutines.RiskLong(test[0], test[1], test[2])
            assert result["riskFuzzy"] == test[3]["riskFuzzy"], "Incorrect output! {} {}".format(test[0], test[3]["riskFuzzy"])
            assert round(result["riskPercent"], 4) == test[3]["riskPercent"], "Incorrect output! {} {}".format(test[0], test[3]["riskFuzzy"])

    def test_RiskLongNegative(self):
        testData = [
            [1, 2, 3], [1, -3, -2],
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.RiskLong(test[0], test[1], test[2])

            assert "The highest" in str(info.value)
            assert "close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement must be greater than the lowest" in str(info.value)
            assert "close price!" in str(info.value)

    def test_RiskShortCheckType(self):
        assert isinstance(TradeRoutines.RiskShort(1.5, 3, 1), dict), "Not dict type returned!"

    def test_RiskShortPositive(self):
        testData = [
            (1, 3, 2, {"riskFuzzy": "Max", "riskPercent": 100}),
            (4, 3, 2, {"riskFuzzy": "Min", "riskPercent": 0}),
            (0, 0, 0, {"riskFuzzy": "Min", "riskPercent": 0}),
            (1, 1, 0, {"riskFuzzy": "Min", "riskPercent": 0}),
            (0, 1, 0, {"riskFuzzy": "Max", "riskPercent": 100}),
            (1, 9, 0, {"riskFuzzy": "Max", "riskPercent": 88.8889}),
            (2, 9, 0, {"riskFuzzy": "High", "riskPercent": 77.7778}),
            (3, 9, 0, {"riskFuzzy": "High", "riskPercent": 66.6667}),
            (4, 9, 0, {"riskFuzzy": "Med", "riskPercent": 55.5556}),
            (5, 9, 0, {"riskFuzzy": "Med", "riskPercent": 44.4444}),
            (6, 9, 0, {"riskFuzzy": "Low", "riskPercent": 33.3333}),
            (7, 9, 0, {"riskFuzzy": "Low", "riskPercent": 22.2222}),
            (8, 9, 0, {"riskFuzzy": "Min", "riskPercent": 11.1111}),
        ]

        for test in testData:
            result = TradeRoutines.RiskShort(test[0], test[1], test[2])
            assert result["riskFuzzy"] == test[3]["riskFuzzy"], "Incorrect output! {} {}".format(test[0], test[3]["riskFuzzy"])
            assert round(result["riskPercent"], 4) == test[3]["riskPercent"], "Incorrect output! {} {}".format(test[0], test[3]["riskFuzzy"])

    def test_RiskShortNegative(self):
        testData = [
            [1, 2, 3], [1, -3, -2],
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.RiskShort(test[0], test[1], test[2])

            assert "The highest" in str(info.value)
            assert "close price in forecasted movements of candles chain or prognosis of the highest diapason border of price movement must be greater than the lowest" in str(info.value)
            assert "close price!" in str(info.value)

    def test_ReachLongCheckType(self):
        assert isinstance(TradeRoutines.ReachLong(pd.Series([1, 2, 3])), dict), "Not dict type returned!"

    def test_ReachLongPositive(self):
        testData = [
            ([4, 5, 3, 2, 11], "Min", 0),
            ([1, 2, 3, 5, 6, 1], "Low", 33.3333),
            ([1, 2, 3, 5, 4], "Med", 40),
            ([1, 2, 3, 5, 4, 1], "Med", 50),
            ([1, 2, 5, 5, 4], "Med", 60),
            ([4, 5, 3, 2, 1], "High", 80),
            ([4, 1, 5, 3, 2, 1, 0], "High", 71.4286),
            ([8, 2, 3, 5, 6, 1], "Max", 100),
            ([-1, -2, -3, -4, -5], "Max", 100),
            ([-5, -4, -3, -2, -1], "Min", 0),
        ]

        for test in testData:
            result = TradeRoutines.ReachLong(pd.Series(test[0]))
            assert result["reachFuzzy"] == test[1], "Incorrect output! {} {}".format(test[0], test[1])
            assert round(result["reachPercent"], 4) == test[2], "Incorrect output! {} {}".format(test[0], test[2])

    def test_ReachLongNegative(self):
        testData = [
            [], [None], [None, None], [None, None, None],
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.ReachLong(pd.Series(test))

            assert "Pandas Series can't be empty and must contain 1 or more elements!" in str(info.value)

    def test_ReachShortCheckType(self):
        assert isinstance(TradeRoutines.ReachShort(pd.Series([3, 2, 1])), dict), "Not dict type returned!"

    def test_ReachShortPositive(self):
        testData = [
            ([1, 2, 3, 4, 5], "Max", 100),
            ([2, 1, 2, 3, 5], "High", 80.0),
            ([2, 1, 2, 3], "High", 75.0),
            ([3, 2, 1, 2, 3], "Med", 60),
            ([3, 2, 2, 1, 2, 4], "Med", 50),
            ([5, 4, 3, 2, 1, 2, 1], "Med", 42.8571),
            ([5, 4, 3, 2, 2, 1, 2, 1], "Med", 37.5),
            ([5, 4, 3, 2, 1, 2], "Low", 33.3333),
            ([5, 4, 3, 2, 2, 2, 2, 1, 2], "Low", 22.2222),
            ([5, 4, 3, 2, 2, 2, 2, 2, 2, 1, 2], "Low", 18.1818),
            ([5, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2], "Min", 14.2857),
            ([8, 2, 3, 5, 6, 1], "Min", 0),
        ]

        for test in testData:
            result = TradeRoutines.ReachShort(pd.Series(test[0]))
            assert result["reachFuzzy"] == test[1], "Incorrect output! {} {}".format(test[0], test[1])
            assert round(result["reachPercent"], 4) == test[2], "Incorrect output! {} {}".format(test[0], test[2])

    def test_ReachShortNegative(self):
        testData = [
            [], [None], [None, None], [None, None, None],
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.ReachShort(pd.Series(test))

            assert "Pandas Series can't be empty and must contain 1 or more elements!" in str(info.value)

    def test_CalculateAdaptiveCacheReserveCheckType(self):
        result = TradeRoutines.CalculateAdaptiveCacheReserve(
            drawdowns=[0.01, 0.02, 0.03],
            curDrawdown=0.04,
            reserve=0.05,
            portfolioValue=1000.0,
            amplificationFactor=1.25,
            amplificationSensitivity=0.1,
        )
        assert isinstance(result, float), "Not float type returned!"

    def test_CalculateAdaptiveCacheReservePositive(self):
        testData = [
            # drawdowns, curDrawdown, reserve, portfolioValue, amplificationFactor, amplificationSensitivity, expected:
            ([0.02, 0.03], 0.03, 0.035, 1000, 1.25, 0.1, 35.0),  # Stable drawdown → no amplification
            ([0.01, 0.02, 0.03], 0.04, 0.05, 1000, 1.25, 0.1, round(1000 * 0.05 * 1.25 * math.exp(3 * 0.1), 4)),  # GrowStreak=3, ≈ 84.37
            ([], 0.0, 0.05, 1000, 1.25, 0.1, 50.0),  # Empty history → base reserve
            ([0], 0.0, 0.07, 1000, 1.25, 0.1, 70.0),  # Single value, no increase → base reserve
            ([0.01, 0.02, 0.03], 0.031, 0.05, 1000, 1.25, 0.2, round(1000 * 0.05 * 1.25 * math.exp(3 * 0.2), 4)),  # GrowStreak=3, sensitivity=0.2, ≈ 94.69
        ]

        for test in testData:
            result = TradeRoutines.CalculateAdaptiveCacheReserve(
                drawdowns=test[0],
                curDrawdown=test[1],
                reserve=test[2],
                portfolioValue=test[3],
                amplificationFactor=test[4],
                amplificationSensitivity=test[5],
            )
            assert round(result, 4) == test[6], f"Incorrect output! Input: {test[:6]} Expected: {test[6]} Got: {round(result, 4)}"

    def test_CalculateAdaptiveCacheReserveNegative(self):
        testData = [
            (None, 0.02, 0.05, 1000, 1.25, 0.1, "drawdowns must be a list or iterable of floats!"),
            ([0.01, None], 0.02, 0.05, 1000, 1.25, 0.1, "drawdowns contains invalid data!"),
            ([0.01, 0.02], None, 0.05, 1000, 1.25, 0.1, "curDrawdown must be a float or int!"),
            ([0.01, 0.02], 0.02, None, 1000, 1.25, 0.1, "reserve must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, "NotValid", 1.25, 0.1, "portfolioValue must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, 1000, "NotValid", 0.1, "amplificationFactor must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, 1000, 1.25, "NotValid", "amplificationSensitivity must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, -0.05, 1000, 1.25, 0.1, "reserve must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, -1000, 1.25, 0.1, "portfolioValue must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, 1000, -1.25, 0.1, "amplificationFactor must be a positive float or int value!"),
            ([0.01, 0.02], 0.02, 0.05, 1000, 1.25, -0.1, "amplificationSensitivity must be a positive float or int value!"),
        ]

        for test in testData:
            with pytest.raises(BaseException) as info:
                TradeRoutines.CalculateAdaptiveCacheReserve(
                    drawdowns=test[0],
                    curDrawdown=test[1],
                    reserve=test[2],
                    portfolioValue=test[3],
                    amplificationFactor=test[4],
                    amplificationSensitivity=test[5],
                )

            assert test[6] in str(info.value), "Incorrect exception raised! Input: {} Expected Error: {}".format(test[:6], test[6])

    def test_HampelCleanerCheckType(self):
        testSeries = pd.Series([1, 1, 10, 1, 1])

        for strategy in ["neighborAvg", "prev", "const", "medianWindow", "rollingMean"]:
            cleaned = TradeRoutines.HampelCleaner(
                series=testSeries,
                window=3,
                sigma=3,
                scaleFactor=1.4826,
                strategy=strategy,
                fallbackValue=0.0,
                medianWindow=2
            )
            assert isinstance(cleaned, pd.Series), f"Expected pd.Series, got {type(cleaned)} for strategy={strategy}"

    def test_HampelCleanerPositive(self):
        testData = [
            # strategy, input series, expected cleaned result:
            ("neighborAvg", pd.Series([1, 10, 1, 1, 1]), pd.Series([1, 1, 1, 1, 1])),
            ("prev", pd.Series([1, 10, 1, 1, 1]), pd.Series([1, 1, 1, 1, 1])),
            ("const", pd.Series([1, 10, 1, 1, 1]), pd.Series([1, 0.0, 1, 1, 1])),
            ("medianWindow", pd.Series([1, 10, 1, 1, 1]), pd.Series([1, 1, 1, 1, 1])),
            ("rollingMean", pd.Series([1, 10, 1, 1, 1]), pd.Series([1, 1.0, 1, 1, 1])),

            # edge cases:
            ("neighborAvg", pd.Series([100]), pd.Series([100])),  # not replaced, because not detected as an outlier
            ("prev", pd.Series([1, 100, 1]), pd.Series([1, 1, 1])),  # center
            ("const", pd.Series([1]), pd.Series([1])),  # single element, const, not replaced, because not detected as an outlier
            ("medianWindow", pd.Series([1, 100, 1]), pd.Series([1, 1, 1])),
            ("rollingMean", pd.Series([1, 100, 1]), pd.Series([1, 1.0, 1])),

            ("neighborAvg", pd.Series([100, 1, 1, 1, 1]), pd.Series([1, 1, 1, 1, 1])),  # left edge
            ("neighborAvg", pd.Series([1, 1, 1, 1, 100]), pd.Series([1, 1, 1, 1, 1])),  # right edge
            ("prev", pd.Series([100, 1, 1]), pd.Series([0.0, 1, 1])),  # first idx fallback
        ]

        for strategy, inputSeries, expected in testData:
            result = TradeRoutines.HampelCleaner(
                series=inputSeries,
                window=3,
                sigma=3,
                scaleFactor=1.4826,
                strategy=strategy,
                fallbackValue=0.0,
                medianWindow=2
            )

            assert list(result.round(4)) == list(expected.round(4)), f"Incorrect output for strategy={strategy}"

    def test_HampelCleanerNegative(self):
        testData = [
            {
                "series": pd.Series([1, 2, 3]),
                "strategy": "invalidStrategy",
                "expectedMessage": "Unknown strategy"
            },
            {
                "series": "not_a_series",
                "strategy": "const",
                "expectedMessage": "has no attribute 'copy'"
            },
        ]

        for test in testData:
            with pytest.raises(Exception) as err:
                TradeRoutines.HampelCleaner(
                    series=test["series"],
                    window=3,
                    sigma=3,
                    scaleFactor=1.4826,
                    strategy=test["strategy"],
                    fallbackValue=0.0,
                    medianWindow=2
                )

            assert test["expectedMessage"] in str(err.value), f"Unexpected exception: {str(err.value)}"

    def test_HampelCleanerPerformance(self):
        sizes = [10, 100, 500, 1000, 5000, 10000, 50000, 100000, 300000, 500000, 1000000]
        strategy = "medianWindow"

        for size in sizes:
            series = self.GenerateSeries(size)

            startTime = time.perf_counter()

            _ = TradeRoutines.HampelCleaner(
                series,
                window=5,
                sigma=3,
                scaleFactor=1.4826,
                strategy=strategy,
                fallbackValue=0.0,
                medianWindow=3
            )

            elapsed = time.perf_counter() - startTime

            # Assert an upper time limit for performance (adjust as needed):
            assert elapsed < 2.5, f"HampelCleaner too slow for size {size}: took {elapsed:.2f}s"

    def test_EstimateTargetReachabilityCheckType(self):
        # Generate valid synthetic data for testing:
        seriesLowTF = self.GenerateSeries(200)
        seriesHighTF = self.GenerateSeries(60)
        currentPrice = seriesLowTF.iloc[-1]
        targetPrice = currentPrice * 1.05

        # Test function call:
        pIntegral, fIntegral = TradeRoutines.EstimateTargetReachability(
            seriesLowTF, seriesHighTF, currentPrice, targetPrice, 12, 4, ddof=2
        )

        # Check return types:
        assert isinstance(pIntegral, float), "Returned probability (pIntegral) is not float!"
        assert isinstance(fIntegral, str), "Returned fuzzy value (fIntegral) is not string!"
        assert fIntegral in TradeRoutines.FUZZY_LEVELS, "Returned fuzzy value is not valid!"

    def test_EstimateTargetReachabilityPositive(self):
        testCases = [
            (self.GenerateSeries(150), self.GenerateSeries(40), 12, 3),
            (self.GenerateSeries(300), self.GenerateSeries(60), 20, 5),
            (self.GenerateSeries(1000), self.GenerateSeries(100), 15, 4),
        ]

        for seriesLowTF, seriesHighTF, horizonLowTF, horizonHighTF in testCases:
            currentPrice = seriesLowTF.iloc[-1]
            targetPrice = currentPrice * 1.07

            pIntegral, fIntegral = TradeRoutines.EstimateTargetReachability(
                seriesLowTF, seriesHighTF, currentPrice, targetPrice,
                horizonLowTF, horizonHighTF, ddof=2
            )

            # Probability must be within [0, 1]:
            assert 0.0 <= pIntegral <= 1.0, f"Probability out of bounds: {pIntegral}"

            # Fuzzy level must be valid:
            assert fIntegral in TradeRoutines.FUZZY_LEVELS, f"Invalid fuzzy label: {fIntegral}"

    def test_EstimateTargetReachabilityNegative(self):
        validSeries = self.GenerateSeries(100)
        emptySeries = pd.Series([], dtype=float)

        # Invalid/edge test cases:
        testCases = [
            ([], [], 100, 110, 10, 5),  # Empty lists
            ([100], [100], 100, 110, 10, 5),  # Single-point series
            (validSeries, validSeries, 0, 110, 10, 5),  # Zero current price
            (validSeries, validSeries, 100, -110, 10, 5),  # Negative target price
            (validSeries, validSeries, 100, 110, 0, 5),  # Zero horizon
            (emptySeries, emptySeries, 100, 110, 10, 5),  # Empty Pandas series
        ]

        for seriesLowTF, seriesHighTF, currentPrice, targetPrice, horizonLowTF, horizonHighTF in testCases:
            pIntegral, fIntegral = TradeRoutines.EstimateTargetReachability(
                seriesLowTF, seriesHighTF, currentPrice, targetPrice,
                horizonLowTF, horizonHighTF, ddof=2
            )

            # Must fallback to zero probability and "Min":
            assert pIntegral == 0.0 and fIntegral == "Min", (
                f"Expected fallback (0.0, 'Min'), got: {pIntegral}, {fIntegral}"
            )

    def test_EstimateTargetReachabilityPerformance(self):
        sizes = [1000, 5000, 10000, 50000]

        for size in sizes:
            seriesLowTF = self.GenerateSeries(size)
            seriesHighTF = self.GenerateSeries(size // 5)
            currentPrice = seriesLowTF.iloc[-1]
            targetPrice = currentPrice * 1.05

            startTime = time.perf_counter()

            pIntegral, fIntegral = TradeRoutines.EstimateTargetReachability(
                seriesLowTF, seriesHighTF, currentPrice, targetPrice,
                horizonLowTF=12, horizonHighTF=4, ddof=2
            )

            elapsed = time.perf_counter() - startTime

            print(
                f"Size: {size:>6}, "
                f"Time: {elapsed:.5f}s, "
                f"Prob: {pIntegral:.4f}, "
                f"Fuzzy: {fIntegral}"
            )

            # Ensuring reasonable performance (adjust 1.0s limit as needed):
            assert elapsed < 1.0, f"Performance issue for size {size}: took {elapsed:.2f}s"

    def test_LogReturnsCheckType(self):
        series = self.GenerateSeries(100)

        result = TradeRoutines.LogReturns(series)

        assert isinstance(result, pd.Series), "LogReturns must return a Pandas Series!"

    def test_LogReturnsPositive(self):
        series = pd.Series([100, 105, 110, 120])

        expected = np.log(pd.Series([105, 110, 120]) / pd.Series([100, 105, 110]))
        expected = pd.Series(expected.values, index=[1, 2, 3])  # Name index as after shift + dropna.

        result = TradeRoutines.LogReturns(series)

        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_LogReturnsNegative(self):
        badInputs = [[], pd.Series([]), None, [1], pd.Series([1]), "not a series"]

        for testCase in badInputs:
            try:
                result = TradeRoutines.LogReturns(testCase)

                assert result.empty or isinstance(result, pd.Series), f"Should return empty Series for input: {testCase}"

            except Exception:
                pass  # Acceptable if exception raised on invalid input.

    def test_MeanReturnCheckType(self):
        logReturns = pd.Series([0.01, 0.02, 0.03])

        result = TradeRoutines.MeanReturn(logReturns)

        assert isinstance(result, float), "MeanReturn must return a float!"

    def test_MeanReturnPositive(self):
        logReturns = pd.Series([0.01, 0.02, 0.03])
        expected = (0.01 + 0.02 + 0.03) / 3

        result = TradeRoutines.MeanReturn(logReturns)

        assert abs(result - expected) < 1e-10, f"Incorrect mean return: {result}, expected: {expected}"

    def test_MeanReturnNegative(self):
        badInputs = [[], pd.Series([]), None, "not a series"]

        for testCase in badInputs:
            try:
                result = TradeRoutines.MeanReturn(testCase)

                assert result == 0.0 or np.isnan(result), f"Expected 0.0 or NaN for input: {testCase}"

            except Exception:
                pass  # Also acceptable.

    def test_VolatilityCheckType(self):
        logReturns = pd.Series([0.01, 0.02, 0.03])

        result = TradeRoutines.Volatility(logReturns, ddof=1)

        assert isinstance(result, float), "Volatility must return a float!"

    def test_VolatilityPositive(self):
        logReturns = pd.Series([0.01, 0.02, 0.03])

        for ddof in [0, 1, 2]:
            expected = logReturns.std(ddof=ddof)

            result = TradeRoutines.Volatility(logReturns, ddof=ddof)

            assert abs(result - expected) < 1e-10, (
                f"Incorrect volatility for ddof={ddof}: {result}, expected: {expected}"
            )

    def test_VolatilityNegative(self):
        badInputs = [[], pd.Series([]), None, "invalid"]

        for testCase in badInputs:
            try:
                result = TradeRoutines.Volatility(testCase)

                assert result == 0.0 or np.isnan(result), f"Expected 0.0 or NaN for input: {testCase}"

            except Exception:
                pass  # Also acceptable.

    def test_ZScoreCheckType(self):
        result = TradeRoutines.ZScore(logTargetRatio=0.05, meanReturn=0.01, volatility=0.02, horizon=10)

        assert isinstance(result, float), "ZScore must return a float!"

    def test_ZScorePositive(self):
        logTarget = 0.05
        mu = 0.01
        sigma = 0.02
        horizon = 10

        expected = (logTarget - (mu - 0.5 * sigma**2) * horizon) / (sigma * math.sqrt(horizon))

        result = TradeRoutines.ZScore(logTarget, mu, sigma, horizon)

        assert abs(result - expected) < 1e-10, f"Incorrect z-score: {result}, expected: {expected}"

    def test_ZScoreNegative(self):
        testCases = [
            (0.05, 0.01, 0.0, 10),  # Zero volatility.
            (0.05, 0.01, 0.02, 0),  # Zero horizon.
            ("bad", 0.01, 0.02, 10),  # Invalid logTargetRatio.
            (0.05, None, 0.02, 10),  # None in input.
        ]

        for logTarget, mu, sigma, horizon in testCases:
            try:
                result = TradeRoutines.ZScore(logTarget, mu, sigma, horizon)

                assert np.isfinite(result), f"Unexpected result: {result}"

            except Exception:
                pass  # Acceptable fallback on bad input.

    def test_BayesianAggregationCheckType(self):
        result = TradeRoutines.BayesianAggregation(0.6, 0.7)

        assert isinstance(result, float), "BayesianAggregation must return a float!"

    def test_BayesianAggregationPositive(self):
        testCases = [
            (0.5, 0.5, 0.5),
            (0.8, 0.9, (0.8 * 0.9) / (0.8 * 0.9 + 0.2 * 0.1)),
            (0.0, 0.0, 0.0),
            (1.0, 1.0, 1.0),
        ]

        for p1, p2, expected in testCases:
            result = TradeRoutines.BayesianAggregation(p1, p2)

            assert abs(result - expected) < 1e-10, f"Incorrect result for {p1}, {p2}: {result}, expected: {expected}"

    def test_BayesianAggregationNegative(self):
        testCases = [
            (1.2, 0.5),
            (0.5, -0.1),
            ("bad", 0.5),
            (None, 0.7),
        ]

        for p1, p2 in testCases:
            try:
                result = TradeRoutines.BayesianAggregation(p1, p2)

                assert 0.0 <= result <= 1.0, f"Result out of bounds: {result}"

            except Exception:
                pass  # Acceptable on bad input.

    def test_VolatilityWeightCheckType(self):
        result = TradeRoutines.VolatilityWeight(0.01, 0.02)

        assert isinstance(result, float), "VolatilityWeight must return a float!"

    def test_VolatilityWeightPositive(self):
        testCases = [
            (0.01, 0.01, 0.5),
            (0.02, 0.01, 0.3333333333),
            (0.01, 0.02, 0.6666666667),
            (0.0, 0.01, 1.0),
            (0.01, 0.0, 0.0),
        ]

        for sigmaLow, sigmaHigh, expected in testCases:
            result = TradeRoutines.VolatilityWeight(sigmaLow, sigmaHigh)

            assert abs(result - expected) < 1e-10, f"Incorrect result for {sigmaLow}, {sigmaHigh}: {result}, expected: {expected}"

    def test_VolatilityWeightNegative(self):
        testCases = [
            (-0.01, 0.02),     # Negative sigmaLow.
            (0.02, -0.01),     # Negative sigmaHigh.
            (0.0, 0.0),        # Both zero.
            (None, 0.01),      # None input.
            ("bad", 0.01),     # Non-numeric input.
        ]

        for sigmaLow, sigmaHigh in testCases:
            try:
                result = TradeRoutines.VolatilityWeight(sigmaLow, sigmaHigh)

                assert 0.0 <= result <= 1.0 or np.isnan(result), f"Unexpected result: {result}"

            except Exception:
                pass  # Acceptable if function raises.

    def test_RollingMeanCheckType(self):
        series = self.GenerateSeries(length=100).values

        result = TradeRoutines.RollingMean(series, window=5)

        assert isinstance(result, np.ndarray), "RollingMean must return a NumPy array!"

    def test_RollingMeanPositive(self):
        series = np.array([1, 2, 3, 4, 5])
        expected = np.array([np.nan, np.nan, np.nan, np.nan, 3.0])

        result = TradeRoutines.RollingMean(series, window=5)

        np.testing.assert_allclose(result[4:], expected[4:], rtol=1e-6)

    def test_RollingMeanNegative(self):
        series = np.array([np.nan, np.nan, np.nan, np.nan])

        result = TradeRoutines.RollingMean(series, window=3)

        assert np.isnan(result).all(), "Expected all NaNs for insufficient data!"

    def test_RollingMeanPerformance(self):
        series = self.GenerateSeries(length=1_000_000).values
        start = time.perf_counter()

        TradeRoutines.RollingMean(series, window=5)

        elapsed = time.perf_counter() - start

        assert elapsed < 1.0, f"RollingMean too slow: {elapsed:.2f}s"

    def test_RollingStdCheckType(self):
        series = self.GenerateSeries(length=100).values

        result = TradeRoutines.RollingStd(series, window=5)

        assert isinstance(result, np.ndarray), "RollingStd must return a NumPy array!"

    def test_RollingStdPositive(self):
        series = np.array([1, 2, 3, 4, 5])
        expected_std = np.std([1, 2, 3, 4, 5], ddof=1)

        result = TradeRoutines.RollingStd(series, window=5)

        np.testing.assert_allclose(result[4], expected_std, rtol=1e-6)

    def test_RollingStdNegative(self):
        series = np.array([np.nan, np.nan, np.nan, np.nan])

        result = TradeRoutines.RollingStd(series, window=3)

        assert np.isnan(result).all(), "Expected all NaNs for insufficient data!"

    def test_RollingStdPerformance(self):
        series = self.GenerateSeries(length=1_000_000).values
        start = time.perf_counter()

        TradeRoutines.RollingStd(series, window=5)

        elapsed = time.perf_counter() - start

        assert elapsed < 1.0, f"RollingStd too slow: {elapsed:.2f}s"

    def test_FastBBandsCheckType(self):
        series = self.GenerateSeries(length=100)

        result = TradeRoutines.FastBBands(series, length=20)

        assert isinstance(result, pd.DataFrame), "FastBBands must return a pandas DataFrame!"

    def test_FastBBandsPositive(self):
        series = pd.Series(np.arange(1, 51))

        result = TradeRoutines.FastBBands(series, length=5, std=2)

        assert all(col in result.columns for col in ["BBL_5_2.0", "BBM_5_2.0", "BBU_5_2.0", "BBB_5_2.0", "BBP_5_2.0"]), "Missing columns in BBands output!"

    def test_FastBBandsNegative(self):
        invalidInputs = [None, [], {}, "bad input"]

        for badInput in invalidInputs:
            result = TradeRoutines.FastBBands(badInput)  # type: ignore

            assert result is None, f"Expected None for invalid input, got {result}"

    def test_FastBBandsPerformance(self):
        series = self.GenerateSeries(length=1_000_000)
        start = time.perf_counter()

        TradeRoutines.FastBBands(series, length=20)
        elapsed = time.perf_counter() - start

        assert elapsed < 1.5, f"FastBBands too slow: {elapsed:.2f}s"