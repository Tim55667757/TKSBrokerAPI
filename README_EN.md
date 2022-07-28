# TKSBrokerAPI

**[TKSBrokerAPI](https://github.com/Tim55667757/TKSBrokerAPI)** is a python API for working with Tinkoff Open API and accessing the [Tinkoff Investments](http://tinkoff.ru/sl/AaX1Et1omnH) broker's trade server via the REST protocol. The TKSBrokerAPI module can be used from the console, it has a rich keys and commands. Also, you can used it with `python import`. TKSBrokerAPI allows you to automate routine trading operations and implement your trading scenarios, or just receive the necessary information from the broker. It is easy enough to integrate into CI/CD automation systems.

[![Build Status](https://travis-ci.com/Tim55667757/TKSBrokerAPI.svg?branch=master)](https://travis-ci.com/Tim55667757/TKSBrokerAPI)
[![pypi](https://img.shields.io/pypi/v/TKSBrokerAPI.svg)](https://pypi.python.org/pypi/TKSBrokerAPI)
[![license](https://img.shields.io/pypi/l/TKSBrokerAPI.svg)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/LICENSE)
[![ru-doc](https://badgen.net/badge/russian/readme/pink)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md)
[![api-doc](https://badgen.net/badge/api-doc/TKSBrokerAPI/blue)](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html)
[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)

❗ If you are missing some feature of the program or some specific example in the documentation to understand how to work with the TKSBrokerAPI module (in the CLI or as a python API), then describe your case in the section 👉 [**Issues**](https://github.com/Tim55667757/TKSBrokerAPI/issues/new) 👈, please. As far as possible, we will try to implement the desired feature and add examples in the next release.

**Useful links**

* 📚 [See documentation and examples in russian here (документация и примеры на русском)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md)
  * ⚙ [TKSBrokerAPI module documentation](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html)
  * 🇷🇺 [See release notes in russian here (релиз-ноты на русском)](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/CHANGELOG.md)
  * 🇺🇸 [Release notes](https://github.com/Tim55667757/TKSBrokerAPI/blob/master/CHANGELOG_EN.md)
    * 💡 [All planned releases and features](https://github.com/Tim55667757/TKSBrokerAPI/milestones?direction=desc&sort=title&state=open)
    * 📂 [All open tasks in the backlog](https://github.com/Tim55667757/TKSBrokerAPI/issues?q=is%3Aissue+is%3Aopen+sort%3Acreated-asc)
* 🎁 Support the project with a donation to our yoomoney-wallet: [410015019068268](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)

**Contents**

1. [Introduction](#Introduction)
   - [Key features](#Key-features)
2. [Setup](#Setup)
3. [Auth](#Auth)
   - [Token](#Token)
   - [User account ID](#User-account-ID)
4. [Usage examples](#Usage-examples)
   - [Command line](#Command-line)
     - [Reference](#Reference)
     - [Get a list of all instruments available for trading](#Get-a-list-of-all-instruments-available-for-trading)
     - [Get information about an instrument](#Get-information-about-an-instrument)
     - [Request Depth of Market with a specified depth](#Request-Depth-of-Market-with-a-specified-depth)
     - [Request a table of the latest up-to-date prices for a list of instruments](#Request-a-table-of-the-latest-up-to-date-prices-for-a-list-of-instruments)
     - [Get the current portfolio and asset allocation statistics](#Get-the-current-portfolio-and-asset-allocation-statistics)
     - [Get a report on operations with a portfolio for a specified period](#Get-a-report-on-operations-with-a-portfolio-for-a-specified-period)
     - [Make a deal on the market](#Make-a-deal-on-the-market)
     - [Open a pending limit or stop order](#Open-a-pending-limit-or-stop-order)
     - [Cancel orders and close positions](#Cancel-orders-and-close-positions)
   - [Module import](#Module-import)
     - [Abstract scenario implementation example](#Abstract-scenario-implementation-example)


## Introduction

If you are engaged in investment, automation and algorithmic trading at the same time, then you have probably heard about [Tinkoff Open API](https://tinkoff.github.io/investAPI/) (there is a good [Swagger-documentation](https://tinkoff.github.io/investAPI/swagger-ui/)). This is an API provided by the Tinkoff Investments broker to automate the operation of exchange trading robots. If you haven't heard it yet, you can create an account [following the link](http://tinkoff.ru/sl/AaX1Et1omnH) and test its capabilities.

When working with any API, there are always technical difficulties: a high entry threshold, the need to study of the big volume of documentation, writing and debugging code to make network requests using the API format. It will take a long time before you get to the point of implementing a trading algorithm.

**[TKSBrokerAPI](https://github.com/Tim55667757/TKSBrokerAPI)** is a simpler tool that can be used as a regular python module or run from the command line, and immediately out of the box get the opportunity to work with an account with a Tinkoff Investments broker: receive information about the state of the portfolio, including elementary analytics, open and close positions, receive general information about the instruments traded on the exchange, request prices and receive reports on operations for the specified period. All data is output immediately to the console: in text view or saved in Markdown format files.

<details>
  <summary>An example of requesting a client portfolio and viewing information in the console</summary>

```commandline
$ tksbrokerapi --overview

TKSBrokerAPI.py     L:1726 INFO    [2022-07-26 12:43:12,279] Statistics of client's portfolio:
# Client's portfolio

* **Actual date:** [2022-07-26 09:43:12] (UTC)
* **Portfolio cost:** 19835.73 RUB
* **Changes:** +415.14 RUB (+2.05%)

## Open positions

| Ticker [FIGI]               | Volume (blocked)                | Lots     | Curr. price  | Avg. price   | Current volume cost | Profit (%)
|-----------------------------|---------------------------------|----------|--------------|--------------|---------------------|----------------------
| Ruble                       |                90.96 (0.30) rub |          |              |              |                     |
|                             |                                 |          |              |              |                     |
| **Currencies:**             |                                 |          |              |              |         9159.71 RUB |
| EUR_RUB__TOM [BBG0013HJJ31] |                 6.29 (0.00) eur | 0.0063   |    59.35 rub |    56.11 rub |          373.31 rub | +22.80 rub (+5.76%)
| CNYRUB_TOM [BBG0013HRTL0]   |                23.00 (0.00) cny | 0.0230   |     8.78 rub |     8.92 rub |          201.95 rub | -3.20 rub (-1.56%)
| CHFRUB_TOM [BBG0013HQ5K4]   |                 1.00 (0.00) chf | 0.0010   |    60.54 rub |    64.00 rub |           60.54 rub | -3.46 rub (-5.41%)
| GBPRUB_TOM [BBG0013HQ5F0]   |                 2.00 (0.00) gbp | 0.0020   |    72.80 rub |    90.10 rub |          145.59 rub | -34.61 rub (-19.21%)
| TRYRUB_TOM [BBG0013J12N1]   |                 1.00 (0.00) try | 0.0010   |     3.26 rub |     4.75 rub |            3.26 rub | -1.50 rub (-31.55%)
| USD000UTSTOM [BBG0013HGFT4] |               143.03 (0.00) usd | 0.1430   |    58.50 rub |    55.88 rub |         8367.25 rub | +395.68 rub (+4.96%)
| HKDRUB_TOM [BBG0013HSW87]   |                 1.00 (0.00) hkd | 0.0010   |     7.79 rub |    11.46 rub |            7.79 rub | -3.67 rub (-32.02%)
|                             |                                 |          |              |              |                     |
| **Stocks:**                 |                                 |          |              |              |          905.80 RUB |
| POSI [TCS00A103X66]         |                           1 (1) | 1        |   905.80 rub |   906.80 rub |          905.80 rub | -1.00 rub (-0.11%)
|                             |                                 |          |              |              |                     |
| **Bonds:**                  |                                 |          |              |              |         3024.30 RUB |
| RU000A101YV8 [TCS00A101YV8] |                           3 (0) | 3        |  1008.10 rub |  1004.40 rub |         3024.30 rub | +11.10 rub (+0.37%)
|                             |                                 |          |              |              |                     |
| **Etfs:**                   |                                 |          |              |              |         6654.96 RUB |
| TGLD [BBG222222222]         |                        1600 (0) | 16       |     0.07 usd |     0.07 usd |          113.76 usd | -3.63 usd (-3.09%)
|                             |                                 |          |              |              |                     |
| **Futures:** no trades      |                                 |          |              |              |                     |

## Opened pending limit-orders: 1

| Ticker [FIGI]               | Order ID       | Lots (exec.) | Current price (% delta) | Target price  | Action    | Type      | Create date (UTC)
|-----------------------------|----------------|--------------|-------------------------|---------------|-----------|-----------|---------------------
| POSI [TCS00A103X66]         | ***********    | 1 (0)        |     905.80 rub (-9.33%) |    999.00 rub | ↓ Sell    | Limit     | 2022-07-26 12:43:05

## Opened stop-orders: 2

| Ticker [FIGI]               | Stop order ID                        | Lots   | Current price (% delta) | Target price  | Limit price   | Action    | Type        | Expire type  | Create date (UTC)   | Expiration (UTC)
|-----------------------------|--------------------------------------|--------|-------------------------|---------------|---------------|-----------|-------------|--------------|---------------------|---------------------
| POSI [TCS00A103X66]         | ********-****-****-****-************ | 1      |     905.80 rub (-9.42%) |   1000.00 rub |        Market | ↓ Sell    | Take profit | Until cancel | 2022-07-26 08:58:02 | Undefined
| IBM [BBG000BLNNH6]          | ********-****-****-****-************ | 1      |         N/A usd (0.00%) |    135.00 usd |        Market | ↓ Sell    | Take profit | Until cancel | 2022-07-26 09:38:44 | Undefined

# Analytics

* **Current total portfolio cost:** 19835.73 RUB
* **Changes:** +415.14 RUB (+2.05%)

## Portfolio distribution by assets

| Type       | Uniques | Percent | Current cost
|------------|---------|---------|-----------------
| Ruble      | 1       | 0.46%   | 90.96 rub
| Currencies | 7       | 46.18%  | 9159.71 rub
| Shares     | 1       | 4.57%   | 905.80 rub
| Bonds      | 1       | 15.25%  | 3024.30 rub
| Etfs       | 1       | 33.55%  | 6654.96 rub

## Portfolio distribution by companies

| Company                                     | Percent | Current cost
|---------------------------------------------|---------|-----------------
| All money cash                              | 46.64%  | 9250.67 rub
| [POSI] Positive Technologies                | 4.57%   | 905.80 rub
| [RU000A101YV8] Позитив Текнолоджиз выпуск 1 | 15.25%  | 3024.30 rub
| [TGLD] Тинькофф Золото                      | 33.55%  | 6654.96 rub

## Portfolio distribution by sectors

| Sector         | Percent | Current cost
|----------------|---------|-----------------
| All money cash | 46.64%  | 9250.67 rub
| it             | 19.81%  | 3930.10 rub
| other          | 33.55%  | 6654.96 rub

## Portfolio distribution by currencies

| Instruments currencies   | Percent | Current cost
|--------------------------|---------|-----------------
| [rub] Российский рубль   | 20.27%  | 4021.06 rub
| [usd] Доллар США         | 75.73%  | 15022.22 rub
| [eur] Евро               | 1.88%   | 373.33 rub
| [cny] Юань               | 1.02%   | 201.95 rub
| [chf] Швейцарский франк  | 0.31%   | 60.54 rub
| [gbp] Фунт стерлингов    | 0.73%   | 145.59 rub
| [try] Турецкая лира      | 0.02%   | 3.26 rub
| [hkd] Гонконгский доллар | 0.04%   | 7.79 rub

TKSBrokerAPI.py     L:1732 INFO    [2022-07-26 12:43:12,303] Client's portfolio is saved to file: [overview.md]
```

</details>

TKSBrokerAPI allows you to automate routine trading operations and implement your trading scenarios, or just receive the necessary information from the broker. Thanks to the rich system of CLI commands, it is quite easy to integrate it into CI/CD automation systems.

In the future, based on this module, ready-made trading scenarios and templates for writing your own scenarios in Python will be posted here in open source.

### Key features

At the time of the latest release, the TKSBrokerAPI tool can:

- Receive from the broker's server a list of all instruments available for the specified account: currencies, stocks, bonds, funds and futures;
  - key `--list` or `-l`;
  - API-method: [`Listing()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Listing).
- Request the broker for information about the instrument, knowing its ticker or FIGI ID;
  - key `--info` or `-i`;
  - API-methods: [`SearchByTicker()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SearchByTicker), [`SearchByFIGI()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SearchByFIGI) and [`ShowInstrumentInfo()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.ShowInstrumentInfo).
- Request the broker for the current exchange prices for the instrument by its ticker or FIGI ID, also you can specify the depth;
  - key `--price` together with the key `--depth`;
  - API-method: [`GetCurrentPrices()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetCurrentPrices).
- Receive a table of the latest prices from the broker server;
  - key `--prices` with the list of requested instruments;
  - API-method: [`GetListOfPrices()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.GetListOfPrices).
- Receive information about the user's portfolio and some analytics on it: distribution of the portfolio by assets, companies, sectors and currencies of assets;
  - key `--overview` or `-o`;
  - API-method: [`Overview()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Overview).
- Receive from the broker server information about completed transactions for the specified period and show it as a table;
  - key `--deals` or `-d`;
  - API-method: [`Deals()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Deals).
- Make market deals, buy or sell assets, satisfying existing orders from sellers or buyers;
  - common key `--trade` and additional keys: `--buy`, `--sell`;
  - API-methods: [`Trade()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Trade), [`Buy()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Buy) and [`Sell()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Sell).
- Open orders of any type: pending limit orders, expire after one trading session, and stop orders, which can be valid until canceled or until a specified date;
  - common key `--order` and additional keys: `--buy-limit`, `--sell-limit`, `--buy-stop`, `--sell-stop`;
  - API-methods: [`Order()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.Order), [`BuyLimit()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.BuyLimit), [`SellLimit()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SellLimit), [`BuyStop()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.BuyStop) and [`SellStop()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.SellStop).
- Close previously opened orders or lists of orders of any type by their ID;
  - keys `--close-order` or `--cancel-order`, `--close-orders` or `--cancel-orders`;
  - API-method: [`CloseOrders()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.CloseOrders).
- Close previously opened positions completely (except for blocked volumes) by specifying an instrument or a list of instruments through their tickers or FIGI ID;
  - key `--close-trade` or `--cancel-trade`;
  - API-method: [`CloseTrades()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.CloseTrades).
- Cancel all previously opened orders and close current positions for all instruments at once, except for blocked volumes and positions for currencies, which must be closed manually;
  - key `--close-all`, you can also specify orders, asset type or specify several keywords after the key `--close-all` separated by a space: `orders`, `shares`, `bonds`, `etfs` or `futures`;
  - API-methods: [`CloseAll()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.CloseAll), [`CloseAllOrders()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.CloseAllOrders) and [`CloseAllTrades()`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.CloseAllTrades).


## Setup

The easiest way is to install via PyPI:

```commandline
pip install tksbrokerapi
```

After that, you can check the installation with the command:

```commandline
pip show tksbrokerapi
```

You can also use the TKSBrokerAPI module by downloading it directly from [repository](https://github.com/Tim55667757/TKSBrokerAPI/) via `git clone` and taking the codebase of any tested [release](https://github.com/Tim55667757/TKSBrokerAPI/releases).

In the first case, the tool will be available in the console through the `tksbrokerapi` command, and in the second case, you will have to run it as a normal python script, through `python TKSBrokerAPI.py` from the source directory.

Further, all examples are written for the case when TKSBrokerAPI is installed via PyPI.


## Auth

### Token

The TINKOFF INVEST API service uses a token for authentication. A token is a set of characters that encodes information about the owner, access rights, and other information required for authorization in the service. The token must be passed to the server with every network request.

The TKSBrokerAPI module takes care of all the work with tokens. There are three options for setting a user token:

- when calling `tksbrokerapi` in the console, specify the key: `--token "your_token_here"`;
- either specify `token` when initializing the class in a python script: [`TKSBrokerAPI.TinkoffBrokerServer(token="your_token_here", ...)`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__);
- or you can pre-set a special variable in the user environment: `TKS_API_TOKEN=your_token_here`.

❗ **Working with the TINKOFF INVEST API without creating and using a token is not possible**. Before you start working with the TKSBrokerAPI module, please open the [brokerage account in Tinkoff Investments](http://tinkoff.ru/sl/AaX1Et1omnH), and then select the type of token you need and create it as indicated [in official documentation](https://tinkoff.github.io/investAPI/token/).

❗ **Important note**: never share your tokens with anyone, don't use them in examples, and don't save them in public code. Anyone can use the token, but all transactions with the broker will be displayed on your behalf. If you want to use your tokens for automation in CI/CD systems, then be sure to use hidden environment variables ([example](https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings) of setting "hidden variables" for Travis CI, and [example](https://docs.gitlab.com/ee/ci/variables/#protected-cicd-variables) of setting "protected variables" for GitLab CI).

### User account ID

The second important parameter for the operation of TKSBrokerAPI is the numeric identifier of the user's account. It is not mandatory, but without specifying it, it will be impossible to perform many operations through the API that are logically tied to a specific user (view a portfolio on a brokerage account, perform trading operations, and many others). You can find this number in any brokerage report, which can be ordered either from the Tinkoff Investments mobile application or in your account on their website. Usually the user account ID is located at the top, in the "header" of reports. You can also requested this number from the Tinkoff Investments technical support chat.

There are three options for setting the user account ID:

- when calling `tksbrokerapi` in the console, specify the key: `--account-id your_id_number"`;
- either specify `accountId` when initializing the class in a python script: [`TKSBrokerAPI.TinkoffBrokerServer(token="...", accountId=your_id_number, ...)`](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html#TinkoffBrokerServer.__init__);
- or you can pre-set a special variable in the user environment: `TKS_ACCOUNT_ID=your_id_number`.


## Usage examples

Next, consider some scenarios for using the TKSBrokerAPI module: when it is launched in the console or as a python script.

❗ By default, level `INFO` information is displayed in the console. In case of any errors, it is recommended to increase the logging level to `DEBUG`. To do this, specify any of the keys together with the command: `--debug-level=10`, `--verbosity=10` or `-v 10`. After that, copy the logs with the problem and create a new bug in the section 👉 [**Issues**](https://github.com/Tim55667757/TKSBrokerAPI/issues/new) 👈, please.

Also, `DEBUG` level information is always output to the log-file `TKSBrokerAPI.log` (it is created in the working directory where `tksbrokerapi` or `python TKSBrokerAPI.py` script is called).

### Command line

When you run the program in the console, you can specify many parameters and perform one action. The format of any commands is as follows:

```commandline
tksbrokerapi [необязательные ключи и параметры] [одно действие]
```

❗ To execute most commands, you must each time specify your token through the `--token` key and the account ID through the `--account-id` key, or set them once with the `TKS_API_TOKEN` and `TKS_ACCOUNT_ID` environment variables (see section ["Auth"](#Auth)).

*Note: in the examples below, the access token and account ID were pre-set via the `TKS_API_TOKEN` and `TKS_ACCOUNT_ID` environment variables, so the `--token` and `--account-id` keys do not appear in the logs.*

#### Reference

The `--help` (`-h`) key is used, no action need to specify. The list of keys relevant for this release and their description will be displayed in the console.

<details>
  <summary>Command for displaying internal help on working with the keys</summary>

```commandline
tksbrokerapi --help
```

Output:

```text
usage: python TKSBrokerAPI.py [some options] [one command]

TKSBrokerAPI is a python API to work with some methods of Tinkoff Open API
using REST protocol. It can view history, orders and market information. Also,
you can open orders and trades. See examples:
https://tim55667757.github.io/TKSBrokerAPI/#Usage-examples

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Option: Tinkoff service's api key. If not set then
                        used environment variable `TKS_API_TOKEN`. See how to
                        use: https://tinkoff.github.io/investAPI/token/
  --account-id ACCOUNT_ID
                        Option: string with an user numeric account ID in
                        Tinkoff Broker. It can be found in any broker's
                        reports (see the contract number). Also, this variable
                        can be set from environment variable `TKS_ACCOUNT_ID`.
  --ticker TICKER, -t TICKER
                        Option: instrument's ticker, e.g. `IBM`, `YNDX`,
                        `GOOGL` etc. Use alias for `USD000UTSTOM` simple as
                        `USD`, `EUR_RUB__TOM` as `EUR`.
  --figi FIGI, -f FIGI  Option: instrument's FIGI, e.g. `BBG006L8G4H1` (for
                        `YNDX`).
  --depth DEPTH         Option: Depth of Market (DOM) can be >=1, 1 by
                        default.
  --output OUTPUT       Option: replace default paths to output files for some
                        commands. If None then used default files.
  --debug-level DEBUG_LEVEL, --verbosity DEBUG_LEVEL, -v DEBUG_LEVEL
                        Option: showing STDOUT messages of minimal debug
                        level, e.g. 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 =
                        ERROR, 50 = CRITICAL. INFO (20) by default.
  --list, -l            Action: get and print all available instruments and
                        some information from broker server. Also, you can
                        define --output key to save list of instruments to
                        file, default: instruments.md.
  --info, -i            Action: get information from broker server about
                        instrument by it's ticker or FIGI. `--ticker` key or
                        `--figi` key must be defined!
  --price               Action: show actual price list for current instrument.
                        Also, you can use --depth key. `--ticker` key or
                        `--figi` key must be defined!
  --prices PRICES [PRICES ...], -p PRICES [PRICES ...]
                        Action: get and print current prices for list of given
                        instruments (by it's tickers or by FIGIs. WARNING!
                        This is too long operation if you request a lot of
                        instruments! Also, you can define --output key to save
                        list of prices to file, default: prices.md.
  --overview, -o        Action: show all open positions, orders and some
                        statistics. Also, you can define --output key to save
                        this information to file, default: overview.md.
  --deals [DEALS [DEALS ...]], -d [DEALS [DEALS ...]]
                        Action: show all deals between two given dates. Start
                        day may be an integer number: -1, -2, -3 days ago.
                        Also, you can use keywords: `today`, `yesterday` (-1),
                        `week` (-7), `month` (-30), `year` (-365). Dates
                        format must be: `%Y-%m-%d`, e.g. 2020-02-03. Also, you
                        can define `--output` key to save all deals to file,
                        default: report.md.
  --trade [TRADE [TRADE ...]]
                        Action: universal action to open market position for
                        defined ticker or FIGI. You must specify 1-5
                        parameters: [direction `Buy` or `Sell] [lots, >= 1]
                        [take profit, >= 0] [stop loss, >= 0] [expiration date
                        for TP/SL orders, Undefined|`%Y-%m-%d %H:%M:%S`]. See
                        examples in readme.
  --buy [BUY [BUY ...]]
                        Action: immediately open BUY market position at the
                        current price for defined ticker or FIGI. You must
                        specify 0-4 parameters: [lots, >= 1] [take profit, >=
                        0] [stop loss, >= 0] [expiration date for TP/SL
                        orders, Undefined|`%Y-%m-%d %H:%M:%S`].
  --sell [SELL [SELL ...]]
                        Action: immediately open SELL market position at the
                        current price for defined ticker or FIGI. You must
                        specify 0-4 parameters: [lots, >= 1] [take profit, >=
                        0] [stop loss, >= 0] [expiration date for TP/SL
                        orders, Undefined|`%Y-%m-%d %H:%M:%S`].
  --order [ORDER [ORDER ...]]
                        Action: universal action to open limit or stop-order
                        in any directions. You must specify 4-7 parameters:
                        [direction `Buy` or `Sell] [order type `Limit` or
                        `Stop`] [lots] [target price] [maybe for stop-order:
                        [limit price, >= 0] [stop type, Limit|SL|TP]
                        [expiration date, Undefined|`%Y-%m-%d %H:%M:%S`]]. See
                        examples in readme.
  --buy-limit BUY_LIMIT BUY_LIMIT
                        Action: open pending BUY limit-order (below current
                        price). You must specify only 2 parameters: [lots]
                        [target price] to open BUY limit-order. If you try to
                        create `Buy` limit-order above current price then
                        broker immediately open `Buy` market order, such as if
                        you do simple `--buy` operation!
  --sell-limit SELL_LIMIT SELL_LIMIT
                        Action: open pending SELL limit-order (above current
                        price). You must specify only 2 parameters: [lots]
                        [target price] to open SELL limit-order. If you try to
                        create `Sell` limit-order below current price then
                        broker immediately open `Sell` market order, such as
                        if you do simple `--sell` operation!
  --buy-stop [BUY_STOP [BUY_STOP ...]]
                        Action: open BUY stop-order. You must specify at least
                        2 parameters: [lots] [target price] to open BUY stop-
                        order. In additional you can specify 3 parameters for
                        stop-order: [limit price, >= 0] [stop type,
                        Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d
                        %H:%M:%S`]. When current price will go up or down to
                        target price value then broker opens a limit order.
                        Stop loss order always executed by market price.
  --sell-stop [SELL_STOP [SELL_STOP ...]]
                        Action: open SELL stop-order. You must specify at
                        least 2 parameters: [lots] [target price] to open SELL
                        stop-order. In additional you can specify 3 parameters
                        for stop-order: [limit price, >= 0] [stop type,
                        Limit|SL|TP] [expiration date, Undefined|`%Y-%m-%d
                        %H:%M:%S`]. When current price will go up or down to
                        target price value then broker opens a limit order.
                        Stop loss order always executed by market price.
  --close-order CLOSE_ORDER, --cancel-order CLOSE_ORDER
                        Action: close only one order by it's `orderId` or
                        `stopOrderId`. You can find out the meaning of these
                        IDs using the key `--overview`
  --close-orders CLOSE_ORDERS [CLOSE_ORDERS ...], --cancel-orders CLOSE_ORDERS [CLOSE_ORDERS ...]
                        Action: close one or list of orders by it's `orderId`
                        or `stopOrderId`. You can find out the meaning of
                        these IDs using the key `--overview`
  --close-trade, --cancel-trade
                        Action: close only one position for instrument defined
                        by `--ticker` key, including for currencies tickers.
  --close-trades CLOSE_TRADES [CLOSE_TRADES ...], --cancel-trades CLOSE_TRADES [CLOSE_TRADES ...]
                        Action: close positions for list of tickers, including
                        for currencies tickers.
  --close-all [CLOSE_ALL [CLOSE_ALL ...]], --cancel-all [CLOSE_ALL [CLOSE_ALL ...]]
                        Action: close all available (not blocked) opened
                        trades and orders, excluding for currencies. Also you
                        can select one or more keywords case insensitive to
                        specify trades type: `orders`, `shares`, `bonds`,
                        `etfs` and `futures`, but not `currencies`. Currency
                        positions you must closes manually using `--buy`,
                        `--sell`, `--close-trade` or `--close-trades`
                        operations.
```

</details>

#### Get a list of all instruments available for trading

The `--list` (`-l`) key is used. At the same time, information is requested from the broker's server on the instruments available for the current account. Additionally, you can use the `--output` key to specify the file where you want to save the received data in Markdown format (by default, `instruments.md` in the current working directory). The `--debug-level=10` key will output all debugging information to the console (not nesessary to specify it).

<details>
  <summary>Command to get a list of all instruments</summary>

```commandline
$ tksbrokerapi --debug-level=10 --list --output ilist.md

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-26 22:04:39,571] TKSBrokerAPI module started at: [2022-07-26 19:04:39] (UTC), it is [2022-07-26 22:04:39] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-26 22:04:39,572] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-26 22:04:39,572] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-26 22:04:39,573] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-26 22:04:39,573] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-26 22:04:39,574] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 22:04:39,581] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 22:04:39,581] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 22:04:39,581] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 22:04:39,581] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 22:04:39,582] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:925  INFO    [2022-07-26 22:04:40,400] # All available instruments from Tinkoff Broker server for current user token

* **Actual on date:** [2022-07-26 19:04] (UTC)
* **Currencies:** [21]
* **Shares:** [1900]
* **Bonds:** [655]
* **Etfs:** [105]
* **Futures:** [284]


## Currencies available. Total: [21]

| Ticker       | Full name                                                      | FIGI         | Cur | Lot    | Step
|--------------|----------------------------------------------------------------|--------------|-----|--------|---------
| USDCHF_TOM   | Швейцарский франк - Доллар США                                 | BBG0013HPJ07 | chf | 1000   | 1e-05
| EUR_RUB__TOM | Евро                                                           | BBG0013HJJ31 | rub | 1000   | 0.0025
| CNYRUB_TOM   | Юань                                                           | BBG0013HRTL0 | rub | 1000   | 0.0001
| ...          | ...                                                            | ...          | ... | ...    | ...   
| RUB000UTSTOM | Российский рубль                                               | RUB000UTSTOM | rub | 1      | 0.0025
| USD000UTSTOM | Доллар США                                                     | BBG0013HGFT4 | rub | 1000   | 0.0025

[... далее идёт аналогичная информация по другим инструментам ...]

TKSBrokerAPI.py     L:931  INFO    [2022-07-26 22:04:41,211] All available instruments are saved to file: [ilist.md]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-26 22:04:41,213] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-26 22:04:41,214] TKSBrokerAPI module work duration: [0:00:01.641989]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-26 22:04:41,215] TKSBrokerAPI module finished: [2022-07-26 19:04:41] (UTC), it is [2022-07-26 22:04:41] local time
```

</details>

#### Get information about an instrument

The key `--info` (`-i`) is used, and one of the two parameters must be specified: the instrument's ticker, or its FIGI ID. They are specified by the `--ticker` (`-t`) and `--figi` (`-f`) keys, respectively. The information displayed to the user is the same for both keys. The difference is in the content and number of fields displayed in the information table, depending on the type of instrument found: it is a currency, stock, bond, fund or futures.

<details>
  <summary>Command to get currency information (using ticker alias, minimal logs)</summary>

```commandline
$ tksbrokerapi  -t CNY -i

TKSBrokerAPI.py     L:607  INFO    [2022-07-26 23:48:31,766] Information about instrument: ticker [CNYRUB_TOM], FIGI [BBG0013HRTL0]
# Information is actual at: [2022-07-26 20:48] (UTC)

| Parameters                                              | Values
|---------------------------------------------------------|---------------------------------------------------------
| Stock ticker:                                           | CNYRUB_TOM
| Full name:                                              | Юань
| Country of instrument:                                  |
|                                                         |
| FIGI (Financial Instrument Global Identifier):          | BBG0013HRTL0
| Exchange:                                               | FX
| Class Code:                                             | CETS
|                                                         |
| Current broker security trading status:                 | Not available for trading
| Buy operations allowed:                                 | Yes
| Sale operations allowed:                                | Yes
| Short positions allowed:                                | No
|                                                         |
| Type of the instrument:                                 | Currencies
| ISO currency name:                                      | cny
| Payment currency:                                       | rub
|                                                         |
| Previous close price of the instrument:                 | 8.6894 rub
| Last deal price of the instrument:                      | 9.2 rub
| Changes between last deal price and last close  %       | 5.88%
| Current limit price, min / max:                         | 8.1891 rub / 9.3463 rub
| Actual price, sell / buy:                               | N/A rub / N/A rub
| Minimum lot to buy:                                     | 1000
| Minimum price increment (step):                         | 0.0001
```

</details>

<details>
  <summary>Command to get information about the stock (using ticker, detailed logs)</summary>

```commandline
$ tksbrokerapi -v 10 --ticker IBM --info

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-26 23:49:58,496] TKSBrokerAPI module started at: [2022-07-26 20:49:58] (UTC), it is [2022-07-26 23:49:58] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-26 23:49:58,497] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-26 23:49:58,497] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-26 23:49:58,498] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-26 23:49:58,498] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-26 23:49:58,499] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 23:49:58,503] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 23:49:58,503] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 23:49:58,503] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 23:49:58,503] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-26 23:49:58,503] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-26 23:49:59,357] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:607  INFO    [2022-07-26 23:49:59,462] Information about instrument: ticker [IBM], FIGI [BBG000BLNNH6]
# Information is actual at: [2022-07-26 20:49] (UTC)

| Parameters                                              | Values
|---------------------------------------------------------|---------------------------------------------------------
| Stock ticker:                                           | IBM
| Full name:                                              | IBM
| Sector:                                                 | it
| Country of instrument:                                  | (US) Соединенные Штаты Америки
|                                                         |
| FIGI (Financial Instrument Global Identifier):          | BBG000BLNNH6
| Exchange:                                               | SPB
| ISIN (International Securities Identification Number):  | US4592001014
| Class Code:                                             | SPBXM
|                                                         |
| Current broker security trading status:                 | Normal trading
| Buy operations allowed:                                 | Yes
| Sale operations allowed:                                | Yes
| Short positions allowed:                                | No
|                                                         |
| Type of the instrument:                                 | Shares
| IPO date:                                               | 1915-11-11 00:00:00
| Payment currency:                                       | usd
|                                                         |
| Previous close price of the instrument:                 | 128.54 usd
| Last deal price of the instrument:                      | 128.2 usd
| Changes between last deal price and last close  %       | -0.26%
| Current limit price, min / max:                         | 126.54 usd / 129.86 usd
| Actual price, sell / buy:                               | 128.08 usd / 128.65 usd
| Minimum lot to buy:                                     | 1
| Minimum price increment (step):                         | 0.01

TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-26 23:49:59,471] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-26 23:49:59,471] TKSBrokerAPI module work duration: [0:00:00.974552]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-26 23:49:59,472] TKSBrokerAPI module finished: [2022-07-26 20:49:59] (UTC), it is [2022-07-26 23:49:59] local time
```

</details>

<details>
  <summary>Command for obtaining information on a bond (with the FIGI ID of the instrument)</summary>

```commandline
$ tksbrokerapi -f TCS00A101YV8 --info

TKSBrokerAPI.py     L:607  INFO    [2022-07-26 23:57:22,581] Information about instrument: ticker [RU000A101YV8], FIGI [TCS00A101YV8]
# Information is actual at: [2022-07-26 20:57] (UTC)

| Parameters                                              | Values
|---------------------------------------------------------|---------------------------------------------------------
| Stock ticker:                                           | RU000A101YV8
| Full name:                                              | Позитив Текнолоджиз выпуск 1
| Sector:                                                 | it
| Country of instrument:                                  | (RU) Российская Федерация
|                                                         |
| FIGI (Financial Instrument Global Identifier):          | TCS00A101YV8
| Exchange:                                               | MOEX_PLUS
| ISIN (International Securities Identification Number):  | RU000A101YV8
| Class Code:                                             | TQCB
|                                                         |
| Current broker security trading status:                 | Break in trading
| Buy operations allowed:                                 | Yes
| Sale operations allowed:                                | Yes
| Short positions allowed:                                | No
|                                                         |
| Type of the instrument:                                 | Bonds
| Payment currency:                                       | rub
| State registration date:                                | 2020-07-21 00:00:00
| Placement date:                                         | 2020-07-29 00:00:00
| Maturity date:                                          | 2023-07-26 00:00:00
|                                                         |
| Previous close price of the instrument:                 | 101. rub
| Last deal price of the instrument:                      | 101. rub
| Changes between last deal price and last close  %       | 0.00%
| Current limit price, min / max:                         | 60.51 rub / 141.17 rub
| Actual price, sell / buy:                               | N/A rub / N/A rub
| Minimum lot to buy:                                     | 1
| Minimum price increment (step):                         | 0.01
```

</details>

<details>
  <summary>Command for obtaining information about the ETF (with the FIGI ID)</summary>

```commandline
$ tksbrokerapi --figi BBG222222222 -i

TKSBrokerAPI.py     L:607  INFO    [2022-07-26 23:59:07,204] Information about instrument: ticker [TGLD], FIGI [BBG222222222]
# Information is actual at: [2022-07-26 20:59] (UTC)

| Parameters                                              | Values
|---------------------------------------------------------|---------------------------------------------------------
| Stock ticker:                                           | TGLD
| Full name:                                              | Тинькофф Золото
| Country of instrument:                                  |
|                                                         |
| FIGI (Financial Instrument Global Identifier):          | BBG222222222
| Exchange:                                               | MOEX
| ISIN (International Securities Identification Number):  | RU000A101X50
| Class Code:                                             | TQTD
|                                                         |
| Current broker security trading status:                 | Break in trading
| Buy operations allowed:                                 | Yes
| Sale operations allowed:                                | Yes
| Short positions allowed:                                | No
|                                                         |
| Type of the instrument:                                 | Etfs
| Released date:                                          | 2020-07-13 00:00:00
| Focusing type:                                          | equity
| Payment currency:                                       | usd
|                                                         |
| Previous close price of the instrument:                 | 0.07110000000000001 usd
| Last deal price of the instrument:                      | 0.07110000000000001 usd
| Changes between last deal price and last close  %       | 0.00%
| Current limit price, min / max:                         | 0.06080000000000001 usd / 0.0815 usd
| Actual price, sell / buy:                               | N/A usd / N/A usd
| Minimum lot to buy:                                     | 100
| Minimum price increment (step):                         | 0.0001
```

</details>

<details>
  <summary>Command to get information about the futures (using its ticker, detailed logs)</summary>

```commandline
$ tksbrokerapi --verbosity=10 --ticker PZH2 --info

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 00:01:48,048] TKSBrokerAPI module started at: [2022-07-26 21:01:48] (UTC), it is [2022-07-27 00:01:48] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 00:01:48,049] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 00:01:48,049] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 00:01:48,049] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 00:01:48,050] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 00:01:48,050] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 00:01:48,056] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 00:01:48,056] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 00:01:48,057] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 00:01:48,057] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 00:01:48,058] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 00:01:48,968] Requesting current prices for instrument with ticker [PZH2] and FIGI [FUTPLZL03220]...
TKSBrokerAPI.py     L:607  INFO    [2022-07-27 00:01:49,075] Information about instrument: ticker [PZH2], FIGI [FUTPLZL03220]
# Information is actual at: [2022-07-26 21:01] (UTC)

| Parameters                                              | Values
|---------------------------------------------------------|---------------------------------------------------------
| Stock ticker:                                           | PZH2
| Full name:                                              | PLZL-3.22 Полюс Золото
| Sector:                                                 | SECTOR_MATERIALS
| Country of instrument:                                  |
|                                                         |
| FIGI (Financial Instrument Global Identifier):          | FUTPLZL03220
| Exchange:                                               | FORTS
| Class Code:                                             | SPBFUT
|                                                         |
| Current broker security trading status:                 | Not available for trading
| Buy operations allowed:                                 | Yes
| Sale operations allowed:                                | Yes
| Short positions allowed:                                | Yes
|                                                         |
| Type of the instrument:                                 | Futures
| Futures type:                                           | DELIVERY_TYPE_PHYSICAL_DELIVERY
| Asset type:                                             | TYPE_SECURITY
| Basic asset:                                            | PLZL
| Basic asset size:                                       | 10.0
| Payment currency:                                       | rub
| First trade date:                                       | 2021-09-02 20:59:59
| Last trade date:                                        | 2022-03-28 21:00:00
| Date of expiration:                                     | 2022-03-30 00:00:00
|                                                         |
| Previous close price of the instrument:                 | 108100. rub
| Last deal price of the instrument:                      | 108100. rub
| Changes between last deal price and last close  %       | 0.00%
| Current limit price, min / max:                         | 0. rub / 0. rub
| Actual price, sell / buy:                               | N/A rub / N/A rub
| Minimum lot to buy:                                     | 1

TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 00:01:49,085] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 00:01:49,085] TKSBrokerAPI module work duration: [0:00:01.036968]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 00:01:49,086] TKSBrokerAPI module finished: [2022-07-26 21:01:49] (UTC), it is [2022-07-27 00:01:49] local time
```

</details>

#### Request Depth of Market with a specified depth

The `--price` key is used, and one of the two parameters must be specified: the instrument's ticker (the `--ticker` or `-t` key), or its FIGI identifier (the `--figi` or `-f` key), respectively . Additionally, you can specify the `--depth` key to set the "depth of the order book". The actual given depth is determined by the broker's policies for a particular instrument, it can be much less than the requested one.

<details>
  <summary>Command for getting Depth of Market</summary>

```commandline
$ tksbrokerapi --ticker IBM --depth=5 --price

TKSBrokerAPI.py     L:871  INFO    [2022-07-27 00:11:35,189] Current prices in order book:

Orders book actual at [2022-07-26 21:11:35] (UTC)
Ticker: [IBM], FIGI: [BBG000BLNNH6], Depth of Market: [5]
----------------------------------------
 Orders of Buyers   | Orders of Sellers
----------------------------------------
 Sell prices (vol.) | Buy prices (vol.)
----------------------------------------
                    | 129.2 (1)
                    | 129.0 (9)
                    | 128.96 (21)
                    | 128.7 (1)
                    | 128.65 (150)
         127.67 (1) |
         127.66 (1) |
        127.65 (60) |
         127.53 (2) |
          127.5 (5) |
----------------------------------------
     Total sell: 69 | Total buy: 182
----------------------------------------
```

</details>

#### Request a table of the latest up-to-date prices for a list of instruments

The `--prices` (`-p`) key is used, and it is also necessary to list the tickers of the instruments or their FIGI identifiers, separated by a space. Additionally, you can specify the `--output` key and specify the name of the file where the price table will be saved in Markdown format (by default, `prices.md` in the current working directory).

<details>
  <summary>Command to request prices for specified instruments</summary>

```commandline
$ tksbrokerapi --prices EUR IBM MSFT GOOGL UNKNOWN_TICKER TCS00A101YV8 POSI BBG000000001 PTZ2 --output some-prices.md

TKSBrokerAPI.py     L:977  WARNING [2022-07-27 00:25:43,224] Instrument [UNKNOWN_TICKER] not in list of available instruments for current token!
TKSBrokerAPI.py     L:1018 INFO    [2022-07-27 00:25:43,606] Only unique instruments are shown:
# Actual prices at: [2022-07-26 21:25 UTC]

| Ticker       | FIGI         | Type       | Prev. close | Last price  | Chg. %   | Day limits min/max  | Actual sell / buy   | Curr.
|--------------|--------------|------------|-------------|-------------|----------|---------------------|---------------------|------
| EUR_RUB__TOM | BBG0013HJJ31 | Currencies |       59.22 |       61.68 |   +4.16% |       55.82 / 62.47 |           N/A / N/A | rub
| IBM          | BBG000BLNNH6 | Shares     |      128.08 |      128.36 |   +0.22% |     126.64 / 129.96 |     128.18 / 128.65 | usd
| MSFT         | BBG000BPH459 | Shares     |      251.90 |      252.23 |   +0.13% |     248.74 / 254.96 |     252.01 / 252.35 | usd
| GOOGL        | BBG009S39JX6 | Shares     |      105.02 |      108.00 |   +2.84% |       97.78 / 119.3 |     107.55 / 107.94 | usd
| RU000A101YV8 | TCS00A101YV8 | Bonds      |      101.00 |      101.00 |    0.00% |      60.51 / 141.17 |           N/A / N/A | rub
| POSI         | TCS00A103X66 | Shares     |      910.00 |      910.00 |    0.00% |      533.2 / 1243.6 |           N/A / N/A | rub
| TRUR         | BBG000000001 | Etfs       |        5.45 |        5.45 |    0.00% |          4.8 / 5.94 |           N/A / N/A | rub
| PTZ2         | FUTPLT122200 | Futures    |      940.40 |      930.00 |   -1.11% |      831.4 / 1024.2 |           N/A / N/A | rub

TKSBrokerAPI.py     L:1024 INFO    [2022-07-27 00:25:43,611] Price list for all instruments saved to file: [some-prices.md]
```

</details>


#### Get the current portfolio and asset allocation statistics

The `--overview` (`-o`) key is used. Additionally, you can specify the `--output` key and specify the file name where to save the portfolio in Markdown format (by default `overview.md` in the current working directory). The `--verbosity=10` key will output all debugging information to the console (not nesessary to specify it).

<details>
  <summary>Command to get user's portfolio</summary>

```commandline
$ tksbrokerapi --verbosity=10 --overview --output portfolio.md

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 18:03:05,365] TKSBrokerAPI module started at: [2022-07-27 15:03:05] (UTC), it is [2022-07-27 18:03:05] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 18:03:05,366] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 18:03:05,367] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 18:03:05,368] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 18:03:05,369] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 18:03:05,370] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 18:03:05,375] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 18:03:05,375] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 18:03:05,375] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 18:03:05,375] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 18:03:05,375] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:1146 DEBUG   [2022-07-27 18:03:06,455] Request portfolio of a client...
TKSBrokerAPI.py     L:1035 DEBUG   [2022-07-27 18:03:06,456] Requesting current actual user's portfolio. Wait, please...
TKSBrokerAPI.py     L:1041 DEBUG   [2022-07-27 18:03:06,659] Records about user's portfolio successfully received
TKSBrokerAPI.py     L:1052 DEBUG   [2022-07-27 18:03:06,660] Requesting current open positions in currencies and instruments. Wait, please...
TKSBrokerAPI.py     L:1058 DEBUG   [2022-07-27 18:03:06,779] Records about current open positions successfully received
TKSBrokerAPI.py     L:1069 DEBUG   [2022-07-27 18:03:06,779] Requesting current actual pending orders. Wait, please...
TKSBrokerAPI.py     L:1075 DEBUG   [2022-07-27 18:03:06,914] [1] records about pending orders successfully received
TKSBrokerAPI.py     L:1086 DEBUG   [2022-07-27 18:03:06,916] Requesting current actual stop orders. Wait, please...
TKSBrokerAPI.py     L:1092 DEBUG   [2022-07-27 18:03:07,027] [3] records about stop orders successfully received
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 18:03:07,039] Requesting current prices for instrument with ticker [RU000A101YV8] and FIGI [TCS00A101YV8]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 18:03:07,144] Requesting current prices for instrument with ticker [POSI] and FIGI [TCS00A103X66]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 18:03:07,235] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:1726 INFO    [2022-07-27 18:03:07,387] Statistics of client's portfolio:
# Client's portfolio

* **Actual date:** [2022-07-27 15:03:07] (UTC)
* **Portfolio cost:** 34501.76 RUB
* **Changes:** +168.23 RUB (+0.49%)

## Open positions

| Ticker [FIGI]               | Volume (blocked)                | Lots     | Curr. price  | Avg. price   | Current volume cost | Profit (%)
|-----------------------------|---------------------------------|----------|--------------|--------------|---------------------|----------------------
| Ruble                       |                 7.05 (0.62) rub |          |              |              |                     |
|                             |                                 |          |              |              |                     |
| **Currencies:**             |                                 |          |              |              |        11186.55 RUB |
| EUR_RUB__TOM [BBG0013HJJ31] |                 6.29 (0.00) eur | 0.0063   |    61.06 rub |    62.98 rub |          384.07 rub | -12.06 rub (-3.04%)
| CNYRUB_TOM [BBG0013HRTL0]   |               264.00 (0.00) cny | 0.2640   |     9.08 rub |     8.95 rub |         2396.99 rub | +35.51 rub (+1.50%)
| CHFRUB_TOM [BBG0013HQ5K4]   |                 1.00 (0.00) chf | 0.0010   |    60.54 rub |    64.00 rub |           60.54 rub | -3.46 rub (-5.41%)
| GBPRUB_TOM [BBG0013HQ5F0]   |                 2.00 (0.00) gbp | 0.0020   |    73.85 rub |    90.10 rub |          147.70 rub | -32.50 rub (-18.04%)
| TRYRUB_TOM [BBG0013J12N1]   |                 1.00 (0.00) try | 0.0010   |     3.34 rub |     4.75 rub |            3.34 rub | -1.41 rub (-29.65%)
| USD000UTSTOM [BBG0013HGFT4] |               135.68 (0.00) usd | 0.1357   |    60.33 rub |    59.40 rub |         8185.91 rub | +126.52 rub (+1.57%)
| HKDRUB_TOM [BBG0013HSW87]   |                 1.00 (0.00) hkd | 0.0010   |     8.00 rub |    11.46 rub |            8.00 rub | -3.46 rub (-30.19%)
|                             |                                 |          |              |              |                     |
| **Stocks:**                 |                                 |          |              |              |         8660.80 RUB |
| POSI [TCS00A103X66]         |                           1 (0) | 1        |   929.80 rub |   906.80 rub |          929.80 rub | +23.00 rub (+2.54%)
| IBM [BBG000BLNNH6]          |                           1 (0) | 1        |   128.14 usd |   128.89 usd |          128.14 usd | -0.75 usd (-0.58%)
|                             |                                 |          |              |              |                     |
| **Bonds:**                  |                                 |          |              |              |         3032.76 RUB |
| RU000A101YV8 [TCS00A101YV8] |                           3 (2) | 3        |  1010.60 rub |  1004.40 rub |         3032.76 rub | +18.60 rub (+0.62%)
|                             |                                 |          |              |              |                     |
| **Etfs:**                   |                                 |          |              |              |        11614.60 RUB |
| TGLD [BBG222222222]         |                        2700 (0) | 27       |     0.07 usd |     0.07 usd |          192.51 usd | -3.31 usd (-1.69%)
|                             |                                 |          |              |              |                     |
| **Futures:** no trades      |                                 |          |              |              |                     |

## Opened pending limit-orders: 1

| Ticker [FIGI]               | Order ID       | Lots (exec.) | Current price (% delta) | Target price  | Action    | Type      | Create date (UTC)
|-----------------------------|----------------|--------------|-------------------------|---------------|-----------|-----------|---------------------
| RU000A101YV8 [TCS00A101YV8] | ***********    | 2 (0)        |     101.13 rub (-0.85%) |    102.00 rub | ↓ Sell    | Limit     | 2022-07-27 16:10:38

## Opened stop-orders: 2

| Ticker [FIGI]               | Stop order ID                        | Lots   | Current price (% delta) | Target price  | Limit price   | Action    | Type        | Expire type  | Create date (UTC)   | Expiration (UTC)
|-----------------------------|--------------------------------------|--------|-------------------------|---------------|---------------|-----------|-------------|--------------|---------------------|---------------------
| POSI [TCS00A103X66]         | ********-****-****-****-************ | 1      |     929.80 rub (-7.02%) |   1000.00 rub |        Market | ↓ Sell    | Take profit | Until cancel | 2022-07-26 08:58:02 | Undefined
| IBM [BBG000BLNNH6]          | ********-****-****-****-************ | 1      |     128.16 usd (-1.42%) |    130.00 usd |        Market | ↓ Sell    | Take profit | Until cancel | 2022-07-26 14:46:07 | Undefined

# Analytics

* **Current total portfolio cost:** 34501.76 RUB
* **Changes:** +168.23 RUB (+0.49%)

## Portfolio distribution by assets

| Type       | Uniques | Percent | Current cost
|------------|---------|---------|-----------------
| Ruble      | 1       | 0.02%   | 7.05 rub
| Currencies | 7       | 32.42%  | 11186.55 rub
| Shares     | 2       | 25.10%  | 8660.80 rub
| Bonds      | 1       | 8.79%   | 3032.76 rub
| Etfs       | 1       | 33.66%  | 11614.60 rub

## Portfolio distribution by companies

| Company                                     | Percent | Current cost
|---------------------------------------------|---------|-----------------
| All money cash                              | 32.44%  | 11193.60 rub
| [POSI] Positive Technologies                | 2.69%   | 929.80 rub
| [IBM] IBM                                   | 22.41%  | 7731.01 rub
| [RU000A101YV8] Позитив Текнолоджиз выпуск 1 | 8.79%   | 3032.76 rub
| [TGLD] Тинькофф Золото                      | 33.66%  | 11614.61 rub

## Portfolio distribution by sectors

| Sector         | Percent | Current cost
|----------------|---------|-----------------
| All money cash | 32.44%  | 11193.60 rub
| it             | 33.89%  | 11693.57 rub
| other          | 33.66%  | 11614.61 rub

## Portfolio distribution by currencies

| Instruments currencies   | Percent | Current cost
|--------------------------|---------|-----------------
| [rub] Российский рубль   | 11.51%  | 3969.61 rub
| [usd] Доллар США         | 79.80%  | 27531.53 rub
| [eur] Евро               | 1.11%   | 384.07 rub
| [cny] Юань               | 6.95%   | 2396.99 rub
| [chf] Швейцарский франк  | 0.18%   | 60.54 rub
| [gbp] Фунт стерлингов    | 0.43%   | 147.70 rub
| [try] Турецкая лира      | 0.01%   | 3.34 rub
| [hkd] Гонконгский доллар | 0.02%   | 8.00 rub

TKSBrokerAPI.py     L:1732 INFO    [2022-07-27 18:03:07,410] Client's portfolio is saved to file: [portfolio.md]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 18:03:07,411] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 18:03:07,411] TKSBrokerAPI module work duration: [0:00:02.045574]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 18:03:07,412] TKSBrokerAPI module finished: [2022-07-27 15:03:07] (UTC), it is [2022-07-27 18:03:07] local time
```

</details>

#### Get a report on operations with a portfolio for a specified period

The key `--deals` (`-d`) is used, after which you need to specify two dates: the start and end dates of the report. They must be in the format `%Y-%m-%d` and separated by a space, e.g. `--deals 2022-07-01 2022-07-27`. In this case, the report will include all transactions from 0:00:00 on the first date to 23:59:59 on the second date.

Instead of the start date, you can specify a negative number — the number of previous days from the current date (`--deals -1`, `-d -2`, `-d -3`, ...), then you do not need to specify the end date. Also, instead of the start date, you can specify one of the keywords: `today`, `yesterday` (-1 day), `week` (-7 days), `month` (-30 days), `year` (-365 days) . In all these cases, a report will be issued for the specified number of previous days up to today and the current time.

Additionally, you can specify the `--output` key to specify the file where to save the report on deals in Markdown format (by default, `report.md` in the current working directory).
 
<details>
  <summary>Command to get a report on operations between two specified dates</summary>

```commandline
$ tksbrokerapi --deals 2022-07-01 2022-07-28 --output deals.md

TKSBrokerAPI.py     L:1972 INFO    [2022-07-28 18:13:18,960] # Client's operations

* **Period:** from [2022-07-01] to [2022-07-28]

## Summary (operations executed only)

| 1                          | 2                             | 3                            | 4                    | 5
|----------------------------|-------------------------------|------------------------------|----------------------|------------------------
| **Actions:**               | Operations executed: 35       | Trading volumes:             |                      |
|                            |   Buy: 19 (54.3%)             |   rub, buy: -25907.12        |                      |
|                            |   Sell: 16 (45.7%)            |   rub, sell: +11873.86       |                      |
|                            |                               |   usd, buy: -664.45          |                      |
|                            |                               |   usd, sell: +281.03         |                      |
|                            |                               |                              |                      |
| **Payments:**              | Deposit on broker account:    | Withdrawals:                 | Dividends income:    | Coupons income:
|                            |   rub: +14000.00              |   —                          |   —                  |   rub: +86.01
|                            |                               |                              |                      |
| **Commissions and taxes:** | Broker commissions:           | Service commissions:         | Margin commissions:  | All taxes/corrections:
|                            |   rub: -75.85                 |   —                          |   —                  |   rub: -11.00
|                            |   usd: -0.30                  |   —                          |   —                  |   —
|                            |                               |                              |                      |

## All operations

| Date and time       | FIGI         | Ticker       | Asset      | Value     | Payment         | Status     | Operation type
|---------------------|--------------|--------------|------------|-----------|-----------------|------------|--------------------------------------------------------------------
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      +86.01 rub | √ Executed | Coupons income
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      -11.00 rub | √ Executed | Withholding personal income tax on bond coupons
|                     |              |              |            |           |                 |            |
| 2022-07-27 20:30:12 | BBG000BLNNH6 | IBM          | Shares     | 2         |               — | × Canceled | Sell securities
| 2022-07-27 20:26:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:26:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -129.28 usd | √ Executed | Buy securities
| 2022-07-27 20:25:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:25:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.89 usd | √ Executed | Sell securities
| 2022-07-27 19:18:43 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 19:18:42 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.80 usd | √ Executed | Buy securities
| 2022-07-27 19:13:29 | BBG000BLNNH6 | IBM          | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-27 16:00:39 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 16:00:38 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.01 usd | √ Executed | Sell securities
| 2022-07-27 15:56:46 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 15:56:45 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.10 usd | √ Executed | Buy securities
| 2022-07-27 13:10:38 | TCS00A101YV8 | RU000A101YV8 | Bonds      | 2         |               — | × Canceled | Sell securities
| 2022-07-27 13:06:38 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | —         |       -6.47 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:06:37 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | 241       |    -2156.28 rub | √ Executed | Buy securities
| 2022-07-27 13:05:42 | BBG222222222 | TGLD         | Etfs       | 1100      |      -78.43 usd | √ Executed | Buy securities
| 2022-07-27 13:04:26 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -35.66 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:04:25 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 200       |   -11885.50 rub | √ Executed | Buy securities
| 2022-07-27 13:03:46 | —            | —            | —          | —         |   +14000.00 rub | √ Executed | Deposit on broker account
|                     |              |              |            |           |                 |            |
| 2022-07-26 14:46:08 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-26 14:46:07 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.89 usd | √ Executed | Buy securities
| 2022-07-26 09:43:05 | TCS00A103X66 | POSI         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-26 09:37:47 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -24.57 rub | √ Executed | Operation fee deduction
| 2022-07-26 09:37:46 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 140       |    -8190.00 rub | √ Executed | Buy securities
| 2022-07-26 08:58:02 | TCS00A103X66 | POSI         | Shares     | —         |       -0.23 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:58:01 | TCS00A103X66 | POSI         | Shares     | 1         |     -906.80 rub | √ Executed | Buy securities
| 2022-07-26 08:56:25 | TCS00A103X66 | POSI         | Shares     | —         |       -1.13 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:56:24 | TCS00A103X66 | POSI         | Shares     | 5         |    +4530.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-25 08:25:59 | TCS00A103X66 | POSI         | Shares     | —         |       -1.17 rub | √ Executed | Operation fee deduction
| 2022-07-25 08:25:58 | TCS00A103X66 | POSI         | Shares     | 5         |    +4676.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-22 14:48:50 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-22 14:48:49 | BBG00JN4FXG8 | SLDB         | Shares     | 3         |       +2.14 usd | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-21 17:21:21 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:17:06 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:16:17 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:11:30 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-21 17:11:29 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       -0.74 usd | √ Executed | Buy securities
|                     |              |              |            |           |                 |            |
| 2022-07-19 07:08:11 | TCS00A103X66 | POSI         | Shares     | —         |       -0.22 rub | √ Executed | Operation fee deduction
| 2022-07-19 07:08:10 | TCS00A103X66 | POSI         | Shares     | 1         |     -864.00 rub | √ Executed | Buy securities
|                     |              |              |            |           |                 |            |
| 2022-07-15 07:00:05 | TCS00A103X66 | POSI         | Shares     | —         |       -0.22 rub | √ Executed | Operation fee deduction
| 2022-07-15 07:00:04 | TCS00A103X66 | POSI         | Shares     | 1         |     +860.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-11 07:46:13 | BBG222222222 | TGLD         | Etfs       | 300       |      -21.45 usd | √ Executed | Buy securities
| 2022-07-08 18:04:04 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-08 18:04:03 | BBG00JN4FXG8 | SLDB         | Shares     | 25        |      +16.26 usd | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-06 17:15:05 | BBG00JN4FXG8 | SLDB         | Shares     | 27        |               — | × Canceled | Sell securities
| 2022-07-06 14:58:23 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-06 14:58:22 | BBG00JN4FXG8 | SLDB         | Shares     | 3         |       +2.16 usd | √ Executed | Sell securities
| 2022-07-06 14:46:40 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-06 14:46:39 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.68 usd | √ Executed | Sell securities
| 2022-07-06 14:40:39 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-06 14:40:38 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.66 usd | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-05 14:24:15 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-05 13:26:56 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-05 13:26:55 | BBG00JN4FXG8 | SLDB         | Shares     | 6         |       -3.59 usd | √ Executed | Buy securities
| 2022-07-05 13:26:31 | BBG222222222 | TGLD         | Etfs       | 300       |      -22.29 usd | √ Executed | Buy securities
| 2022-07-05 13:24:45 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |       -5.38 rub | √ Executed | Operation fee deduction
| 2022-07-05 13:24:44 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 29        |    -1792.56 rub | √ Executed | Buy securities
| 2022-07-05 13:24:26 | BBG00V9V16J8 | GOLD         | Etfs       | —         |       -0.45 rub | √ Executed | Operation fee deduction
| 2022-07-05 13:24:25 | BBG00V9V16J8 | GOLD         | Etfs       | 1972      |    +1797.68 rub | √ Executed | Sell securities
| 2022-07-05 13:21:59 | BBG222222222 | TGLD         | Etfs       | 100       |       -7.44 usd | √ Executed | Buy securities
| 2022-07-05 10:12:22 | BBG00V9V16J8 | GOLD         | Etfs       | —         |       -0.01 rub | √ Executed | Operation fee deduction
| 2022-07-05 10:12:21 | BBG00V9V16J8 | GOLD         | Etfs       | 11        |      +10.18 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-01 19:32:46 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-01 19:32:45 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.58 usd | √ Executed | Sell securities
| 2022-07-01 18:13:04 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-01 18:13:03 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       -0.56 usd | √ Executed | Buy securities
| 2022-07-01 17:46:57 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-01 17:46:56 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-01 17:46:56 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Buy securities
| 2022-07-01 17:46:56 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.55 usd | √ Executed | Sell securities
| 2022-07-01 17:46:56 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-01 17:46:55 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.55 usd | √ Executed | Sell securities
| 2022-07-01 17:46:55 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       +0.55 usd | √ Executed | Sell securities
| 2022-07-01 09:22:15 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | —         |       -0.34 rub | √ Executed | Operation fee deduction
| 2022-07-01 09:22:14 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | 13        |     -111.98 rub | √ Executed | Buy securities
| 2022-07-01 09:20:21 | BBG222222222 | TGLD         | Etfs       | 200       |      -14.88 usd | √ Executed | Buy securities

TKSBrokerAPI.py     L:1978 INFO    [2022-07-28 18:13:18,975] History of a client's operations are saved to file: [deals.md]
```

</details>

<details>
  <summary>Command to get a report on operations for the previous three days</summary>

```commandline
$ tksbrokerapi -d -3

TKSBrokerAPI.py     L:1972 INFO    [2022-07-28 18:29:15,026] # Client's operations

* **Period:** from [2022-07-25] to [2022-07-28]

## Summary (operations executed only)

| 1                          | 2                             | 3                            | 4                    | 5
|----------------------------|-------------------------------|------------------------------|----------------------|------------------------
| **Actions:**               | Operations executed: 13       | Trading volumes:             |                      |
|                            |   Buy: 9 (69.2%)              |   rub, buy: -23138.58        |                      |
|                            |   Sell: 4 (30.8%)             |   rub, sell: +9206.00        |                      |
|                            |                               |   usd, buy: -593.50          |                      |
|                            |                               |   usd, sell: +256.90         |                      |
|                            |                               |                              |                      |
| **Payments:**              | Deposit on broker account:    | Withdrawals:                 | Dividends income:    | Coupons income:
|                            |   rub: +14000.00              |   —                          |   —                  |   rub: +86.01
|                            |                               |                              |                      |
| **Commissions and taxes:** | Broker commissions:           | Service commissions:         | Margin commissions:  | All taxes/corrections:
|                            |   rub: -69.23                 |   —                          |   —                  |   rub: -11.00
|                            |   usd: -0.18                  |   —                          |   —                  |   —
|                            |                               |                              |                      |

## All operations

| Date and time       | FIGI         | Ticker       | Asset      | Value     | Payment         | Status     | Operation type
|---------------------|--------------|--------------|------------|-----------|-----------------|------------|--------------------------------------------------------------------
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      +86.01 rub | √ Executed | Coupons income
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      -11.00 rub | √ Executed | Withholding personal income tax on bond coupons
|                     |              |              |            |           |                 |            |
| 2022-07-27 20:30:12 | BBG000BLNNH6 | IBM          | Shares     | 2         |               — | × Canceled | Sell securities
| 2022-07-27 20:26:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:26:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -129.28 usd | √ Executed | Buy securities
| 2022-07-27 20:25:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:25:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.89 usd | √ Executed | Sell securities
| 2022-07-27 19:18:43 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 19:18:42 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.80 usd | √ Executed | Buy securities
| 2022-07-27 19:13:29 | BBG000BLNNH6 | IBM          | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-27 16:00:39 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 16:00:38 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.01 usd | √ Executed | Sell securities
| 2022-07-27 15:56:46 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 15:56:45 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.10 usd | √ Executed | Buy securities
| 2022-07-27 13:10:38 | TCS00A101YV8 | RU000A101YV8 | Bonds      | 2         |               — | × Canceled | Sell securities
| 2022-07-27 13:06:38 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | —         |       -6.47 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:06:37 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | 241       |    -2156.28 rub | √ Executed | Buy securities
| 2022-07-27 13:05:42 | BBG222222222 | TGLD         | Etfs       | 1100      |      -78.43 usd | √ Executed | Buy securities
| 2022-07-27 13:04:26 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -35.66 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:04:25 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 200       |   -11885.50 rub | √ Executed | Buy securities
| 2022-07-27 13:03:46 | —            | —            | —          | —         |   +14000.00 rub | √ Executed | Deposit on broker account
|                     |              |              |            |           |                 |            |
| 2022-07-26 14:46:08 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-26 14:46:07 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.89 usd | √ Executed | Buy securities
| 2022-07-26 09:43:05 | TCS00A103X66 | POSI         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-26 09:37:47 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -24.57 rub | √ Executed | Operation fee deduction
| 2022-07-26 09:37:46 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 140       |    -8190.00 rub | √ Executed | Buy securities
| 2022-07-26 08:58:02 | TCS00A103X66 | POSI         | Shares     | —         |       -0.23 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:58:01 | TCS00A103X66 | POSI         | Shares     | 1         |     -906.80 rub | √ Executed | Buy securities
| 2022-07-26 08:56:25 | TCS00A103X66 | POSI         | Shares     | —         |       -1.13 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:56:24 | TCS00A103X66 | POSI         | Shares     | 5         |    +4530.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-25 08:25:59 | TCS00A103X66 | POSI         | Shares     | —         |       -1.17 rub | √ Executed | Operation fee deduction
| 2022-07-25 08:25:58 | TCS00A103X66 | POSI         | Shares     | 5         |    +4676.00 rub | √ Executed | Sell securities

TKSBrokerAPI.py     L:1978 INFO    [2022-07-28 18:29:15,032] History of a client's operations are saved to file: [report.md]
```

</details>

<details>
  <summary>Command to get a report on operations for the last week</summary>

```commandline
$ tksbrokerapi -d week

TKSBrokerAPI.py     L:1972 INFO    [2022-07-28 18:29:59,035] # Client's operations

* **Period:** from [2022-07-21] to [2022-07-28]

## Summary (operations executed only)

| 1                          | 2                             | 3                            | 4                    | 5
|----------------------------|-------------------------------|------------------------------|----------------------|------------------------
| **Actions:**               | Operations executed: 15       | Trading volumes:             |                      |
|                            |   Buy: 10 (66.7%)             |   rub, buy: -23138.58        |                      |
|                            |   Sell: 5 (33.3%)             |   rub, sell: +9206.00        |                      |
|                            |                               |   usd, buy: -594.24          |                      |
|                            |                               |   usd, sell: +259.04         |                      |
|                            |                               |                              |                      |
| **Payments:**              | Deposit on broker account:    | Withdrawals:                 | Dividends income:    | Coupons income:
|                            |   rub: +14000.00              |   —                          |   —                  |   rub: +86.01
|                            |                               |                              |                      |
| **Commissions and taxes:** | Broker commissions:           | Service commissions:         | Margin commissions:  | All taxes/corrections:
|                            |   rub: -69.23                 |   —                          |   —                  |   rub: -11.00
|                            |   usd: -0.20                  |   —                          |   —                  |   —
|                            |                               |                              |                      |

## All operations

| Date and time       | FIGI         | Ticker       | Asset      | Value     | Payment         | Status     | Operation type
|---------------------|--------------|--------------|------------|-----------|-----------------|------------|--------------------------------------------------------------------
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      -11.00 rub | √ Executed | Withholding personal income tax on bond coupons
| 2022-07-28 05:00:08 | TCS00A101YV8 | RU000A101YV8 | Bonds      | —         |      +86.01 rub | √ Executed | Coupons income
|                     |              |              |            |           |                 |            |
| 2022-07-27 20:30:12 | BBG000BLNNH6 | IBM          | Shares     | 2         |               — | × Canceled | Sell securities
| 2022-07-27 20:26:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:26:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -129.28 usd | √ Executed | Buy securities
| 2022-07-27 20:25:41 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 20:25:40 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.89 usd | √ Executed | Sell securities
| 2022-07-27 19:18:43 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 19:18:42 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.80 usd | √ Executed | Buy securities
| 2022-07-27 19:13:29 | BBG000BLNNH6 | IBM          | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-27 16:00:39 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 16:00:38 | BBG000BLNNH6 | IBM          | Shares     | 1         |     +128.01 usd | √ Executed | Sell securities
| 2022-07-27 15:56:46 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-27 15:56:45 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.10 usd | √ Executed | Buy securities
| 2022-07-27 13:10:38 | TCS00A101YV8 | RU000A101YV8 | Bonds      | 2         |               — | × Canceled | Sell securities
| 2022-07-27 13:06:38 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | —         |       -6.47 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:06:37 | BBG0013HRTL0 | CNYRUB_TOM   | Currencies | 241       |    -2156.28 rub | √ Executed | Buy securities
| 2022-07-27 13:05:42 | BBG222222222 | TGLD         | Etfs       | 1100      |      -78.43 usd | √ Executed | Buy securities
| 2022-07-27 13:04:26 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -35.66 rub | √ Executed | Operation fee deduction
| 2022-07-27 13:04:25 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 200       |   -11885.50 rub | √ Executed | Buy securities
| 2022-07-27 13:03:46 | —            | —            | —          | —         |   +14000.00 rub | √ Executed | Deposit on broker account
|                     |              |              |            |           |                 |            |
| 2022-07-26 14:46:08 | BBG000BLNNH6 | IBM          | Shares     | —         |       -0.03 usd | √ Executed | Operation fee deduction
| 2022-07-26 14:46:07 | BBG000BLNNH6 | IBM          | Shares     | 1         |     -128.89 usd | √ Executed | Buy securities
| 2022-07-26 09:43:05 | TCS00A103X66 | POSI         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-26 09:37:47 | BBG0013HGFT4 | USD000UTSTOM | Currencies | —         |      -24.57 rub | √ Executed | Operation fee deduction
| 2022-07-26 09:37:46 | BBG0013HGFT4 | USD000UTSTOM | Currencies | 140       |    -8190.00 rub | √ Executed | Buy securities
| 2022-07-26 08:58:02 | TCS00A103X66 | POSI         | Shares     | —         |       -0.23 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:58:01 | TCS00A103X66 | POSI         | Shares     | 1         |     -906.80 rub | √ Executed | Buy securities
| 2022-07-26 08:56:25 | TCS00A103X66 | POSI         | Shares     | —         |       -1.13 rub | √ Executed | Operation fee deduction
| 2022-07-26 08:56:24 | TCS00A103X66 | POSI         | Shares     | 5         |    +4530.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-25 08:25:59 | TCS00A103X66 | POSI         | Shares     | —         |       -1.17 rub | √ Executed | Operation fee deduction
| 2022-07-25 08:25:58 | TCS00A103X66 | POSI         | Shares     | 5         |    +4676.00 rub | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-22 14:48:50 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-22 14:48:49 | BBG00JN4FXG8 | SLDB         | Shares     | 3         |       +2.14 usd | √ Executed | Sell securities
|                     |              |              |            |           |                 |            |
| 2022-07-21 17:21:21 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:17:06 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:16:17 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |               — | × Canceled | Sell securities
| 2022-07-21 17:11:30 | BBG00JN4FXG8 | SLDB         | Shares     | —         |       -0.01 usd | √ Executed | Operation fee deduction
| 2022-07-21 17:11:29 | BBG00JN4FXG8 | SLDB         | Shares     | 1         |       -0.74 usd | √ Executed | Buy securities

TKSBrokerAPI.py     L:1978 INFO    [2022-07-28 18:29:59,045] History of a client's operations are saved to file: [report.md]
```

</details>

#### Make a deal on the market

At the beginning, you should specify the `--ticker` or `--figi` key to specify the instrument for which there will be a market order. To make a deal "at the market", that is, at current prices in the order book, use the common key `--trade`, after which you need to specify from 1 to 5 parameters in the strict order of their sequence:

- direction: `Buy` or `Sell` — required parameter;
- optional parameters:
  - number of instrument lots, integer >= 1, default 1;
  - take profit level, fractional number >= 0, default 0 (if 0, no take profit order will be placed);
  - stop loss level, fractional number >= 0, default 0 (if 0, stop loss order will not be placed);
  - expiration date of take profit and stop loss orders, by default the string `Undefined` (in this case orders will be valid until canceled) or you can set the date in the format `%Y-%m-%d %H:%M:% S`.

You can also use more simple keys to perform buy and sell operations on the market `--buy` or `--sell`, for which you can set up to 4 optional parameters:

- number of instrument lots, integer >= 1, default 1;
- take profit level, fractional number >= 0, default 0 (if 0, no take profit order will be placed);
- stop loss level, fractional number >= 0, default 0 (if 0, stop loss order will not be placed);
- expiration date of take profit and stop loss orders, by default the string `Undefined` (in this case orders will be valid until canceled) or you can set the date in the format `%Y-%m-%d %H:%M:% S`.
 
<details>
  <summary>Command for buying and placing take profit and stop loss orders</summary>

```commandline
$ tksbrokerapi --ticker IBM --trade Buy 1 131.5 125.1 "2022-07-28 12:00:00"

TKSBrokerAPI.py     L:2202 INFO    [2022-07-27 18:56:49,032] [Buy] market order [447445558780] was executed: ticker [IBM], FIGI [BBG000BLNNH6], lots [1]. Total order price: [128.1000 usd] (with commission: [0.04 usd]). Average price of lot: [128.10 usd]
TKSBrokerAPI.py     L:2476 INFO    [2022-07-27 18:56:49,389] Stop-order [182892f7-9533-4817-94d9-613545a01ee1] was created: ticker [IBM], FIGI [BBG000BLNNH6], action [Sell], lots [1], target price [131.50 usd], limit price [131.50 usd], stop-order type [Take profit] and expiration date in UTC [2022-07-28 09:00:00]
TKSBrokerAPI.py     L:2476 INFO    [2022-07-27 18:56:49,683] Stop-order [4ca044e8-607a-4636-ad27-3a9139cc964a] was created: ticker [IBM], FIGI [BBG000BLNNH6], action [Sell], lots [1], target price [125.10 usd], limit price [125.10 usd], stop-order type [Stop loss] and expiration date in UTC [2022-07-28 09:00:00]
```

</details>

<details>
  <summary>Command for selling a previously purchased instrument (without specifying SL/TP orders, with detailed logs)</summary>

```commandline
$ tksbrokerapi -v 10 --ticker IBM --sell 1

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 19:00:39,673] TKSBrokerAPI module started at: [2022-07-27 16:00:39] (UTC), it is [2022-07-27 19:00:39] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 19:00:39,674] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 19:00:39,675] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 19:00:39,676] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 19:00:39,677] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 19:00:39,678] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 19:00:39,682] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 19:00:39,682] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 19:00:39,682] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 19:00:39,682] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 19:00:39,683] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 19:00:40,812] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:2184 DEBUG   [2022-07-27 19:00:40,922] Opening [Sell] market order: ticker [IBM], FIGI [BBG000BLNNH6], lots [1], TP [0.0000], SL [0.0000], expiration date of TP/SL orders [Undefined]. Wait, please...
TKSBrokerAPI.py     L:2202 INFO    [2022-07-27 19:00:41,201] [Sell] market order [447451039340] was executed: ticker [IBM], FIGI [BBG000BLNNH6], lots [1]. Total order price: [128.0100 usd] (with commission: [0.04 usd]). Average price of lot: [128.01 usd]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 19:00:41,203] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 19:00:41,204] TKSBrokerAPI module work duration: [0:00:01.530060]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 19:00:41,204] TKSBrokerAPI module finished: [2022-07-27 16:00:41] (UTC), it is [2022-07-27 19:00:41] local time
```

</details>

#### Open a pending limit or stop order

At the beginning, you should specify the `--ticker` or `--figi` key to specify the instrument for which the order will be placed. To open a pending order of any type, you can use the common key `--order`, after which you need to specify from 4 to 7 parameters in strict order:

- direction: `Buy` or `Sell` — required parameter;
- order type: `Limit` (valid until the end of the trading session) or `Stop` (valid until canceled or until the specified date) — required parameter;
- number of instrument lots, integer >= 1 — required parameter;
- target trigger price of the initial order, fractional number >= 0 — required parameter;
- optional parameters and only for stop orders:
  - price of the opened limit order, fractional number >= 0, default 0 (if 0, a market order will be immediately placed instead of a limit order, when the trigger price of the initial stop order is reached);
  - type of order opened upon reaching the trigger price of the initial stop order, by default it is the string `Limit` or you can specify `SL`, `TP` to open a stop loss or take profit order;
    - stop-loss order is always opened at the market price;
  - date of cancellation of take profit and stop loss orders, by default the string `Undefined` (in this case orders will be valid until canceled) or you can set the date in the format `%Y-%m-%d %H:%M:% S`.

You can use more simple keys to place pending limit orders (valid until the end of the trading session) `--buy-limit` or `--sell-limit`, for which you need to specify only 2 required parameters:

- number of instrument lots, integer >= 1 — required parameter;
- target price for triggering a limit order, fractional number >= 0 — required parameter;
  - for a `--buy-limit` order, the target price must be lower than the current price, and if it is higher, the broker will immediately open a market order to buy, as if the `--buy` command was executed;
  - for a `--sell-limit` order, the target price must be higher than the current price, and if it is lower, the broker will immediately open a market order to sell, as if the `--sell` command was executed.

You can use more simple keys to place pending stop orders (valid until canceled or until a specified date) `--buy-stop` or `--sell-stop`, for which you only need to specify 2 required parameters and 3 optional:

- number of instrument lots, integer >= 1 — required parameter;
- target stop order trigger price, fractional number >= 0 — required parameter;
- optional parameters:
  - price of the opened limit order, fractional number >= 0, default 0 (if 0, a market order will be immediately placed instead of a limit order, when the trigger price of the initial stop order is reached);
  - type of order opened upon reaching the trigger price of the initial stop order, by default it is the string `Limit` or you can specify `SL`, `TP` to open a stop loss or take profit order;
    - stop-loss order is always opened at the market price;
  - date of cancellation of take profit and stop loss orders, by default the string `Undefined` (in this case orders will be valid until canceled) or you can set the date in the format `%Y-%m-%d %H:%M:% S`.

<details>
  <summary>Command for placing a stop order of the take profit type for sale with the date of cancellation</summary>

```commandline
$ tksbrokerapi -v 10 --ticker IBM --order Sell Stop  1 130.2 130.1 TP  "2022-07-28 12:20:00"

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 22:15:20,137] TKSBrokerAPI module started at: [2022-07-27 19:15:20] (UTC), it is [2022-07-27 22:15:20] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 22:15:20,138] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 22:15:20,139] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 22:15:20,141] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 22:15:20,141] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 22:15:20,142] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:15:20,148] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:15:20,148] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:15:20,148] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:15:20,148] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:15:20,148] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 22:15:21,400] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:2443 DEBUG   [2022-07-27 22:15:21,500] Creating stop-order: ticker [IBM], FIGI [BBG000BLNNH6], action [Sell], lots [1], target price [130.20 usd], limit price [130.10 usd], stop-order type [TP] and local expiration date [2022-07-28 12:20:00]. Wait, please...
TKSBrokerAPI.py     L:2476 INFO    [2022-07-27 22:15:21,671] Stop-order [********-****-****-****-************] was created: ticker [IBM], FIGI [BBG000BLNNH6], action [Sell], lots [1], target price [130.20 usd], limit price [130.10 usd], stop-order type [Take profit] and expiration date in UTC [2022-07-28 09:20:00]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 22:15:21,673] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 22:15:21,674] TKSBrokerAPI module work duration: [0:00:01.535746]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 22:15:21,675] TKSBrokerAPI module finished: [2022-07-27 19:15:21] (UTC), it is [2022-07-27 22:15:21] local time
```

</details>

<details>
  <summary>Command for placing a take-profit stop order with a sale at the market price, when the target level is reached</summary>

```commandline
$ tksbrokerapi -t IBM --sell-stop 2 140 0 TP

TKSBrokerAPI.py     L:2476 INFO    [2022-07-27 23:29:29,614] Stop-order [********-****-****-****-************] was created: ticker [IBM], FIGI [BBG000BLNNH6], action [Sell], lots [2], target price [140.00 usd], limit price [140.00 usd], stop-order type [Take profit] and expiration date in UTC [Undefined]
```

</details>

<details>
  <summary>Command for placing a buy limit order</summary>

```commandline
$ tksbrokerapi --debug-level=10 --ticker IBM --buy-limit 1 128.8

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 22:18:41,111] TKSBrokerAPI module started at: [2022-07-27 19:18:41] (UTC), it is [2022-07-27 22:18:41] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 22:18:41,111] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 22:18:41,111] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 22:18:41,111] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 22:18:41,111] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 22:18:41,111] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:18:41,118] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:18:41,119] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:18:41,119] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:18:41,119] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 22:18:41,120] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 22:18:42,032] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:2398 DEBUG   [2022-07-27 22:18:42,134] Creating pending limit-order: ticker [IBM], FIGI [BBG000BLNNH6], action [Buy], lots [1] and the target price [128.80 usd]. Wait, please...
TKSBrokerAPI.py     L:2417 INFO    [2022-07-27 22:18:42,358] Limit-order [************] was created: ticker [IBM], FIGI [BBG000BLNNH6], action [Buy], lots [1], target price [128.80 usd]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 22:18:42,359] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 22:18:42,359] TKSBrokerAPI module work duration: [0:00:01.248221]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 22:18:42,359] TKSBrokerAPI module finished: [2022-07-27 19:18:42] (UTC), it is [2022-07-27 22:18:42] local time
```

</details>

#### Cancel orders and close positions

Order IDs and instrument tickers for which positions are open can be found in the client's portfolio by running the `tksbrokerapi --overview` command. They will be needed for the operations below.

To close one order of any type by its ID, you can use the `--close-order` (`--cancel-order`) key followed by a unique order ID. To close orders by list, you can use the similar key `--close-orders` (`--cancel-orders`), after which followed all order identifiers.

To close a previously opened position (both "long" or "short") use the `--close-trade` (`--cancel-trade`) key, preceded by the instrument with the `--ticker key `. In fact, a market order is opened with the direction opposite to the open position. To close positions for several instruments, you can use the similar key `--close-trades` (`--cancel-trades`), after which define the required tickers (the `--ticker` key is no longer required).

You can also use the common key `--close-all` (`--cancel-all`). If you specify it without parameters, then an attempt will be made to close all instruments and orders, except for those that are blocked or not available for trading. First, all orders will be closed, otherwise, for example, limit orders may block the closing of part of the available volumes for instruments. Then, in order, positions will be closed for all instruments: stocks, bonds, ETFs and futures. This key is more convenient when you need to urgently close all positions than to perform these operations one by one.

❗ It is important to note that in the current version of TKSBrokerAPI, open currency positions will not be closed with the `--close-all` (`--cancel-all`) key. This is because other instruments may use different base currencies. In addition, the user may not want to reduce their currency positions in order to buy other instruments with these funds in the future. If necessary, currency positions can be closed manually using the keys `--buy`, `--sell`, `--close-trade` or `--close-trades`.

To selectively reduce positions, you can use the `--close-all` (`--cancel-all`) key, followed by one or more instrument's types, separated by spaces:
- `orders` — close all orders (both limit and stop orders),
- `shares` — close all stock positions,
- `bonds` — close all positions on bonds,
- `etfs` — close all ETFs positions,
- `futures` — close all futures positions,
- but, you can not specify `currencies` — to close all positions in currencies, due to the reasons described above.

<details>
  <summary>Command to cancel one stop order by its ID</summary>

```commandline
$ tksbrokerapi -v 10 --cancel-order ********-****-****-****-************

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 23:16:55,978] TKSBrokerAPI module started at: [2022-07-27 20:16:55] (UTC), it is [2022-07-27 23:16:55] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 23:16:55,979] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 23:16:55,980] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 23:16:55,981] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 23:16:55,982] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 23:16:55,983] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:16:55,989] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:16:55,989] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:16:55,989] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:16:55,989] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:16:55,989] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:1069 DEBUG   [2022-07-27 23:16:56,959] Requesting current actual pending orders. Wait, please...
TKSBrokerAPI.py     L:1075 DEBUG   [2022-07-27 23:16:57,077] [1] records about pending orders successfully received
TKSBrokerAPI.py     L:1086 DEBUG   [2022-07-27 23:16:57,078] Requesting current actual stop orders. Wait, please...
TKSBrokerAPI.py     L:1092 DEBUG   [2022-07-27 23:16:57,187] [6] records about stop orders successfully received
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:16:57,188] Cancelling stop order with ID: [********-****-****-****-************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:16:57,317] Success time marker received from server: [2022-07-27T20:16:57.288786707Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:16:57,318] Stop order with ID [********-****-****-****-************] successfully cancel
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 23:16:57,319] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 23:16:57,319] TKSBrokerAPI module work duration: [0:00:01.340621]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 23:16:57,320] TKSBrokerAPI module finished: [2022-07-27 20:16:57] (UTC), it is [2022-07-27 23:16:57] local time
```

</details>

<details>
  <summary>Command to close a position on ETF (an example of an unsuccessful attempt, since the market is already closed)</summary>

```commandline
$ tksbrokerapi -v 10 --ticker TGLD --close-trade

TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 23:20:32,745] TKSBrokerAPI module started at: [2022-07-27 20:20:32] (UTC), it is [2022-07-27 23:20:32] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 23:20:32,746] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 23:20:32,746] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 23:20:32,746] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 23:20:32,747] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 23:20:32,747] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:20:32,751] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:20:32,751] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:20:32,752] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:20:32,752] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:20:32,752] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:1035 DEBUG   [2022-07-27 23:20:34,316] Requesting current actual user's portfolio. Wait, please...
TKSBrokerAPI.py     L:1041 DEBUG   [2022-07-27 23:20:34,468] Records about user's portfolio successfully received
TKSBrokerAPI.py     L:1052 DEBUG   [2022-07-27 23:20:34,469] Requesting current open positions in currencies and instruments. Wait, please...
TKSBrokerAPI.py     L:1058 DEBUG   [2022-07-27 23:20:34,582] Records about current open positions successfully received
TKSBrokerAPI.py     L:1069 DEBUG   [2022-07-27 23:20:34,583] Requesting current actual pending orders. Wait, please...
TKSBrokerAPI.py     L:1075 DEBUG   [2022-07-27 23:20:34,682] [1] records about pending orders successfully received
TKSBrokerAPI.py     L:1086 DEBUG   [2022-07-27 23:20:34,683] Requesting current actual stop orders. Wait, please...
TKSBrokerAPI.py     L:1092 DEBUG   [2022-07-27 23:20:34,793] [5] records about stop orders successfully received
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:34,805] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:34,907] Requesting current prices for instrument with ticker [POSI] and FIGI [TCS00A103X66]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:34,993] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:35,077] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:35,192] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:2264 DEBUG   [2022-07-27 23:20:35,285] All opened instruments by it's tickers names: ['EUR_RUB__TOM', 'CNYRUB_TOM', 'CHFRUB_TOM', 'GBPRUB_TOM', 'TRYRUB_TOM', 'USD000UTSTOM', 'HKDRUB_TOM', 'POSI', 'IBM', 'RU000A101YV8', 'TGLD']
TKSBrokerAPI.py     L:2290 DEBUG   [2022-07-27 23:20:35,286] Closing trade of instrument: ticker [TGLD], FIGI[BBG222222222], lots [2700]. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:20:35,286] Requesting current prices for instrument with ticker [TGLD] and FIGI [BBG222222222]...
TKSBrokerAPI.py     L:2184 DEBUG   [2022-07-27 23:20:35,386] Opening [Sell] market order: ticker [TGLD], FIGI [BBG222222222], lots [27.0], TP [0.0000], SL [0.0000], expiration date of TP/SL orders [Undefined]. Wait, please... TKSBrokerAPI.py     L:358  DEBUG   [2022-07-27 23:20:35,485]     - not oK status code received: [400] {"code":3,"message":"instrument is not available for trading","description":"30079"}
TKSBrokerAPI.py     L:368  ERROR   [2022-07-27 23:20:35,486] Not `oK` status received from broker server!
TKSBrokerAPI.py     L:369  ERROR   [2022-07-27 23:20:35,486]     - message: [400] {"code":3,"message":"instrument is not available for trading","description":"30079"}
TKSBrokerAPI.py     L:2206 WARNING [2022-07-27 23:20:35,487] Not `oK` status received! Market order not created. See full debug log or try again and open order later.
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 23:20:35,488] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 23:20:35,488] TKSBrokerAPI module work duration: [0:00:02.742544]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 23:20:35,488] TKSBrokerAPI module finished: [2022-07-27 20:20:35] (UTC), it is [2022-07-27 23:20:35] local time
```

</details>

<details>
  <summary>Command to cancel all orders and close positions on non-blocked shares</summary>

```commandline
$ tksbrokerapi --debug-level=10 --close-all orders shares
TKSBrokerAPI.py     L:2804 DEBUG   [2022-07-27 23:25:36,481] TKSBrokerAPI module started at: [2022-07-27 20:25:36] (UTC), it is [2022-07-27 23:25:36] local time
TKSBrokerAPI.py     L:198  DEBUG   [2022-07-27 23:25:36,482] Bearer token for Tinkoff OpenApi set up from environment variable `TKS_API_TOKEN`. See https://tinkoff.github.io/investAPI/token/
TKSBrokerAPI.py     L:210  DEBUG   [2022-07-27 23:25:36,483] String with user's numeric account ID in Tinkoff Broker set up from environment variable `TKS_ACCOUNT_ID`
TKSBrokerAPI.py     L:240  DEBUG   [2022-07-27 23:25:36,484] Broker API server: https://invest-public-api.tinkoff.ru/rest
TKSBrokerAPI.py     L:411  DEBUG   [2022-07-27 23:25:36,485] Requesting all available instruments from broker for current user token. Wait, please...
TKSBrokerAPI.py     L:412  DEBUG   [2022-07-27 23:25:36,485] CPU usages for parallel requests: [7]
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:25:36,492] Requesting available [Currencies] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:25:36,492] Requesting available [Shares] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:25:36,492] Requesting available [Bonds] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:25:36,492] Requesting available [Etfs] list. Wait, please...
TKSBrokerAPI.py     L:389  DEBUG   [2022-07-27 23:25:36,492] Requesting available [Futures] list. Wait, please...
TKSBrokerAPI.py     L:1035 DEBUG   [2022-07-27 23:25:37,568] Requesting current actual user's portfolio. Wait, please...
TKSBrokerAPI.py     L:1041 DEBUG   [2022-07-27 23:25:37,742] Records about user's portfolio successfully received
TKSBrokerAPI.py     L:1052 DEBUG   [2022-07-27 23:25:37,743] Requesting current open positions in currencies and instruments. Wait, please...
TKSBrokerAPI.py     L:1058 DEBUG   [2022-07-27 23:25:37,831] Records about current open positions successfully received
TKSBrokerAPI.py     L:1069 DEBUG   [2022-07-27 23:25:37,832] Requesting current actual pending orders. Wait, please...
TKSBrokerAPI.py     L:1075 DEBUG   [2022-07-27 23:25:37,934] [1] records about pending orders successfully received
TKSBrokerAPI.py     L:1086 DEBUG   [2022-07-27 23:25:37,934] Requesting current actual stop orders. Wait, please...
TKSBrokerAPI.py     L:1092 DEBUG   [2022-07-27 23:25:38,049] [5] records about stop orders successfully received
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:25:38,058] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:25:38,165] Requesting current prices for instrument with ticker [POSI] and FIGI [TCS00A103X66]...
TKSBrokerAPI.py     L:2663 DEBUG   [2022-07-27 23:25:38,534] Closing all available ['orders', 'shares']. Currency positions you must closes manually using buy or sell operations! Wait, please...
TKSBrokerAPI.py     L:1069 DEBUG   [2022-07-27 23:25:38,535] Requesting current actual pending orders. Wait, please...
TKSBrokerAPI.py     L:1075 DEBUG   [2022-07-27 23:25:38,639] [1] records about pending orders successfully received
TKSBrokerAPI.py     L:1086 DEBUG   [2022-07-27 23:25:38,639] Requesting current actual stop orders. Wait, please...
TKSBrokerAPI.py     L:1092 DEBUG   [2022-07-27 23:25:38,774] [5] records about stop orders successfully received
TKSBrokerAPI.py     L:2636 INFO    [2022-07-27 23:25:38,775] Found: [1] opened pending and [5] stop orders. Let's trying to cancel it all. Wait, please...
TKSBrokerAPI.py     L:2591 DEBUG   [2022-07-27 23:25:38,776] Cancelling pending order with ID: [************]. Wait, please...
TKSBrokerAPI.py     L:2599 DEBUG   [2022-07-27 23:25:38,939] Success time marker received from server: [2022-07-27T20:25:38.908221Z] (UTC)
TKSBrokerAPI.py     L:2600 INFO    [2022-07-27 23:25:38,940] Pending order with ID [************] successfully cancel
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:25:38,941] Cancelling stop order with ID: [********-****-****-****-************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:25:39,201] Success time marker received from server: [2022-07-27T20:25:39.171270508Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:25:39,202] Stop order with ID [********-****-****-****-************] successfully cancel
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:25:39,202] Cancelling stop order with ID: [********-****-****-****-************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:25:39,336] Success time marker received from server: [2022-07-27T20:25:39.306369844Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:25:39,337] Stop order with ID [********-****-****-****-************] successfully cancel
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:25:39,337] Cancelling stop order with ID: [********-****-****-****-************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:25:39,438] Success time marker received from server: [2022-07-27T20:25:39.410229318Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:25:39,439] Stop order with ID [********-****-****-****-************] successfully cancel
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:25:39,439] Cancelling stop order with ID: [********-****-****-****-************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:25:39,565] Success time marker received from server: [2022-07-27T20:25:39.534114123Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:25:39,566] Stop order with ID [********-****-****-****-************] successfully cancel
TKSBrokerAPI.py     L:2606 DEBUG   [2022-07-27 23:25:39,567] Cancelling stop order with ID: [************]. Wait, please...
TKSBrokerAPI.py     L:2614 DEBUG   [2022-07-27 23:25:39,745] Success time marker received from server: [2022-07-27T20:25:39.714517992Z] (UTC)
TKSBrokerAPI.py     L:2615 INFO    [2022-07-27 23:25:39,746] Stop order with ID [************] successfully cancel
TKSBrokerAPI.py     L:2325 DEBUG   [2022-07-27 23:25:39,747] Instrument tickers with type [Shares] that will be closed: ['POSI', 'IBM']
TKSBrokerAPI.py     L:2264 DEBUG   [2022-07-27 23:25:39,747] All opened instruments by it's tickers names: ['EUR_RUB__TOM', 'CNYRUB_TOM', 'CHFRUB_TOM', 'GBPRUB_TOM', 'TRYRUB_TOM', 'USD000UTSTOM', 'HKDRUB_TOM', 'POSI', 'IBM', 'RU000A101YV8', 'TGLD']
TKSBrokerAPI.py     L:2290 DEBUG   [2022-07-27 23:25:39,748] Closing trade of instrument: ticker [POSI], FIGI[TCS00A103X66], lots [1]. Wait, please...
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:25:39,749] Requesting current prices for instrument with ticker [POSI] and FIGI [TCS00A103X66]...
TKSBrokerAPI.py     L:2184 DEBUG   [2022-07-27 23:25:39,855] Opening [Sell] market order: ticker [POSI], FIGI [TCS00A103X66], lots [1.0], TP [0.0000], SL [0.0000], expiration date of TP/SL orders [Undefined]. Wait, please...
TKSBrokerAPI.py     L:358  DEBUG   [2022-07-27 23:25:39,947]     - not oK status code received: [400] {"code":3,"message":"instrument is not available for trading","description":"30079"}
TKSBrokerAPI.py     L:368  ERROR   [2022-07-27 23:25:39,948] Not `oK` status received from broker server!
TKSBrokerAPI.py     L:369  ERROR   [2022-07-27 23:25:39,948]     - message: [400] {"code":3,"message":"instrument is not available for trading","description":"30079"}
TKSBrokerAPI.py     L:2206 WARNING [2022-07-27 23:25:39,949] Not `oK` status received! Market order not created. See full debug log or try again and open order later.
TKSBrokerAPI.py     L:2290 DEBUG   [2022-07-27 23:25:39,949] Closing trade of instrument: ticker [IBM], FIGI[BBG000BLNNH6], lots [2], blocked [1]. Wait, please...
TKSBrokerAPI.py     L:2300 WARNING [2022-07-27 23:25:39,950] Just for your information: there are [1] lots blocked for instrument [IBM]! Available only [1.0] lots to closing trade.
TKSBrokerAPI.py     L:798  DEBUG   [2022-07-27 23:25:39,950] Requesting current prices for instrument with ticker [IBM] and FIGI [BBG000BLNNH6]...
TKSBrokerAPI.py     L:2184 DEBUG   [2022-07-27 23:25:40,042] Opening [Sell] market order: ticker [IBM], FIGI [BBG000BLNNH6], lots [1.0], TP [0.0000], SL [0.0000], expiration date of TP/SL orders [Undefined]. Wait, please...
TKSBrokerAPI.py     L:2202 INFO    [2022-07-27 23:25:40,685] [Sell] market order [447747151970] was executed: ticker [IBM], FIGI [BBG000BLNNH6], lots [1.0]. Total order price: [128.8900 usd] (with commission: [0.04 usd]). Average price of lot: [128.89 usd]
TKSBrokerAPI.py     L:3034 DEBUG   [2022-07-27 23:25:40,686] All operations with Tinkoff Server using Open API are finished success (summary code is 0).
TKSBrokerAPI.py     L:3039 DEBUG   [2022-07-27 23:25:40,686] TKSBrokerAPI module work duration: [0:00:04.204806]
TKSBrokerAPI.py     L:3042 DEBUG   [2022-07-27 23:25:40,687] TKSBrokerAPI module finished: [2022-07-27 20:25:40] (UTC), it is [2022-07-27 23:25:40] local time
```

</details>

### Module import

Full documentation of all available properties and methods of the `TKSBrokerAPI.TinkoffBrokerServer()` class can be found [by the link](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html). You can also see the correspondence between keys and methods in the ["Key features"](#Key-features) section.

Using the TKSBrokerAPI module, you can implement any trading scenario in Python. Many different system used for making trading decisions about buying or selling (technical analysis, neural networks, parsing reports or tracking other traders’ transactions), but you still need to perform trading operations: place orders, open and close transactions. The `TKSBrokerAPI` module will act as an intermediary between the code with the trading logic and the infrastructure of the Tinkoff Investments broker, as well as perform routine tasks on your behalf in [brokerage account](http://tinkoff.ru/sl/AaX1Et1omnH).

❗ **Important note**: the TKSBrokerAPI module is not intended for high-frequency (HFT) trading, due to the system of dynamic limit generation for TINKOFF INVEST API users (for more details [see the link](https://tinkoff.github.io/investAPI/limits/)). On average, this is 50-300 requests per second, depending on their type, which is very low for the requirements for HFT speeds (there are [several recommendations](https://tinkoff.github.io/investAPI/speedup/) to speed up execution orders). However, you can use it to automate your intraday, short, medium and long term trading strategies.

#### Abstract scenario implementation example

In this documentation, we do not want to focus on specific trading scenarios, but only show the possibilities for automating them. Therefore, let's consider one simple but completely fictional scenario, and implement it using the TKSBrokerAPI module. The actions will be the following:

- requesting the client's current portfolio and determining funds available for trading;
- request for a Depth of Market with a depth of 20 for the selected instrument, for example, shares with the ticker `IBM`;
- if the instrument was not purchased earlier, then checking:
  - if the buying volumes in the DOM are at least 50% higher than the selling volumes, then buy 1 share on the market and place the take profit as a stop order 5% higher than the current buy price with an expire period until cancellation;
- if the instrument is in the list of open positions, then checking:
   - if the current price is 3% higher than the average position price, then place the take profit as a pending limit order 0.05% more higher than the current price so that the position is closed with a profit with a high probability during the current session.
- requesting the current user's portfolio.

To understand the example, save and run the script under the spoiler below. Before doing this, don't forget to get a token and find out your accountId (see the section ["Auth"](#Auth)).

<details>
  <summary>Example of trading script in python using TKSBrokerAPI</summary>

```python

```
</details>

<details>
  <summary>Scenario run results</summary>

```commandline

```

</details>


That's all, ask questions in the section 👉 [**Issues**](https://github.com/Tim55667757/TKSBrokerAPI/issues/new) 👈, please.

🚀 Good luck for you in automating stock trading! And profit!

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=Donat%20(gift)%20for%20the%20authors%20of%20the%20TKSBrokerAPI%20project&default-sum=999&button-text=13&payment-type-choice=on&successURL=https%3A%2F%2Ftim55667757.github.io%2FTKSBrokerAPI%2F&quickpay=shop&account=410015019068268)
