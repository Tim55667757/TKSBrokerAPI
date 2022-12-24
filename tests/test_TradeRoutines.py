# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from tksbrokerapi import TradeRoutines
import pandas as pd


class UpdateClassFieldsTestClass:

    def __init__(self):
        self.a = "123"
        self.b = 123
        self.c = False


class TestTradeRoutinesMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        pass

    def test_GetDatesAsStringCheckType(self):
        result = TradeRoutines.GetDatesAsString(None, None)

        assert isinstance(result, tuple), "Not tuple type returned!"
        assert isinstance(result[0], str), "Not str type in first parameter returned!"
        assert isinstance(result[1], str), "Not str type in second parameter returned!"

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

    def test_GetDatesAsStringNegative(self):
        testData = [
            (1, 2, ("", "")), ("1", "2", ("", "")),
            ("", "yesterday", ("", "")), ("", None, ("", "")),
            ("2022-12-03", -1, ("", "")), ("2022-12-02-", "2022-12-03-", ("", "")),
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
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=pd.Series([1, 1, 1, 1, 1, 1]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=pd.Series([1]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=pd.Series([]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=pd.Series([1, "1", True, None]), window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=1, window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries="1", window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=True, window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=[1, "1", True], window=3), pd.Series), "Not Pandas Series type returned!"
        assert isinstance(TradeRoutines.HampelFilter(pdSeries=None, window=3), pd.Series), "Not Pandas Series type returned!"

    def test_HampelFilterPositive(self):
        testData = [
            (
                {
                    "pdSeries": pd.Series([10, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 5, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 5, 1, 1, 1]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 5, 1, 1, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 5, 1, 1, 1]),
                    "window": 3, "sigma": 1, "scaleFactor": 1.4826,
                },
                [False, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 5, 1, 1, 1]),
                    "window": 5, "sigma": 3, "scaleFactor": 1,
                },
                [False, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 10, 10, 1, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 10, 10, 10, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, False, False, False, False, True],
            ),
            (
                {
                    "pdSeries": pd.Series([10, 1, 1, 1, 1, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, False, False, False, False, True],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 1, 1, 10, 10, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 1, 1, 1, 10, 10]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, True, True],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 10, 1, 10, 1, 10]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, True, False],
            ),
            (
                {
                    "pdSeries": pd.Series([10, 1, 10, 1, 10, 1]),
                    "window": 3, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, True, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 10, 1, 10, 1, 10]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([10, 1, 10, 1, 10, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([-1, 1, 1, 1, 0, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [True, False, False, False, True, False],
            ),
            (
                {
                    "pdSeries": pd.Series([-1, -1, -1, -1, 0, -1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, True, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 11, 1, 111, 1, 1]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, True, False, True, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 1, 1, 111, 99, 11]),
                    "window": 6, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, True, True, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 1, 11, 111, 111, 1, 1, 11]),
                    "window": 8, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, True, True, False, False, False],
            ),
            (
                {
                    "pdSeries": pd.Series([1, 1, 1, 111, 111, 1, 1, 11111, 1]),
                    "window": 9, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, True, True, False, False, True, False],
            ),
        ]

        for test in testData:
            assert list(TradeRoutines.HampelFilter(**test[0])) == test[1], "Incorrect output!"

    def test_HampelFilterNegative(self):
        testData = [
            (
                {
                    "pdSeries": pd.Series([None, 10, 10, 10, 10]),
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False, False, False, False, False],
            ),
            (
                {
                    "pdSeries": [None, 10, 10, 10, 10],
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [],
            ),
            (
                {
                    "pdSeries": "10",
                    "window": 5, "sigma": 3, "scaleFactor": 1.4826,
                },
                [],
            ),
            (
                {
                    "pdSeries": pd.Series([1]),
                    "window": -1, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "pdSeries": pd.Series([1]),
                    "window": 2, "sigma": 3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "pdSeries": pd.Series([1]),
                    "window": 1, "sigma": -3, "scaleFactor": 1.4826,
                },
                [False],
            ),
            (
                {
                    "pdSeries": pd.Series([1]),
                    "window": 1, "sigma": 3, "scaleFactor": -1.4826,
                },
                [False],
            ),
        ]

        for test in testData:
            assert list(TradeRoutines.HampelFilter(**test[0])) == test[1], "Incorrect output!"

    def test_HampelAnomalyDetectionCheckType(self):
        assert isinstance(TradeRoutines.HampelAnomalyDetection([1, 2, 1, 1, 1, 1]), int), "Not int type returned!"
        assert TradeRoutines.HampelAnomalyDetection([1, 1, 1, 1, 1, 1]) is None, "Not None returned!"

    def test_HampelAnomalyDetectionPositive(self):
        testData = [
            ([1, 1, 1, 1, 111, 1], 4),
            ([1, 1, 10, 1, 1, 1], 2),
            ([111, 1, 1, 1, 1, 1], 0),
            ([111, 1, 1, 1, 1, 111], 0),
            ([1, 11, 1, 111, 1, 1], 1),
            ([1, 1, 1, 111, 99, 11], 3),
            ([1, 1, 11, 111, 1, 1, 1, 11111], 2),
            ([1, 1, 1, 111, 111, 1, 1, 1, 1], 3),
            ([1, 1, 1, 1, 111, 1, 1, 11111, 5555], 4),
            ([9, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 12, 13, 12, 13, 12, 12, 1, 1], 1),
            ([9, 13, 12, 12, 13, 12, 1000, 13, 12, 12, 300000, 12, 12, 13, 12, 2000, 1, 1, 1, 1], 6),
            ([-111, 1, 1, 1, 1], 0),
            ([-111, -1, -1, -1, -1], 0),
            ([-1, -1, 2, -1, -1], 2),
        ]

        for test in testData:
            assert TradeRoutines.HampelAnomalyDetection(test[0]) == test[1], "Incorrect output!"

    def test_HampelAnomalyDetectionNegative(self):
        testData = [
            [1],
            [[1]],
            [1, 2],
            None, [], {},
            [1, 1, 1, 1, 1, 1],
            [1, "1", 1, 1, 1, 1],
        ]

        for test in testData:
            assert TradeRoutines.HampelAnomalyDetection(test) is None, "Incorrect output!"
