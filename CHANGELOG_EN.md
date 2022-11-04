# TKSBrokerAPI — Release notes

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)

* 🇷🇺 [See release notes in russian here (релиз-ноты на русском)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/CHANGELOG_RU.md)
  * 💡 [All planned releases and features](https://github.com/Tim55667757/TKSBrokerAPI/milestones?direction=desc&sort=title&state=open)
  * 📂 [All open tasks in the backlog](https://github.com/Tim55667757/TKSBrokerAPI/issues?q=is%3Aissue+is%3Aopen+sort%3Acreated-asc)
* 📚 [Documentation for the TKSBrokerAPI module and examples of working with CLI](https://tim55667757.github.io/TKSBrokerAPI)
* 🎁 Support the project with a donation to our yoomoney-wallet: [410015019068268](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)


### [1.4.* (2022-11-05)](https://github.com/Tim55667757/TKSBrokerAPI/milestone/4) — released

##### New features

* [#15](https://github.com/Tim55667757/TKSBrokerAPI/issues/15) Implemented methods: `RequestLimits()` to request raw data on user withdrawal limits, `OverviewLimits()` to display table data, and the `--limits` (`--withdrawal-limits`, `-w`) key to request and print limits in the console.
* [#6](https://github.com/Tim55667757/TKSBrokerAPI/issues/6) When launched with the `--history` key, the ability to specify an additional key `--render-chart` and rendering interactive or static charts using the [`PriceGenerator`](https://tim55667757.github.io/PriceGenerator) library. Similarly, you can build charts for previously saved csv-files with the candles history. To do this, you need to specify the `--render-chart` key with the new key for loading data from file: `--load-history`.
* [#46](https://github.com/Tim55667757/TKSBrokerAPI/issues/46) Implemented the `--list-xlsx` key (or `-x`) that returned raw instruments data for current account similar to `dump.json`, but saved in XLSX format to further used by data scientists or stock analytics, `dump.xlsx` by default. Also, `DumpInstrumentsAsXLSX()` method that converts raw instruments data to XLSX format was developed.
* [#11](https://github.com/Tim55667757/TKSBrokerAPI/issues/11) The `--user-info` (`-u`) key has been added, which displays data associated with the account linked to the current token: available information about the user and his accounts, rights to operations, limits for margin trading. Also added the `--account` (`--accounts`, `-a`) key, which displays a simple table containing only user accounts.
* [#10](https://github.com/Tim55667757/TKSBrokerAPI/issues/10) When requesting information about bonds (with the `--info` or `-i` key), more data is now calculated and displayed: bond payment calendar, total number of payments and already redeemed coupons, coupons yield (average coupon daily yield * 365), current price yield (average daily yield * 365), ACI and coupon's size. To request the necessary information, the `RequestBondCoupons()` (returns a dictionary of processed data received from the server) and `ExtendBondsData()` (returns an extended pandas dataframe containing more information about bonds) methods were implemented to extend bonds data with more information. The `ShowInstrumentInfo()` method has been improved to display more information on bonds and the payment calendar. To receive extended information about bonds in XLSX-format now you can use `--bonds-xlsx` (`-b`) key.
* [#63](https://github.com/Tim55667757/TKSBrokerAPI/issues/63) The `CreateBondsCalendar()` method is implemented, which generates a pandas dataframe with a general payment calendar for the specified or all bonds. The `ShowBondsCalendar()` method displays the calendar in the console and saves it to a file, `calendar.md` by default in Markdown format. To request a payment calendar, you need to use the `--calendar` (`-c`) key. Also, the table in XLSX format will be saved to the default file `calendar.xlsx`.

##### Improvements

* [#59](https://github.com/Tim55667757/TKSBrokerAPI/issues/59) TKSBrokerAPI build version was added to the start of debug log, also shows by the key `--version` (or `--ver`).
* [#47](https://github.com/Tim55667757/TKSBrokerAPI/issues/47) `iList` field is not actual because local `dump.json` make the similar function and auto-updates instruments list. So this field was deleted from `TinkoffBrokerServer()` class.
* [#9](https://github.com/Tim55667757/TKSBrokerAPI/issues/9) Added information about the current trading status for the requested instrument to the method `ShowInstrumentInfo()`. An additional `RequestTradingStatus()` method has been implemented to request current trade status of instrument. Added flags: `buyAvailableFlag`, `sellAvailableFlag`, `shortEnabledFlag`, `limitOrderAvailableFlag`, `marketOrderAvailableFlag` and `apiTradeAvailableFlag`. As part of the same task, the task [#37](https://github.com/Tim55667757/TKSBrokerAPI/issues/37) was implemented: added the ability to save information on the instrument to a file specified by the `--output` key, by default `info .md`.
* [#64](https://github.com/Tim55667757/TKSBrokerAPI/issues/64) WARNING! Refactor a lot of methods. All "show" parameters: `showPrice`, `showPrices`, `printInfo`, `showInfo`, `showInstruments`, `showResults`, `showStatistics`, `printDeals`, `printCandles`, `showLimits`, `showAccounts` — were replaced with simple `show`.
* [#65](https://github.com/Tim55667757/TKSBrokerAPI/issues/65) WARNING! Refactor a lot of methods. All `overview` parameters were replaced with `portfolio`.
* No retries for 4xx net errors, only for 5xx.
* If you run `SendAPIRequest(debug=True)` then prints more debug information, e.g. request and response parameters, headers etc.
* Added waiting between network requests, in case of reaching the limit on the number of requests. The limit is determined by the response header value `"x-ratelimit-remaining": "0"`, and the number of seconds to wait is determined by the value of the `x-ratelimit-reset` header, for example, `"x-ratelimit-reset": "15"` , which means wait 15 seconds before the next request. This significantly reduced the number of network errors for a large number of requests to the server API.
* Header `"x-app-name": "Tim55667757.TKSBrokerAPI"` was added to API requests to identify TKSBrokerAPI framework.

##### Bug fixes

* Bug fix with `NoneType object has no attribute ...` if `--history` key used without any variables.


### [1.3.70 (2022-09-07)](https://github.com/Tim55667757/TKSBrokerAPI/releases/tag/1.3.70) — released

##### New features

* [#5](https://github.com/Tim55667757/TKSBrokerAPI/issues/5) Added ability to download price history for an instrument with "only latest" update support, added `--history` key. Also, the `--interval` key allows you to specify the time interval for downloading price candles in the OHLCV format. The `--only-missing` key allows you to download only the last candles saved in the file specified via `--output`. The `--csv-sep` key sets the separator between data in csv files. Minimum requested date in the past is `1970-01-01`. Warning! Broker server use ISO UTC time by default.

##### Improvements

* [#17](https://github.com/Tim55667757/TKSBrokerAPI/issues/17) Optimized price request for instruments and removed repeated price requests for the same instrument when launched with the `--prices` key or when calling the `Overview()` method. Now TKSBrokerAPI not request prices for duplicated instruments and saving working time.
* [#43](https://github.com/Tim55667757/TKSBrokerAPI/issues/43) Added new keys to reduce information in the `Overview()` method: the `--overview-positions` key shows only open positions, without everything else, the `--overview-digest` key shows a short digest of the portfolio status, the `--overview-analytics` key shows only the analytics section and the distribution of the portfolio by various categories, the `--overview-orders` shows only section of open limits and stop orders.
* [#44](https://github.com/Tim55667757/TKSBrokerAPI/issues/44) All markdown-tables are brought to the standard form, including the rendering of the right side of the tables.

##### Bug fixes

* [#18](https://github.com/Tim55667757/TKSBrokerAPI/issues/18) Error handling added `raise JSONDecodeError("Expecting value", s, err.value) from None`. Now the message is showing: `Check you Internet connection! Failed to establish a new connection to broker server!` and the path to the debug log file.
* [#16](https://github.com/Tim55667757/TKSBrokerAPI/issues/16) Fixed display of fractional numbers with the first zero after the decimal point, e.g. `1.` was displayed instead of `1.0`.
* [#38](https://github.com/Tim55667757/TKSBrokerAPI/issues/38) fixed broken table when ETF requested.


### [1.2.62 (2022-08-23)](https://github.com/Tim55667757/TKSBrokerAPI/releases/tag/1.2.62) — released

##### New features

* [#13](https://github.com/Tim55667757/TKSBrokerAPI/issues/13) To reduce the number of requests to the server, the ability to cache raw data on exchange instruments has been added. The cache is used by default when the `TinkoffBrokerServer` class is initialized, but this action can be canceled using the `useCache=False` class variable or using the `--no-cache` key in the console. The `DumpInstruments()` method has been added, with which you can create a data dump from the server. The `iListDumpFile` variable has also been added to the `TinkoffBrokerServer` class (the path to the cache, `dump.json` by default). The cache is automatically refreshed if there is a different day than the day the `dump.json` file was last modified. Note: all dates are used in UTC format.
* [#7](https://github.com/Tim55667757/TKSBrokerAPI/issues/7) Added the ability to search for an instrument by part of the name, ticker or FIGI with`--search` key (or `-s`). A method for searching `SearchInstruments()` has been implemented, to which a search pattern can be passed as input: part of a word or a string with a regular expression. As a result, the method returns a dictionary of dictionaries, similar to variable `iList`, but containing only found instruments ([examples](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Find-an-instrument)).
* New method `IsInPortfolio()` was added. It checks if instrument is in the user's portfolio. Instrument must be defined by `self.ticker` (highly priority) or `self.figi`. Method returns `True` if portfolio contains open position with given instrument, `False` otherwise.
* New method `GetInstrumentFromPortfolio()` was added. It returns instrument's data if it is in the user's portfolio. Instrument must be defined by `self.ticker` (highly priority) or `self.figi`.

##### Improvements

* [#12](https://github.com/Tim55667757/TKSBrokerAPI/issues/12) In the general information about the state of the portfolio (key `--overview` or `-o`), the section "Portfolio distribution by countries" has been added ([example](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Get-the-current-portfolio-and-asset-allocation-statistics)).
* [#8](https://github.com/Tim55667757/TKSBrokerAPI/issues/8) Added the `--no-cancelled` key and the `showCancelled` variable in the `Deals()` method to control shows canceled operations when using the `--deals` (or `-d`) key. Changed default report filename from `report.md` to `deals.md`.
* [#42](https://github.com/Tim55667757/TKSBrokerAPI/issues/42) [Example](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md#Abstract-scenario-implementation-example) with abstract trade scenario was added.
* To the `stat` section of the `Overview()` result was added `funds` field. This is dict with free funds for trading (total - blocked), by all currencies, e.g. `{"rub": {"total": 10000.99, "totalCostRUB": 10000.99, "free": 1234.56, "freeCostRUB": 1234.56}, "usd": {"total": 250.55, "totalCostRUB": 15375.80, "free": 125.05, "freeCostRUB": 7687.50}}`.

##### Bug fixes

* Bug fix with bond type (failed with `iJSON["type"] == "Bond"`, correct: `iJSON["type"] == "Bonds"`).
* Bug fixed: `TypeError: JSONDecoder.__init__() got an unexpected keyword argument 'encoding'`. Bug occurred because changed in Python version 3.9: The keyword argument encoding has been removed. See: https://docs.python.org/3/library/json.html#json.loads
* Bug fix with incorrect `Overview()["stat"]["funds"]["rub"]` calculation in rubles.


### [1.1.48 (2022-07-28)](https://github.com/Tim55667757/TKSBrokerAPI/releases/tag/1.1.48) — released

##### New features

* License changed from MIT to [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
* **Important!** The functionality of most of the methods included in `TKSBrokerAPI` v1.0 has been restored, except for opening a grid of orders and downloading historical data (to be added in future releases). Now all methods work with the new Open API: https://tinkoff.github.io/investAPI/swagger-ui/
* **Important!** The `TKSBrokerAPI` module has been made as open-source project, further development continues there: https://github.com/Tim55667757/TKSBrokerAPI
* **Important!** The Tinkoff Invest API version supported by the `TKSBrokerAPI` library is now v2 and not backwards compatible.
* **Important!** All internal time variables were converted to ISO UTC format with `Z` (Zulu time) at the end of the string. Example: `1961-04-12T06:07:00.123456Z`. Local time is no longer used. This is to avoid confusion with the Tinkoff Invest API time, which uses UTC Z-notation.
* [#1](https://github.com/Tim55667757/TKSBrokerAPI/issues/1) Added main documentation sections and examples of working with CLI to [`README.md`](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md) and API-documentation of [`TKSBrokerAPI`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html).
* [#2](https://github.com/Tim55667757/TKSBrokerAPI/issues/2) Added `pdoc` documentation automatic build step `PDocBuilder` for `TKSBrokerAPI` module methods.
* [#3](https://github.com/Tim55667757/TKSBrokerAPI/issues/3) The basic CI-process for the release cycle has been implemented: the step of unit tests and launching the package build. CD-process for the release cycle has been implemented: dev builds for feature branches, release builds from release branches or master branch, which are then published to PyPI. Example of build success: [tksbrokerapi-1.2.dev39](https://app.travis-ci.com/github/Tim55667757/TKSBrokerAPI/builds/253552987) and [PyPI packet](https://pypi.org/project/tksbrokerapi/1.2.dev39/).
* [#4](https://github.com/Tim55667757/TKSBrokerAPI/issues/4) Added simple unit tests and stubs for some methods.
* Added an analytics section to the `Overview()` method. The distribution of instruments by asset classes, companies, sectors and currencies is shown.
* Shown extended information on the instrument for the `--info` key, depending on the type of instrument (currency, stock, bond, fund or futures).
* Added keys `--close-order`, `--close-orders`, `--close-trade` and `--close-trades`. With their help, you can cancel one or more orders by ID or close deals on instruments, knowing their tickers.
* Implemented methods for closing orders and positions: `ClosePositions()`, `CloseAllPositions()`, `CloseOrders()`, `CloseAllOrders()` and `CloseAll()`.
* Implemented methods for opening limit and stop orders: `Order()`, `BuyLimit()`, `BuyStop()`, `SellLimit()` and `SellStop()`.
* Implemented methods for opening and closing positions for instruments: `Trade()`, `CloseTrades()`, `CloseAllTrades()`, `Buy()`, `Sell()` and fixed the `CloseAll()` method.

##### Improvements

* **Important!** By optimizing the algorithms, refactoring the code and using the `multiprocessing` module, we managed to speed up the download of instruments during their initial listing by 40-60%.
* **Important!** Enabled logging with rotation from 5Mb to the default file `TKSBrokerAPI.log`. Optimized logging module. Reduced the number of unnecessary notifications. By default, debug logs are printed only to the log file, and info logs are output to the console. You can change the logging level with the keys: `--debug-level`, `--verbosity` or `-v`.
* All enumerated data types and constants moved to `TKSEnums.py` file.
* Added aliases for USD, EUR, GBP, CHF, CNY, HKD, TRY — now they can be used instead of tickers.
* The client's portfolio, information about instrument, the list of available instruments for trading and the history of client operations are now displayed in markdown format.
* For the `TinkoffBrokerServer()` class, it is now possible to set the `token` parameter when initializing the class, and when setting the `TKS_API_TOKEN` environment variable. If the `token` parameter is given when the class is initialized, then it takes highest priority.
* For the `TinkoffBrokerServer()` class, it is now possible to set the `accountId` parameter when initializing the class, and when setting the `TKS_ACCOUNT_ID` environment variable. If the `accountId` parameter is given when the class is initialized, then it takes highest priority. You can find out your account number in any brokerage report, the contract number will be indicated there, it is also your `accountId`.
* All methods related to viewing data in the console have been updated after the transition of the Tinkoff Invest API broker to version v2.
* The `Overview()` method now shows more information on pending and stop orders.
* The `SendAPIRequest()` method now shows more information in the logs for all 4xx and 5xx errors.
* Moved from the `Overview()` method to separate methods `RequestPortfolio()`, `RequestPositions()`, `RequestPendingOrders` and `RequestStopOrders()` — operations on requesting a portfolio, open positions and user orders.
* Using the `CloseOrders()` method, it is now possible to close both exchange pending and stop orders. It is enough to specify an ID or a list of IDs.
* Added display of the difference in % between the previous and current closing price of the instrument in all tables where it is required.
* [#22](https://github.com/Tim55667757/TKSBrokerAPI/issues/22) `--open-trade` and `--open-order` keys are replaced with `--trade` and `--order` keys, because it had long names. `OpenOrder()` and `OpenTrade()` methods are replaced with `Order()` and `Trade()` methods.
* Static method `GetDatesAsString()` moved outside from class `TinkoffBrokerServer()`.
* Variable `instrumentsList` renamed as `iList`.
* The `MDInfo()` method has been renamed to `ShowInstrumentInfo()` (similar to exist `ShowInstrumentsInfo()`).

##### Bug fixes

* **Important!** Refactored and fixed a lot of errors in methods related to the transition of Tinkoff Invest API to version v2 and changing data types.
* Fixed counter in the log in the line "Pairs (tickers, timeframes) count: [XXX]"
* Fixed a bug in the `Deals()` method: in the case when the end date is not specified, the current date is now taken.
* Fixed a bug with displaying the history of operations if there were dividend payments for the specified period.
* Fixed a bug when the server returned an empty fee.
* [#26](https://github.com/Tim55667757/TKSBrokerAPI/issues/26) Fixed a bug with incorrect result for `FloatToNano(number=0.05)`.
* [#34](https://github.com/Tim55667757/TKSBrokerAPI/issues/34) Fixed a bug with `KeyError: 'asks'` when no response from server with current prices.
* [#32](https://github.com/Tim55667757/TKSBrokerAPI/issues/32) Fixed a bug with some problems when trying to execute `--close-all orders`. Extra messages, and with them the formatting error, have been removed.


## [1.0.1 (2020-05 - 2022-07)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/CHANGELOG_EN.md#101-2020-05---2022-07--deprecated-version-not-working-with-new-tinkoff-open-api-rest-protocol) — DEPRECATED version, not working with new Tinkoff Open API REST protocol

##### Retrospective

First prototype [TKSBrokerAPI](https://github.com/Tim55667757/TKSBrokerAPI) - python API over REST protocol for [Tinkoff Invest API](https://tinkoff.github.io/investAPI/swagger-ui/) - included the main features for working with the exchange:
* get prices in the order book (DOM - Depth of Market) for the selected instrument;
* get a list of instruments, their names, tickers and FIGI;
* view the current state of the portfolio and its value;
* receive full brokerage information on the instrument, knowing its ticker or FIGI;
* get a table of current prices for the list of instruments;
* receive information on historical prices of instruments available through Tinkoff Broker and save them to csv-files;
* load historical price data from csv-files and display them on an interactive chart or in the console;
* open and close limit orders;
* create market orders (market orders executed at current prices in order book);
* open a grid of limit orders with a certain step;
* close all orders and positions at once or only a certain type: stocks, bonds, funds;
* create a report on operations for the specified period.

Then, from about the middle to the end of 2021, Tinkoff developers actively changed their REST protocol. The `TKSBrokerAPI` module has become broken. But during the spring-summer of 2022, we managed to restore and even expand most of its functions, rewrite the code to work with the new Tinkoff Open API REST protocol, put the library into open source, and set up the release cycle.

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)
