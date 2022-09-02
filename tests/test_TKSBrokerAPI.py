# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from datetime import datetime, timedelta
from dateutil.tz import tzutc
import json
from tksbrokerapi import TKSBrokerAPI


class TestTKSBrokerAPIMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        TKSBrokerAPI.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        TKSBrokerAPI.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        TKSBrokerAPI.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt

        # set up default parameters:
        self.testIList = json.load(open("./tests/InstrumentsDump.json", mode="r", encoding="UTF-8"))
        self.server = TKSBrokerAPI.TinkoffBrokerServer(
            token="TKSBrokerAPI_unittest_fake_token",
            iList=self.testIList,
            accountId="TKSBrokerAPI_unittest_fake_accountId",
            useCache=False,
        )

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

    def test_ConsistentOfVariablesNames(self):
        mainVarNames = [
            "token", "accountId", "iList",
            "aliases", "aliasesKeys", "ticker", "figi", "depth", "server", "timeout", "headers", "body",
            "historyFile", "instrumentsFile", "searchResultsFile", "pricesFile", "overviewFile", "reportFile", "iListDumpFile",
        ]
        actualNames = dir(self.server)

        for vName in mainVarNames:
            assert vName in actualNames, "One of main variables changed it's name! Problem is with variable [{}]".format(vName)

    def test__ParseJSONCheckType(self):
        assert isinstance(self.server._ParseJSON(rawData="{}", debug=False), dict), "Not dict type returned!"

    def test__ParseJSONPositive(self):
        testData = [
            ("{}", {}), ('{"x":123}', {"x": 123}), ('{"x":""}', {"x": ""}),
            ('{"abc": "123", "xyz": 123}', {"abc": "123", "xyz": 123}),
            ('{"abc": {"abc": "123", "xyz": 123}}', {"abc": {"abc": "123", "xyz": 123}}),
            ('{"abc": {"abc": "", "xyz": 0}}', {"abc": {"abc": "", "xyz": 0}}),
        ]

        for test in testData:
            result = self.server._ParseJSON(rawData=test[0], debug=False)

            assert result == test[1], 'Expected: `_ParseJSON(rawData="{}", debug=False) == {}`, actual: `{}`'.format(test[0], test[1], result)

    def test_SendAPIRequestCheckType(self):
        self.server.body = {"instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"}

        result = self.server.SendAPIRequest(
            url=self.server.server + r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/Currencies",
            reqType="POST",
            retry=0,
            pause=0,
            debug=False,
        )

        assert isinstance(result, dict), "Not dict type returned!"

    def test_SendAPIRequestPositive(self):
        self.server.body = {"instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"}

        # TODO: want more tests with real responses and real bearer token
        testData = [
            (r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/Currencies", {'code': 3, 'description': None, 'message': None}),
        ]

        for test in testData:
            result = self.server.SendAPIRequest(
                url=self.server.server + r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/Currencies",
                reqType="POST",
                retry=0,
                pause=0,
                debug=False,
            )

            assert result == test[1], 'Expected: `{}`, actual: `{}`'.format(test[1], result)

    def test_ShowInstrumentInfoCheckType(self):
        assert isinstance(self.server.ShowInstrumentInfo(iJSON={}, printInfo=False), str), "Not str type returned!"

    def test_ShowInstrumentInfoPositive(self):
        # TODO: want more positive tests with different instruments
        testData = [
            ({}, ""),
        ]

        for test in testData:
            result = self.server.ShowInstrumentInfo(iJSON=test[0], printInfo=False)

            assert result == test[1], 'Expected: `{}`, actual: `{}`'.format(test[1], result)

    def test_SearchByTickerCheckType(self):
        self.server.ticker = "IBM"
        self.server.figi = ""

        assert isinstance(self.server.SearchByTicker(requestPrice=False, showInfo=False, debug=False), dict), "Not dict type returned!"

    def test_SearchByTickerPositive(self):
        testData = [  # tickers and their corresponding instruments:
            ("IBM", {"figi": "BBG000BLNNH6", "ticker": "IBM", "classCode": "SPBXM", "isin": "US4592001014", "lot": 1, "currency": "usd", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 500000000}, "dshort": {"units": "0", "nano": 500000000}, "dlongMin": {"units": "0", "nano": 292900000}, "dshortMin": {"units": "0", "nano": 224700000}, "shortEnabledFlag": False, "name": "IBM", "exchange": "SPB", "ipoDate": "1915-11-11T00:00:00Z", "issueSize": "896320073", "countryOfRisk": "US", "countryOfRiskName": "Соединенные Штаты Америки", "sector": "it", "issueSizePlan": "4687500000", "nominal": {"currency": "usd", "units": "0", "nano": 200000000}, "tradingStatus": "SECURITY_TRADING_STATUS_NORMAL_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "divYieldFlag": True, "shareType": "SHARE_TYPE_COMMON", "minPriceIncrement": {"units": "0", "nano": 10000000}, "apiTradeAvailableFlag": True, "uid": "ca370ca5-e42b-44e4-a0a5-daf5e51d02a7", "realExchange": "REAL_EXCHANGE_RTS", "positionUid": "b70a8cfc-90c1-4a66-8c39-f6239705b2fe", "forIisFlag": True, "first1minCandleDate": "2018-01-23T08:51:00Z", "first1dayCandleDate": "1988-09-12T00:00:00Z", "type": "Shares", "step": 0.01}),
            ("YNDX", {"figi": "BBG006L8G4H1", "ticker": "YNDX", "classCode": "TQBR", "isin": "NL0009805522", "lot": 1, "currency": "rub", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 521100000}, "dshort": {"units": "0", "nano": 635900000}, "dlongMin": {"units": "0", "nano": 308000000}, "dshortMin": {"units": "0", "nano": 279000000}, "shortEnabledFlag": True, "name": "Yandex", "exchange": "MOEX_WEEKEND", "ipoDate": "2011-05-24T00:00:00Z", "issueSize": "323800479", "countryOfRisk": "RU", "countryOfRiskName": "Российская Федерация", "sector": "telecom", "issueSizePlan": "0", "nominal": {"currency": "eur", "units": "0", "nano": 10000000}, "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "divYieldFlag": False, "shareType": "SHARE_TYPE_COMMON", "minPriceIncrement": {"units": "0", "nano": 200000000}, "apiTradeAvailableFlag": True, "uid": "10e17a87-3bce-4a1f-9dfc-720396f98a3c", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "cb51e157-1f73-4c62-baac-93f11755056a", "forIisFlag": True, "first1minCandleDate": "2018-03-07T18:38:00Z", "first1dayCandleDate": "2014-06-04T07:00:00Z", "type": "Shares", "step": 0.2}),
            ("USD000UTSTOM", {"figi": "BBG0013HGFT4", "ticker": "USD000UTSTOM", "classCode": "CETS", "isin": "", "lot": 1000, "currency": "rub", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 500000000}, "dshort": {"units": "0", "nano": 500000000}, "dlongMin": {"units": "0", "nano": 292900000}, "dshortMin": {"units": "0", "nano": 224700000}, "shortEnabledFlag": True, "name": "Доллар США", "exchange": "FX", "nominal": {"currency": "usd", "units": "1", "nano": 0}, "countryOfRisk": "", "countryOfRiskName": "", "tradingStatus": "SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "isoCurrencyName": "usd", "minPriceIncrement": {"units": "0", "nano": 2500000}, "apiTradeAvailableFlag": True, "uid": "a22a1263-8e1b-4546-a1aa-416463f104d3", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "6e97aa9b-50b6-4738-bce7-17313f2b2cc2", "forIisFlag": True, "first1minCandleDate": "2018-03-07T16:16:00Z", "first1dayCandleDate": "2000-05-16T00:00:00Z", "type": "Currencies", "step": 0.0025}),
            ("RU000A101YV8", {"figi": "TCS00A101YV8", "ticker": "RU000A101YV8", "classCode": "TQCB", "isin": "RU000A101YV8", "lot": 1, "currency": "rub", "shortEnabledFlag": False, "name": "Позитив Текнолоджиз выпуск 1", "exchange": "MOEX_PLUS", "couponQuantityPerYear": 4, "maturityDate": "2023-07-26T00:00:00Z", "nominal": {"currency": "rub", "units": "1000", "nano": 0}, "stateRegDate": "2020-07-21T00:00:00Z", "placementDate": "2020-07-29T00:00:00Z", "placementPrice": {"currency": "rub", "units": "1000", "nano": 0}, "aciValue": {"currency": "rub", "units": "26", "nano": 780000000}, "countryOfRisk": "RU", "countryOfRiskName": "Российская Федерация", "sector": "it", "issueKind": "non_documentary", "issueSize": "500000", "issueSizePlan": "500000", "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "floatingCouponFlag": False, "perpetualFlag": False, "amortizationFlag": True, "minPriceIncrement": {"units": "0", "nano": 10000000}, "apiTradeAvailableFlag": True, "uid": "2ee80fbd-356f-4a01-8d64-d2bd1e73745c", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "0500b20b-1a28-4ed5-bf63-958b16a40080", "forIisFlag": True, "type": "Bonds", "step": 0.01}),
            ("TGLD", {"figi": "BBG222222222", "ticker": "TGLD", "classCode": "TQTD", "isin": "RU000A101X50", "lot": 100, "currency": "usd", "shortEnabledFlag": False, "name": "Тинькофф Золото", "exchange": "MOEX", "fixedCommission": {"units": "0", "nano": 450000000}, "focusType": "equity", "releasedDate": "2020-07-13T00:00:00Z", "countryOfRisk": "", "countryOfRiskName": "", "sector": "", "rebalancingFreq": "", "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "minPriceIncrement": {"units": "0", "nano": 100000}, "apiTradeAvailableFlag": True, "uid": "a4b3adc6-4e04-4f06-9048-431aa1ed07ac", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "548bde28-a5ea-4b7b-83d3-47b4c56a0167", "forIisFlag": True, "first1minCandleDate": "2020-08-26T07:00:00Z", "first1dayCandleDate": "2020-08-26T07:00:00Z", "type": "Etfs", "step": 0.0001}),
        ]

        for test in testData:
            self.server.ticker = test[0]
            self.server.figi = ""

            result = self.server.SearchByTicker(requestPrice=False, showInfo=False, debug=False)

            assert result == test[1], 'Ticker: {}\nExpected: {}\nActual: {}'.format(test[0], test[1], result)

    def test_SearchByFIGICheckType(self):
        self.server.ticker = ""
        self.server.figi = "BBG000BLNNH6"

        assert isinstance(self.server.SearchByFIGI(requestPrice=False, showInfo=False, debug=False), dict), "Not dict type returned!"

    def test_SearchByFIGIPositive(self):
        testData = [  # FIGIs and their corresponding instruments:
            ("BBG000BLNNH6", {"figi": "BBG000BLNNH6", "ticker": "IBM", "classCode": "SPBXM", "isin": "US4592001014", "lot": 1, "currency": "usd", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 500000000}, "dshort": {"units": "0", "nano": 500000000}, "dlongMin": {"units": "0", "nano": 292900000}, "dshortMin": {"units": "0", "nano": 224700000}, "shortEnabledFlag": False, "name": "IBM", "exchange": "SPB", "ipoDate": "1915-11-11T00:00:00Z", "issueSize": "896320073", "countryOfRisk": "US", "countryOfRiskName": "Соединенные Штаты Америки", "sector": "it", "issueSizePlan": "4687500000", "nominal": {"currency": "usd", "units": "0", "nano": 200000000}, "tradingStatus": "SECURITY_TRADING_STATUS_NORMAL_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "divYieldFlag": True, "shareType": "SHARE_TYPE_COMMON", "minPriceIncrement": {"units": "0", "nano": 10000000}, "apiTradeAvailableFlag": True, "uid": "ca370ca5-e42b-44e4-a0a5-daf5e51d02a7", "realExchange": "REAL_EXCHANGE_RTS", "positionUid": "b70a8cfc-90c1-4a66-8c39-f6239705b2fe", "forIisFlag": True, "first1minCandleDate": "2018-01-23T08:51:00Z", "first1dayCandleDate": "1988-09-12T00:00:00Z", "type": "Shares", "step": 0.01}),
            ("BBG006L8G4H1", {"figi": "BBG006L8G4H1", "ticker": "YNDX", "classCode": "TQBR", "isin": "NL0009805522", "lot": 1, "currency": "rub", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 521100000}, "dshort": {"units": "0", "nano": 635900000}, "dlongMin": {"units": "0", "nano": 308000000}, "dshortMin": {"units": "0", "nano": 279000000}, "shortEnabledFlag": True, "name": "Yandex", "exchange": "MOEX_WEEKEND", "ipoDate": "2011-05-24T00:00:00Z", "issueSize": "323800479", "countryOfRisk": "RU", "countryOfRiskName": "Российская Федерация", "sector": "telecom", "issueSizePlan": "0", "nominal": {"currency": "eur", "units": "0", "nano": 10000000}, "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "divYieldFlag": False, "shareType": "SHARE_TYPE_COMMON", "minPriceIncrement": {"units": "0", "nano": 200000000}, "apiTradeAvailableFlag": True, "uid": "10e17a87-3bce-4a1f-9dfc-720396f98a3c", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "cb51e157-1f73-4c62-baac-93f11755056a", "forIisFlag": True, "first1minCandleDate": "2018-03-07T18:38:00Z", "first1dayCandleDate": "2014-06-04T07:00:00Z", "type": "Shares", "step": 0.2}),
            ("BBG0013HGFT4", {"figi": "BBG0013HGFT4", "ticker": "USD000UTSTOM", "classCode": "CETS", "isin": "", "lot": 1000, "currency": "rub", "klong": {"units": "2", "nano": 0}, "kshort": {"units": "2", "nano": 0}, "dlong": {"units": "0", "nano": 500000000}, "dshort": {"units": "0", "nano": 500000000}, "dlongMin": {"units": "0", "nano": 292900000}, "dshortMin": {"units": "0", "nano": 224700000}, "shortEnabledFlag": True, "name": "Доллар США", "exchange": "FX", "nominal": {"currency": "usd", "units": "1", "nano": 0}, "countryOfRisk": "", "countryOfRiskName": "", "tradingStatus": "SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "isoCurrencyName": "usd", "minPriceIncrement": {"units": "0", "nano": 2500000}, "apiTradeAvailableFlag": True, "uid": "a22a1263-8e1b-4546-a1aa-416463f104d3", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "6e97aa9b-50b6-4738-bce7-17313f2b2cc2", "forIisFlag": True, "first1minCandleDate": "2018-03-07T16:16:00Z", "first1dayCandleDate": "2000-05-16T00:00:00Z", "type": "Currencies", "step": 0.0025}),
            ("TCS00A101YV8", {"figi": "TCS00A101YV8", "ticker": "RU000A101YV8", "classCode": "TQCB", "isin": "RU000A101YV8", "lot": 1, "currency": "rub", "shortEnabledFlag": False, "name": "Позитив Текнолоджиз выпуск 1", "exchange": "MOEX_PLUS", "couponQuantityPerYear": 4, "maturityDate": "2023-07-26T00:00:00Z", "nominal": {"currency": "rub", "units": "1000", "nano": 0}, "stateRegDate": "2020-07-21T00:00:00Z", "placementDate": "2020-07-29T00:00:00Z", "placementPrice": {"currency": "rub", "units": "1000", "nano": 0}, "aciValue": {"currency": "rub", "units": "26", "nano": 780000000}, "countryOfRisk": "RU", "countryOfRiskName": "Российская Федерация", "sector": "it", "issueKind": "non_documentary", "issueSize": "500000", "issueSizePlan": "500000", "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "floatingCouponFlag": False, "perpetualFlag": False, "amortizationFlag": True, "minPriceIncrement": {"units": "0", "nano": 10000000}, "apiTradeAvailableFlag": True, "uid": "2ee80fbd-356f-4a01-8d64-d2bd1e73745c", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "0500b20b-1a28-4ed5-bf63-958b16a40080", "forIisFlag": True, "type": "Bonds", "step": 0.01}),
            ("BBG222222222", {"figi": "BBG222222222", "ticker": "TGLD", "classCode": "TQTD", "isin": "RU000A101X50", "lot": 100, "currency": "usd", "shortEnabledFlag": False, "name": "Тинькофф Золото", "exchange": "MOEX", "fixedCommission": {"units": "0", "nano": 450000000}, "focusType": "equity", "releasedDate": "2020-07-13T00:00:00Z", "countryOfRisk": "", "countryOfRiskName": "", "sector": "", "rebalancingFreq": "", "tradingStatus": "SECURITY_TRADING_STATUS_BREAK_IN_TRADING", "otcFlag": False, "buyAvailableFlag": True, "sellAvailableFlag": True, "minPriceIncrement": {"units": "0", "nano": 100000}, "apiTradeAvailableFlag": True, "uid": "a4b3adc6-4e04-4f06-9048-431aa1ed07ac", "realExchange": "REAL_EXCHANGE_MOEX", "positionUid": "548bde28-a5ea-4b7b-83d3-47b4c56a0167", "forIisFlag": True, "first1minCandleDate": "2020-08-26T07:00:00Z", "first1dayCandleDate": "2020-08-26T07:00:00Z", "type": "Etfs", "step": 0.0001}),
        ]

        for test in testData:
            self.server.ticker = ""
            self.server.figi = test[0]

            result = self.server.SearchByFIGI(requestPrice=False, showInfo=False, debug=False)

            assert result == test[1], 'FIGI: {}\nExpected: {}\nActual: {}'.format(test[0], test[1], result)

    def test_ShowInstrumentsInfoCheckType(self):
        assert isinstance(self.server.ShowInstrumentsInfo(showInstruments=False), str), "Not str type returned!"

    def test_ShowInstrumentsInfoPositive(self):
        with open("./tests/InstrumentsInfoDump.md", mode="r", encoding="UTF-8") as fH:
            iListInfo = fH.readlines()

        result = self.server.ShowInstrumentsInfo(showInstruments=False).split("\n")
        result[2] = "* **Actual on date:** [2022-07-21 14:26] (UTC)"  # replace 3 string with date similar as in InstrumentsInfoDump.md

        for i, line in enumerate(result):
            assert line + "\n" == iListInfo[i], 'Check `ShowInstrumentsInfo()` method! It returns different info than in `./tests/InstrumentsInfoDump.txt`\nLine: {}\nExpected: `{}`\nActual: `{}`'.format(i + 1, iListInfo[i], line + "\n")
