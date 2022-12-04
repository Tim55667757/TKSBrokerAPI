# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
from pathlib import Path
from tksbrokerapi import TKSBrokerAPI


class TestTKSBrokerAPIMethods:

    @pytest.fixture(scope="function", autouse=True)
    def init(self):
        TKSBrokerAPI.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        TKSBrokerAPI.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        TKSBrokerAPI.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt

        # set up default parameters:
        Path("./tests/InstrumentsDump.json").touch()  # "touching" file to avoid updating by "file outdated" trigger
        self.server = TKSBrokerAPI.TinkoffBrokerServer(
            token="TKSBrokerAPI_unittest_fake_token",
            accountId="TKSBrokerAPI_unittest_fake_accountId",
            useCache=True,
            defaultCache="./tests/InstrumentsDump.json",
        )

    def test_ConsistentOfVariablesNames(self):
        mainVarNames = [
            "token", "accountId", "version", "aliases", "aliasesKeys", "exclude", "ticker", "figi", "depth",
            "server", "timeout", "headers", "body", "moreDebug",
            "historyFile", "htmlHistoryFile", "instrumentsFile", "searchResultsFile", "pricesFile", "infoFile",
            "bondsXLSXFile", "calendarFile", "overviewFile", "overviewDigestFile", "overviewPositionsFile",
            "overviewOrdersFile", "overviewAnalyticsFile", "overviewBondsCalendarFile", "reportFile",
            "withdrawalLimitsFile", "userInfoFile", "userAccountsFile", "iListDumpFile", "iList", "priceModel",
        ]
        actualNames = dir(self.server)

        for vName in mainVarNames:
            assert vName in actualNames, "One of main variables changed it's name! Problem is with variable [{}]".format(vName)

    def test__ParseJSONCheckType(self):
        assert isinstance(self.server._ParseJSON(rawData="{}"), dict), "Not dict type returned!"

    def test__ParseJSONPositive(self):
        testData = [
            ("{}", {}), ('{"x":123}', {"x": 123}), ('{"x":""}', {"x": ""}),
            ('{"abc": "123", "xyz": 123}', {"abc": "123", "xyz": 123}),
            ('{"abc": {"abc": "123", "xyz": 123}}', {"abc": {"abc": "123", "xyz": 123}}),
            ('{"abc": {"abc": "", "xyz": 0}}', {"abc": {"abc": "", "xyz": 0}}),
        ]

        for test in testData:
            result = self.server._ParseJSON(rawData=test[0])

            assert result == test[1], 'Expected: `_ParseJSON(rawData="{}", debug=False) == {}`, actual: `{}`'.format(test[0], test[1], result)

    def test__ParseJSONNegative(self):
        testData = [
            ("[]", []), ("{}", {}), ("{[]}", {}), ([], {}), (123, {}), ("123", 123), (None, {}), ("some string", {}),
        ]

        for test in testData:
            result = self.server._ParseJSON(rawData=test[0])

            assert result == test[1], "Unexpected output!"

    def test_SendAPIRequestCheckType(self):
        self.server.body = {"instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"}

        result = self.server.SendAPIRequest(
            url=self.server.server + r"/tinkoff.public.invest.api.contract.v1.InstrumentsService/Currencies",
            reqType="POST",
            retry=0,
            pause=0,
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
            )

            assert result == test[1], 'Expected: `{}`, actual: `{}`'.format(test[1], result)

    def test_ShowInstrumentInfoCheckType(self):
        assert isinstance(self.server.ShowInstrumentInfo(iJSON={}, show=False), str), "Not str type returned!"

    def test_ShowInstrumentInfoPositive(self):
        testData = [
            # share:
            {"figi": "TCS00A103X66", "ticker": "POSI", "name": "Positive Technologies"},
            # bond:
            {"figi": "TCS00A101YV8", "ticker": "RU000A101YV8", "name": "Позитив Текнолоджиз выпуск 1"},
            # etf:
            {"figi": "BBG222222222", "ticker": "TGLD", "name": "Тинькофф Золото"},
            # futures:
            {"figi": "FUTPLZL03220", "ticker": "PZH2", "name": "PLZL-3.22 Полюс Золото"},
            # currency:
            {"figi": "BBG0013HRTL0", "ticker": "CNYRUB_TOM", "name": "Юань"},
        ]

        for test in testData:
            self.server.ticker = test["ticker"]
            self.server.figi = ""
            searched = self.server.SearchByTicker(requestPrice=False, show=False)
            searched["limitOrderAvailableFlag"] = False
            searched["sellAvailableFlag"] = False
            searched["shortEnabledFlag"] = False
            searched["marketOrderAvailableFlag"] = False
            searched["apiTradeAvailableFlag"] = False
            result = self.server.ShowInstrumentInfo(iJSON=searched, show=False)
            assert test["name"] in result, "Some data in report is incorrect!"

    def test_SearchByTickerCheckType(self):
        self.server.ticker = "IBM"
        self.server.figi = ""

        assert isinstance(self.server.SearchByTicker(requestPrice=False, show=False), dict), "Not dict type returned!"

    def test_SearchByTickerPositive(self):
        testData = [  # tickers and their corresponding instruments:
            ("IBM", {'figi': 'BBG000BLNNH6', 'ticker': 'IBM', 'classCode': 'SPBXM', 'isin': 'US4592001014', 'lot': 1, 'currency': 'usd', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 999000000}, 'dshort': {'units': '0', 'nano': 999000000}, 'dlongMin': {'units': '0', 'nano': 968400000}, 'dshortMin': {'units': '0', 'nano': 413900000}, 'shortEnabledFlag': False, 'name': 'IBM', 'exchange': 'SPB_MORNING', 'ipoDate': '1915-11-11T00:00:00Z', 'issueSize': '896320073', 'countryOfRisk': 'US', 'countryOfRiskName': 'Соединенные Штаты Америки', 'sector': 'it', 'issueSizePlan': '4687500000', 'nominal': {'currency': 'usd', 'units': '0', 'nano': 200000000}, 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'divYieldFlag': True, 'shareType': 'SHARE_TYPE_COMMON', 'minPriceIncrement': {'units': '0', 'nano': 10000000}, 'apiTradeAvailableFlag': True, 'uid': 'ca370ca5-e42b-44e4-a0a5-daf5e51d02a7', 'realExchange': 'REAL_EXCHANGE_RTS', 'positionUid': 'b70a8cfc-90c1-4a66-8c39-f6239705b2fe', 'forIisFlag': True, 'first1minCandleDate': '2018-01-23T08:51:00Z', 'first1dayCandleDate': '1988-09-12T00:00:00Z', 'type': 'Shares', 'step': 0.01}),
            ("YNDX", {'figi': 'BBG006L8G4H1', 'ticker': 'YNDX', 'classCode': 'TQBR', 'isin': 'NL0009805522', 'lot': 1, 'currency': 'rub', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 405400000}, 'dshort': {'units': '0', 'nano': 399100000}, 'dlongMin': {'units': '0', 'nano': 228900000}, 'dshortMin': {'units': '0', 'nano': 182800000}, 'shortEnabledFlag': True, 'name': 'Yandex', 'exchange': 'MOEX_EVENING_WEEKEND', 'ipoDate': '2011-05-24T00:00:00Z', 'issueSize': '326016891', 'countryOfRisk': 'RU', 'countryOfRiskName': 'Российская Федерация', 'sector': 'telecom', 'issueSizePlan': '0', 'nominal': {'currency': 'eur', 'units': '0', 'nano': 10000000}, 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'divYieldFlag': False, 'shareType': 'SHARE_TYPE_COMMON', 'minPriceIncrement': {'units': '0', 'nano': 200000000}, 'apiTradeAvailableFlag': True, 'uid': '10e17a87-3bce-4a1f-9dfc-720396f98a3c', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': 'cb51e157-1f73-4c62-baac-93f11755056a', 'forIisFlag': True, 'first1minCandleDate': '2018-03-07T18:38:00Z', 'first1dayCandleDate': '2014-06-04T07:00:00Z', 'type': 'Shares', 'step': 0.2}),
            ("USD000UTSTOM", {'figi': 'BBG0013HGFT4', 'ticker': 'USD000UTSTOM', 'classCode': 'CETS', 'isin': '', 'lot': 1000, 'currency': 'rub', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 980000000}, 'dshort': {'units': '0', 'nano': 980000000}, 'dlongMin': {'units': '0', 'nano': 858600000}, 'dshortMin': {'units': '0', 'nano': 407100000}, 'shortEnabledFlag': True, 'name': 'Доллар США', 'exchange': 'FX', 'nominal': {'currency': 'usd', 'units': '1', 'nano': 0}, 'countryOfRisk': '', 'countryOfRiskName': '', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'isoCurrencyName': 'usd', 'minPriceIncrement': {'units': '0', 'nano': 2500000}, 'apiTradeAvailableFlag': True, 'uid': 'a22a1263-8e1b-4546-a1aa-416463f104d3', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '6e97aa9b-50b6-4738-bce7-17313f2b2cc2', 'forIisFlag': True, 'first1minCandleDate': '2018-03-07T16:16:00Z', 'first1dayCandleDate': '2000-05-16T00:00:00Z', 'type': 'Currencies', 'step': 0.0025}),
            ("RU000A101YV8", {'figi': 'TCS00A101YV8', 'ticker': 'RU000A101YV8', 'classCode': 'TQCB', 'isin': 'RU000A101YV8', 'lot': 1, 'currency': 'rub', 'shortEnabledFlag': False, 'name': 'Позитив Текнолоджиз выпуск 1', 'exchange': 'MOEX', 'couponQuantityPerYear': 4, 'maturityDate': '2023-07-26T00:00:00Z', 'nominal': {'currency': 'rub', 'units': '750', 'nano': 0}, 'stateRegDate': '2020-07-21T00:00:00Z', 'placementDate': '2020-07-29T00:00:00Z', 'placementPrice': {'currency': 'rub', 'units': '1000', 'nano': 0}, 'aciValue': {'currency': 'rub', 'units': '3', 'nano': 70000000}, 'countryOfRisk': 'RU', 'countryOfRiskName': 'Российская Федерация', 'sector': 'it', 'issueKind': 'non_documentary', 'issueSize': '500000', 'issueSizePlan': '500000', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'floatingCouponFlag': False, 'perpetualFlag': False, 'amortizationFlag': True, 'minPriceIncrement': {'units': '0', 'nano': 10000000}, 'apiTradeAvailableFlag': True, 'uid': '2ee80fbd-356f-4a01-8d64-d2bd1e73745c', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '0500b20b-1a28-4ed5-bf63-958b16a40080', 'forIisFlag': True, 'first1minCandleDate': '2020-07-29T13:21:00Z', 'first1dayCandleDate': '2020-07-29T07:00:00Z', 'type': 'Bonds', 'step': 0.01}),
            ("TGLD", {'figi': 'BBG222222222', 'ticker': 'TGLD', 'classCode': 'TQTD', 'isin': 'RU000A101X50', 'lot': 100, 'currency': 'usd', 'shortEnabledFlag': False, 'name': 'Тинькофф Золото', 'exchange': 'MOEX', 'fixedCommission': {'units': '0', 'nano': 450000000}, 'focusType': 'equity', 'releasedDate': '2020-07-13T00:00:00Z', 'countryOfRisk': '', 'countryOfRiskName': '', 'sector': '', 'rebalancingFreq': '', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'minPriceIncrement': {'units': '0', 'nano': 100000}, 'apiTradeAvailableFlag': True, 'uid': 'a4b3adc6-4e04-4f06-9048-431aa1ed07ac', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '548bde28-a5ea-4b7b-83d3-47b4c56a0167', 'forIisFlag': True, 'first1minCandleDate': '2020-08-26T07:00:00Z', 'first1dayCandleDate': '2020-08-26T07:00:00Z', 'type': 'Etfs', 'step': 0.0001}),
        ]

        for test in testData:
            self.server.ticker = test[0]
            self.server.figi = ""

            result = self.server.SearchByTicker(requestPrice=False, show=False)
            assert result == test[1], 'Ticker: {}\nExpected: {}\nActual: {}'.format(test[0], test[1], result)

    def test_SearchByFIGICheckType(self):
        self.server.ticker = ""
        self.server.figi = "BBG000BLNNH6"

        assert isinstance(self.server.SearchByFIGI(requestPrice=False, show=False), dict), "Not dict type returned!"

    def test_SearchByFIGIPositive(self):
        testData = [  # FIGIs and their corresponding instruments:
            ("BBG000BLNNH6", {'figi': 'BBG000BLNNH6', 'ticker': 'IBM', 'classCode': 'SPBXM', 'isin': 'US4592001014', 'lot': 1, 'currency': 'usd', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 999000000}, 'dshort': {'units': '0', 'nano': 999000000}, 'dlongMin': {'units': '0', 'nano': 968400000}, 'dshortMin': {'units': '0', 'nano': 413900000}, 'shortEnabledFlag': False, 'name': 'IBM', 'exchange': 'SPB_MORNING', 'ipoDate': '1915-11-11T00:00:00Z', 'issueSize': '896320073', 'countryOfRisk': 'US', 'countryOfRiskName': 'Соединенные Штаты Америки', 'sector': 'it', 'issueSizePlan': '4687500000', 'nominal': {'currency': 'usd', 'units': '0', 'nano': 200000000}, 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'divYieldFlag': True, 'shareType': 'SHARE_TYPE_COMMON', 'minPriceIncrement': {'units': '0', 'nano': 10000000}, 'apiTradeAvailableFlag': True, 'uid': 'ca370ca5-e42b-44e4-a0a5-daf5e51d02a7', 'realExchange': 'REAL_EXCHANGE_RTS', 'positionUid': 'b70a8cfc-90c1-4a66-8c39-f6239705b2fe', 'forIisFlag': True, 'first1minCandleDate': '2018-01-23T08:51:00Z', 'first1dayCandleDate': '1988-09-12T00:00:00Z', 'type': 'Shares', 'step': 0.01}),
            ("BBG006L8G4H1", {'figi': 'BBG006L8G4H1', 'ticker': 'YNDX', 'classCode': 'TQBR', 'isin': 'NL0009805522', 'lot': 1, 'currency': 'rub', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 405400000}, 'dshort': {'units': '0', 'nano': 399100000}, 'dlongMin': {'units': '0', 'nano': 228900000}, 'dshortMin': {'units': '0', 'nano': 182800000}, 'shortEnabledFlag': True, 'name': 'Yandex', 'exchange': 'MOEX_EVENING_WEEKEND', 'ipoDate': '2011-05-24T00:00:00Z', 'issueSize': '326016891', 'countryOfRisk': 'RU', 'countryOfRiskName': 'Российская Федерация', 'sector': 'telecom', 'issueSizePlan': '0', 'nominal': {'currency': 'eur', 'units': '0', 'nano': 10000000}, 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'divYieldFlag': False, 'shareType': 'SHARE_TYPE_COMMON', 'minPriceIncrement': {'units': '0', 'nano': 200000000}, 'apiTradeAvailableFlag': True, 'uid': '10e17a87-3bce-4a1f-9dfc-720396f98a3c', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': 'cb51e157-1f73-4c62-baac-93f11755056a', 'forIisFlag': True, 'first1minCandleDate': '2018-03-07T18:38:00Z', 'first1dayCandleDate': '2014-06-04T07:00:00Z', 'type': 'Shares', 'step': 0.2}),
            ("BBG0013HGFT4", {'figi': 'BBG0013HGFT4', 'ticker': 'USD000UTSTOM', 'classCode': 'CETS', 'isin': '', 'lot': 1000, 'currency': 'rub', 'klong': {'units': '2', 'nano': 0}, 'kshort': {'units': '2', 'nano': 0}, 'dlong': {'units': '0', 'nano': 980000000}, 'dshort': {'units': '0', 'nano': 980000000}, 'dlongMin': {'units': '0', 'nano': 858600000}, 'dshortMin': {'units': '0', 'nano': 407100000}, 'shortEnabledFlag': True, 'name': 'Доллар США', 'exchange': 'FX', 'nominal': {'currency': 'usd', 'units': '1', 'nano': 0}, 'countryOfRisk': '', 'countryOfRiskName': '', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'isoCurrencyName': 'usd', 'minPriceIncrement': {'units': '0', 'nano': 2500000}, 'apiTradeAvailableFlag': True, 'uid': 'a22a1263-8e1b-4546-a1aa-416463f104d3', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '6e97aa9b-50b6-4738-bce7-17313f2b2cc2', 'forIisFlag': True, 'first1minCandleDate': '2018-03-07T16:16:00Z', 'first1dayCandleDate': '2000-05-16T00:00:00Z', 'type': 'Currencies', 'step': 0.0025}),
            ("TCS00A101YV8", {'figi': 'TCS00A101YV8', 'ticker': 'RU000A101YV8', 'classCode': 'TQCB', 'isin': 'RU000A101YV8', 'lot': 1, 'currency': 'rub', 'shortEnabledFlag': False, 'name': 'Позитив Текнолоджиз выпуск 1', 'exchange': 'MOEX', 'couponQuantityPerYear': 4, 'maturityDate': '2023-07-26T00:00:00Z', 'nominal': {'currency': 'rub', 'units': '750', 'nano': 0}, 'stateRegDate': '2020-07-21T00:00:00Z', 'placementDate': '2020-07-29T00:00:00Z', 'placementPrice': {'currency': 'rub', 'units': '1000', 'nano': 0}, 'aciValue': {'currency': 'rub', 'units': '3', 'nano': 70000000}, 'countryOfRisk': 'RU', 'countryOfRiskName': 'Российская Федерация', 'sector': 'it', 'issueKind': 'non_documentary', 'issueSize': '500000', 'issueSizePlan': '500000', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'floatingCouponFlag': False, 'perpetualFlag': False, 'amortizationFlag': True, 'minPriceIncrement': {'units': '0', 'nano': 10000000}, 'apiTradeAvailableFlag': True, 'uid': '2ee80fbd-356f-4a01-8d64-d2bd1e73745c', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '0500b20b-1a28-4ed5-bf63-958b16a40080', 'forIisFlag': True, 'first1minCandleDate': '2020-07-29T13:21:00Z', 'first1dayCandleDate': '2020-07-29T07:00:00Z', 'type': 'Bonds', 'step': 0.01}),
            ("BBG222222222", {'figi': 'BBG222222222', 'ticker': 'TGLD', 'classCode': 'TQTD', 'isin': 'RU000A101X50', 'lot': 100, 'currency': 'usd', 'shortEnabledFlag': False, 'name': 'Тинькофф Золото', 'exchange': 'MOEX', 'fixedCommission': {'units': '0', 'nano': 450000000}, 'focusType': 'equity', 'releasedDate': '2020-07-13T00:00:00Z', 'countryOfRisk': '', 'countryOfRiskName': '', 'sector': '', 'rebalancingFreq': '', 'tradingStatus': 'SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING', 'otcFlag': False, 'buyAvailableFlag': True, 'sellAvailableFlag': True, 'minPriceIncrement': {'units': '0', 'nano': 100000}, 'apiTradeAvailableFlag': True, 'uid': 'a4b3adc6-4e04-4f06-9048-431aa1ed07ac', 'realExchange': 'REAL_EXCHANGE_MOEX', 'positionUid': '548bde28-a5ea-4b7b-83d3-47b4c56a0167', 'forIisFlag': True, 'first1minCandleDate': '2020-08-26T07:00:00Z', 'first1dayCandleDate': '2020-08-26T07:00:00Z', 'type': 'Etfs', 'step': 0.0001}),
        ]

        for test in testData:
            self.server.ticker = ""
            self.server.figi = test[0]

            result = self.server.SearchByFIGI(requestPrice=False, show=False)

            assert result == test[1], 'FIGI: {}\nExpected: {}\nActual: {}'.format(test[0], test[1], result)

    def test_ShowInstrumentsInfoCheckType(self):
        assert isinstance(self.server.ShowInstrumentsInfo(show=False), str), "Not str type returned!"

    def test_ShowInstrumentsInfoPositive(self):
        with open("./tests/InstrumentsInfoDump.md", mode="r", encoding="UTF-8") as fH:
            iListInfo = fH.readlines()

        result = self.server.ShowInstrumentsInfo(show=False).split("\n")
        result[2] = "* **Actual on date:** [2022-11-13 15:00 UTC]"  # replace 3 string with date similar as in InstrumentsInfoDump.md

        for i, line in enumerate(result):
            assert line + "\n" == iListInfo[i], 'Check `ShowInstrumentsInfo()` method! It returns different info than in `./tests/InstrumentsInfoDump.txt`\nLine: {}\nExpected: `{}`\nActual: `{}`'.format(i + 1, iListInfo[i], line + "\n")
