# TKSBrokerAPI — Release notes

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)

* 🇷🇺 [See release notes in russian here (релиз-ноты на русском)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/CHANGELOG_RU.md)
  * 💡 [All planned releases and features](https://github.com/Tim55667757/TKSBrokerAPI/milestones?direction=desc&sort=title&state=open)
  * 📂 [All open tasks in the backlog](https://github.com/Tim55667757/TKSBrokerAPI/issues?q=is%3Aissue+is%3Aopen+sort%3Acreated-asc)
* 📚 [Documentation for the TKSBrokerAPI module and examples of working with CLI](https://tim55667757.github.io/TKSBrokerAPI)
* 🎁 Support the project with a donation to our yoomoney-wallet: [410015019068268](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)


### [1.4.* (2022-09-??)](https://github.com/Tim55667757/TKSBrokerAPI/milestone/4) — preparing for release...

##### New features

* [In progress] [#6](https://github.com/Tim55667757/TKSBrokerAPI/issues/6) When launched with the `--history` key, the ability to specify an additional key `--render-chart` and display the change in instrument prices on an interactive or static chart using the [`PriceGenerator`](https://tim55667757.github.io/PriceGenerator) library.
* [In progress] [#10](https://github.com/Tim55667757/TKSBrokerAPI/issues/10) When requesting information about bonds (with the `--info` or `-i` key), more data is now calculated and displayed: bond payment schedule, total number of payments and already redeemed coupons, accumulated coupon income, current yield, yield to maturity and coupon's size.
* [In progress] [#11](https://github.com/Tim55667757/TKSBrokerAPI/issues/11) The `--user-info` key has been added, which displays data associated with the account for the current token: available information about the user, operations rights, limits on operations, and API methods available for this token.

##### Improvements

* [In progress] [#9](https://github.com/Tim55667757/TKSBrokerAPI/issues/9) Added information about the current trading status for the requested instrument to the method that implements launching with the `--info` (or `-i`) key. An additional `GetTradingStatus()` method has been implemented, using an extension of the `SearchByTicker()` and `SearchByFIGI()` methods. Added flags: `buyAvailableFlag`, `sellAvailableFlag`, `shortEnabledFlag`, `limitOrderAvailableFlag`, `marketOrderAvailableFlag` and `apiTradeAvailableFlag`.

##### Bug fixes

* ...


### [1.3.* (2022-08-??)](https://github.com/Tim55667757/TKSBrokerAPI/milestone/3) — preparing for release...

##### New features

* [In progress] [#14](https://github.com/Tim55667757/TKSBrokerAPI/issues/14) Implemented methods for opening grids of pending limit and stop orders.
* [In progress] [#15](https://github.com/Tim55667757/TKSBrokerAPI/issues/15) The `GetWithdrawalLimits()` method and the `--withdrawal-limits` key are implemented. They request the currency balance available to the user for withdrawing funds from the account.

##### Improvements

* [In progress] [#17](https://github.com/Tim55667757/TKSBrokerAPI/issues/17) Optimized price request for instruments and removed repeated price requests for the same instrument when launched with the `--prices` key or when calling the `Overview()` method.

##### Bug fixes

* [In progress] [#18](https://github.com/Tim55667757/TKSBrokerAPI/issues/18) Error handling added `raise JSONDecodeError("Expecting value", s, err.value) from None`.
* [In progress] [#16](https://github.com/Tim55667757/TKSBrokerAPI/issues/16) Fixed display of fractional numbers with the first zero after the decimal point, e.g. `1.` was displayed instead of `1.0`.
* ...


### [1.2.* (2022-08-??)](https://github.com/Tim55667757/TKSBrokerAPI/milestone/2) — preparing for release...

##### New features

* [In progress] [#5](https://github.com/Tim55667757/TKSBrokerAPI/issues/5) Added ability to download price history for an instrument with "only latest" update support, added `--history` key.
* [In progress] [#4](https://github.com/Tim55667757/TKSBrokerAPI/issues/4) Added the ability to search for an instrument by part of the name, ticker or FIGI. Added `--search` key.
* [In progress] [#13](https://github.com/Tim55667757/TKSBrokerAPI/issues/13) Added a local data cache with information on exchange instruments to avoid their permanent download from the server.

##### Improvements

* [In progress] [#8](https://github.com/Tim55667757/TKSBrokerAPI/issues/8) Added the `--no-cancelled` key to not display information about canceled operations when using the `--deals` (or `-d`) key.
* [In progress] [#12](https://github.com/Tim55667757/TKSBrokerAPI/issues/12) In the general information about the state of the portfolio (key `--overview` or `-o`), the section "Portfolio distribution by countries" has been added.

##### Bug fixes

* ...


### [1.1.* (2022-07-??)](https://github.com/Tim55667757/TKSBrokerAPI/milestone/1) — preparing for release...

##### New features

* License changed from MIT to [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
* **Important!** The functionality of most of the methods included in `TKSBrokerAPI` v1.0 has been restored, except for opening a grid of orders and downloading historical data (to be added in future releases). Now all methods work with the new Open API: https://tinkoff.github.io/investAPI/swagger-ui/
* **Important!** The `TKSBrokerAPI` module has been made as open-source project, further development continues there: https://github.com/Tim55667757/TKSBrokerAPI
* **Important!** The Tinkoff Invest API version supported by the `TKSBrokerAPI` library is now v2 and not backwards compatible.
* **Important!** All internal time variables were converted to ISO UTC format with `Z` (Zulu time) at the end of the string. Example: `1961-04-12T06:07:00.123456Z`. Local time is no longer used. This is to avoid confusion with the Tinkoff Invest API time, which uses UTC Z-notation.
* [In progress] [#3](https://github.com/Tim55667757/TKSBrokerAPI/issues/3) The basic CI-process for the release cycle has been implemented: the step of unit tests and launching the package build. CD-process for the release cycle has been implemented: dev builds for feature branches, release builds from release branches or master branch, which are then published to PyPI.
* [#4](https://github.com/Tim55667757/TKSBrokerAPI/issues/4) Added simple unit tests and stubs for some methods.
* [In progress] [#1](https://github.com/Tim55667757/TKSBrokerAPI/issues/1) Added main documentation sections to `README.md` and examples of working with the `TKSBrokerAPI` in CLI.
* [#2](https://github.com/Tim55667757/TKSBrokerAPI/issues/2) Added `pdoc` documentation automatic build step `PDocBuilder` for `TKSBrokerAPI` module methods.
* Added an analytics section to the `Overview()` method. The distribution of instruments by asset classes, companies, sectors and currencies is shown.
* Shown extended information on the instrument for the `--info` key, depending on the type of instrument (currency, stock, bond, fund or futures).
* Added keys `--close-order`, `--close-orders`, `--close-trade` and `--close-trades`. With their help, you can cancel one or more orders by ID or close deals on instruments, knowing their tickers.
* Implemented methods for closing orders and positions: `ClosePositions()`, `CloseAllPositions()`, `CloseOrders()`, `CloseAllOrders()` and `CloseAll()`.
* Implemented methods for opening limit and stop orders: `OpenOrder()`, `BuyLimit()`, `BuyStop()`, `SellLimit()` and `SellStop()`.
* Implemented methods for opening and closing positions for instruments: `OpenTrade()`, `CloseTrades()`, `CloseAllTrades()`, `Buy()`, `Sell()` and fixed the `CloseAll()` method.

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


## 1.0.* (2020-05 - 2022-07) — DEPRECATED version, not working with new Tinkoff Open API REST protocol

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
