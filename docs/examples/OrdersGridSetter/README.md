# Orders Grid Setter

[Документация на русском](#Установщик-сетки-ордеров)

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![task](https://badgen.net/badge/issue/14/red)](https://github.com/Tim55667757/TKSBrokerAPI/issues/14)
[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)

- [Description](#Description)
  - [Concept](#Concept)
  - [Launch](#Launch)
    - [Startup issues](#Startup-issues)
  - [Auth](#Auth)
  - [Methods](#Methods)
  - [Run examples](#Run-examples)


## Description

**[Orders Grid Setter](https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/OrdersGridSetter)** scenario can be set up a grid of orders (limit or stop, with buy or sell directions) with defined step and lots. It works on TKSBrokerAPI platform in parallel mode conveyor simultaneously for a lot of instruments defined by tickers. This script is convenient to use when you need to place fast many orders (several tens or hundreds) for various instruments, which would be difficult to do manually through the broker's application.

### Concept

It will be easier to understand how the scenario works in the illustration below.

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/OrdersGridSetter.png?raw=true" alt="OrdersGridSetter" width="1200" /></a>

Main steps: 

- The script enters the market and request current price for every ticker defined in config. It works in a parallel (multiprocessing) conveyor mode for all instruments simultaneously.

- Depending on the selected direction and grid step, all orders of the specified type and lots are placed for every instrument. The first order in grid is placed at a target price located at a certain distance in percent of the current price. If this distance is 0% then current price is used as target price for first order, and order grid will be created from current price (above or below depends on config parameters).

### Launch

All parameters for order grid are configured in two configuration files: [`config.yaml`](./config.yaml) and [`secrets.yaml`](./secrets.yaml), which must be present next to the script [`TKSOrdersGridSetter.py`](./TKSOrdersGridSetter.py). All configuration parameters are commented in detail. In fact, the parameters are the same as the command parameters for opening orders using the TKSBrokerAPI platform, only they are applied at once to many specified instruments. See also: "[How to parametrize and open a pending limit or stop order using the TKSBrokerAPI platform](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md#open-a-pending-limit-or-stop-order)".

The script works with `python >= 3.9`, and dependencies from [`requirements.txt`](./requirements.txt) must also be installed. Steps to start on a new server:

```commandline
git clone https://github.com/Tim55667757/TKSBrokerAPI.git
cd TKSBrokerAPI
git branch
git checkout -f develop
git pull
cd ./docs/examples/OrdersGridSetter
python3 -m pip install -r requirements.txt
python3 TKSOrdersGridSetter.py config.yaml secrets.yaml
```

If you're using default names `config.yaml` and `secrets.yaml`, then they can be omitted in `python3 OrdersGridSetter.py` command.

#### Startup issues

It is possible that after starting the bot you will see an import error like this:

```
  File "./tksbrokerapi/TKSBrokerAPI.py", line 105, in <module>
    from Templates import *  # Some html-templates used by reporting methods in TKSBrokerAPI module
ModuleNotFoundError: No module named 'Templates'
```

This means that the library directory for the version of Python where the TKSBrokerAPI platform was installed is not visible in the system environment. You need to add it to the `PYTHONPATH` environment variable (see [explanation and examples for different OS](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html)). For example, under Linux/MacOS:

```commandline
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/tksbrokerapi
echo $PYTHONPATH
```

If you don't want to set the `PYTHONPATH` variable every time you open a terminal, you can set it to the system environment.

### Auth

All critical secrets must store locally in [`secrets.yaml`](./secrets.yaml) file. You can define there some parameters:

* `userToken` — place here the Tinkoff Investment API token (`t.*****`) or stay it empty and use `TKS_API_TOKEN` environment variable;
* `userAccount` — place here the `accountId` of Tinkoff Investment broker account or stay it empty and use `TKS_ACCOUNT_ID` environment variable.

How to create the Tinkoff Investment API token [see here](https://tinkoff.github.io/investAPI/token/). After creating token, store it to `userToken` variable in `secrets.yaml` or in `TKS_API_TOKEN` environment variable.

You can find `accountId` number using the TKSBrokerAPI platform with command: `tksbrokerapi --accounts` and then store it to `userAccount` variable in `secrets.yaml` or in `TKS_ACCOUNT_ID` environment variable.

### Methods

* The `ConfigDecorator()` method is a wrapper (decorator) for loading configuration files and secrets and for parameterizing the Trade Manager.
    - Decorator `ConfigDecorator()`:
      - loads settings from configuration files,
      - checks the number of CPU available for parallelization,
      - launches the Trade Manager with defined settings.

* The `TradeManager()` method is a manager for initializing, launching and managing parallel pipelines, on which will be trade for a specific set of tickers.
    - Manager `TradeManager()`:
      - initializes the reporter (an instance of the `TinkoffBrokerServer()` class for generating reports),
      - updates the cache for instruments once and gets the user's portfolio so that they are not updated on each pipeline once again,
      - starts iteration over all tickers, splits them into sets,
      - each set sends to its own pipeline for parallelization.

* The `TradeScenario()` class contains methods for implementing the trading scenario logic. It has two important methods: `Run()` and `Steps()`.
    - `Run()` is a runner of trade steps for all given instruments tickers.
    - `Steps()` is a section for implementing the steps of the trading scenario for one current instrument.

### Run examples

```commandline
test@srv:/projects/TKSBrokerAPI/docs/examples/OrdersGridSetter$ python3 TKSOrdersGridSetter.py

TKSOrdersGridSetter.pyL:355  INFO    [2023-09-20 17:11:45,596] >>> Scenario runs: [John Doe] [**********] [Test account] [TKSOrdersGridSetter] 
TKSOrdersGridSetter.pyL:388  INFO    [2023-09-20 17:11:45,754] [John Doe] [Test account] [TKSOrdersGridSetter] All pipelines initialized, count: [2], tickers for trading:
[1]: ['YNDX']
[2]: ['SBER']
TKSOrdersGridSetter.pyL:190  INFO    [2023-09-20 17:11:45,890] [Test mode] [SBER] Prepared tasks for opening orders grid:
| No. | Operation | orderType | lots   | targetPrice  | limitPrice | stopType | expDate             |
|-----|-----------|-----------|--------|--------------|------------|----------|---------------------|
| 1   | Sell      | Stop      | 1      | 259.24       | 0          | TP       | Undefined           |
| 2   | Sell      | Stop      | 1      | 259.49       | 0          | TP       | Undefined           |
| 3   | Sell      | Stop      | 1      | 259.75       | 0          | TP       | Undefined           |
| 4   | Sell      | Stop      | 1      | 260.0        | 0          | TP       | Undefined           |
| 5   | Sell      | Stop      | 1      | 260.26       | 0          | TP       | Undefined           |
TKSOrdersGridSetter.pyL:259  INFO    [2023-09-20 17:11:45,890] [2] [John Doe] [**********] [Test account] [TKSOrdersGridSetter] [SBER] [success] [Test mode] Only orders parameters were calculated. Real orders do not opening!
TKSOrdersGridSetter.pyL:190  INFO    [2023-09-20 17:11:45,899] [Test mode] [YNDX] Prepared tasks for opening orders grid:
| No. | Operation | orderType | lots   | targetPrice  | limitPrice | stopType | expDate             |
|-----|-----------|-----------|--------|--------------|------------|----------|---------------------|
| 1   | Sell      | Stop      | 1      | 2483.8       | 0          | TP       | Undefined           |
| 2   | Sell      | Stop      | 1      | 2486.2       | 0          | TP       | Undefined           |
| 3   | Sell      | Stop      | 1      | 2488.8       | 0          | TP       | Undefined           |
| 4   | Sell      | Stop      | 1      | 2491.2       | 0          | TP       | Undefined           |
| 5   | Sell      | Stop      | 1      | 2493.6       | 0          | TP       | Undefined           |
TKSOrdersGridSetter.pyL:259  INFO    [2023-09-20 17:11:45,899] [1] [John Doe] [**********] [Test account] [TKSOrdersGridSetter] [YNDX] [success] [Test mode] Only orders parameters were calculated. Real orders do not opening!
TKSOrdersGridSetter.pyL:404  INFO    [2023-09-20 17:11:45,901] >>> Scenario operations completed for all instruments: [John Doe] [Test account] [TKSOrdersGridSetter] 
```

🚀 Good luck for you in trade automation! And profit!

If the scenario was useful to you, you can donate authors using the link: https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


---


# Установщик сетки ордеров

[See doc in English](#Orders-Grid-Setter)

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![task](https://badgen.net/badge/issue/119/red)](https://github.com/Tim55667757/TKSBrokerAPI/issues/119)
[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)

- [Описание](#Описание)
  - [Концепция](#Концепция)
  - [Запуск](#Запуск)
    - [Проблемы запуска](#Проблемы-запуска)
  - [Авторизация](#Авторизация)
  - [Основные методы](#Основные-методы)
  - [Примеры запуска](#Примеры-запуска)


## Описание

**[Установщик сетки ордеров](https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/OrdersGridSetter)** — это сценарий, который позволяет настроить сетку ордеров (лимитных или стоп-ордеров, с указанием направления — покупки или продажи) с определённым шагом и лотностью. Он работает на платформе TKSBrokerAPI и в параллельном режиме конвейера позволяет выставлять ордера одновременно для множества инструментов, заданных своими тикерами. Этот скрипт удобно использовать, когда вам необходимо быстро разместить большое количество ордеров (несколько десятков или сотен) по различным инструментам, что было бы сложно сделать вручную через приложение брокера.

### Концепция

Понять, как работает сценарий, будет легче на иллюстрации ниже.

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/OrdersGridSetter.png?raw=true" alt="OrdersGridSetter" width="1200" /></a>

Основные шаги: 

- Скрипт выходит на рынок и запрашивает текущую цену для каждого тикера, заданного в конфигурации. Он работает в параллельном (многопроцессорном) конвейерном режиме для всех инструментов одновременно.

- В зависимости от выбранного направления и шага сетки по каждому инструменту выставляются ордера заданного типа и лотности по очереди. Первый ордер в сетке размещается по целевой цене, расположенной на указанном расстоянии в процентах от текущей цены. Если это расстояние равно 0%, то текущая цена используется в качестве целевой цены для первого ордера, а сетка ордеров будет создана выше или ниже от неё (зависит от параметров конфигурации).

### Запуск

Все параметры для сетки ордеров настраиваются в двух конфигурационных файлах: [`config.yaml`](./config.yaml) и [`secrets.yaml`](./secrets.yaml), которые должны присутствовать рядом со скриптом [`TKSOrdersGridSetter.py`](./TKSOrdersGridSetter.py). Все параметры конфигурации подробно прокомментированы. По сути, параметры такие же, как и параметры команды для открытия ордеров с помощью платформы TKSBrokerAPI, только они применяются сразу для множества заданных инструментов. Смотрите также: "[Как параметризовать и открыть отложенный лимит или стоп-ордер с помощью платформы TKSBrokerAPI](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md#open-a-pending-limit-or-stop-order)".

Скрипт работает с `python >= 3.9`, а также должны быть установлены зависимости из [`requirements.txt`](./requirements.txt). Шаги для запуска на новом сервере:

```commandline
git clone https://github.com/Tim55667757/TKSBrokerAPI.git
cd TKSBrokerAPI
git branch
git checkout -f develop
git pull
cd ./docs/examples/OrdersGridSetter
python3 -m pip install -r requirements.txt
python3 TKSOrdersGridSetter.py config.yaml secrets.yaml
```

Если используются дефолтные файлы конфигурации `config.yaml` и `secrets.yaml`, то в команде `python3 TKSAVDetector.py` их можно не указывать.

#### Проблемы запуска

Возможно, что после запуска бота вы увидите ошибку импорта такого вида:

```
  File "./tksbrokerapi/TKSBrokerAPI.py", line 105, in <module>
    from Templates import *  # Some html-templates used by reporting methods in TKSBrokerAPI module
ModuleNotFoundError: No module named 'Templates'
```

Это означает, что каталог с библиотеками для той версии Python, куда была установлена платформа TKSBrokerAPI, не виден в системном окружении. Нужно добавить его в переменную окружения `PYTHONPATH` (смотрите объяснение и примеры для разных ОС [по ссылке](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html)). Например, под Linux/MacOS:

```commandline
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/tksbrokerapi
echo $PYTHONPATH
```

Чтобы не устанавливать переменную `PYTHONPATH` каждый раз при открытии терминала, можно установить её в системное окружение своей ОС.

### Авторизация

Все критичные секреты должны храниться локально в файле [`secrets.yaml`](./secrets.yaml). Вы можете задать там параметры:

* `userToken` — укажите здесь свой API-токен от Тинькофф Инвестиции (`t.*****`) или оставьте пустую строку и используйте переменную окружения `TKS_API_TOKEN`;
* `userAccount` — укажите здесь свой `accountId`, это счёт пользователя в Тинькофф Инвестиции, или оставьте пустую строку и используйте переменную окружения `TKS_ACCOUNT_ID`.

Как создать API-токен в Тинькофф Инвестиции, смотрите [по ссылке](https://tinkoff.github.io/investAPI/token/). После создания токена, сохраните его в переменной `userToken` (в `secrets.yaml`) или в переменной окружения `TKS_API_TOKEN`.

Вы можете найти номер своего аккаунта `accountId` используя команду платформы TKSBrokerAPI: `tksbrokerapi --accounts`. После этого сохраните его в переменной `userAccount` (в `secrets.yaml`) или в переменной окружения `TKS_ACCOUNT_ID`.

### Основные методы

* Метод `ConfigDecorator()` — это обёртка (декоратор) для загрузки файлов конфигурации и секретов, а также для параметризации Торгового Менеджера.
    - Декоратор `ConfigDecorator()`:
      - загружает настройки из файлов конфигурации,
      - проверяет количество доступных для распараллеливания запросов CPU,
      - запускает Торгового Менеджера с загруженными настройками.

* Метод `TradeManager()` — это менеджер для инициализации, запуска и управления параллельными конвейерами, на которых будет идти торговля по заданному набору тикеров.
    - Менеджер `TradeManager()`:
      - инициализирует репортер (экземпляр класса `TinkoffBrokerServer()` для генерации отчётов),
      - однократно обновляет кеш по инструментам и получает портфель пользователя, чтобы они не обновлялись на каждом конвейере лишний раз,
      - запускает итерацию по всем тикерам, разбивает их на наборы,
      - каждый набор отправляет на свой конвейер для параллелизации.

* Класс `TradeScenario()` содержит методы для реализации логики торгового сценария. Он содержит два основных метода: `Run()` и `Steps()`.
    - `Run()` — это метод для запуска сценария итеративно по всем указанным тикерам инструментов.
    - `Steps()` — это раздел с описанием, реализацией и запуском отдельных шагов торгового сценария для одного инструмента.

### Примеры запуска

```commandline
test@srv:/projects/TKSBrokerAPI/docs/examples/OrdersGridSetter$ python3 TKSOrdersGridSetter.py

TKSOrdersGridSetter.pyL:355  INFO    [2023-09-20 17:11:45,596] >>> Scenario runs: [John Doe] [**********] [Test account] [TKSOrdersGridSetter] 
TKSOrdersGridSetter.pyL:388  INFO    [2023-09-20 17:11:45,754] [John Doe] [Test account] [TKSOrdersGridSetter] All pipelines initialized, count: [2], tickers for trading:
[1]: ['YNDX']
[2]: ['SBER']
TKSOrdersGridSetter.pyL:190  INFO    [2023-09-20 17:11:45,890] [Test mode] [SBER] Prepared tasks for opening orders grid:
| No. | Operation | orderType | lots   | targetPrice  | limitPrice | stopType | expDate             |
|-----|-----------|-----------|--------|--------------|------------|----------|---------------------|
| 1   | Sell      | Stop      | 1      | 259.24       | 0          | TP       | Undefined           |
| 2   | Sell      | Stop      | 1      | 259.49       | 0          | TP       | Undefined           |
| 3   | Sell      | Stop      | 1      | 259.75       | 0          | TP       | Undefined           |
| 4   | Sell      | Stop      | 1      | 260.0        | 0          | TP       | Undefined           |
| 5   | Sell      | Stop      | 1      | 260.26       | 0          | TP       | Undefined           |
TKSOrdersGridSetter.pyL:259  INFO    [2023-09-20 17:11:45,890] [2] [John Doe] [**********] [Test account] [TKSOrdersGridSetter] [SBER] [success] [Test mode] Only orders parameters were calculated. Real orders do not opening!
TKSOrdersGridSetter.pyL:190  INFO    [2023-09-20 17:11:45,899] [Test mode] [YNDX] Prepared tasks for opening orders grid:
| No. | Operation | orderType | lots   | targetPrice  | limitPrice | stopType | expDate             |
|-----|-----------|-----------|--------|--------------|------------|----------|---------------------|
| 1   | Sell      | Stop      | 1      | 2483.8       | 0          | TP       | Undefined           |
| 2   | Sell      | Stop      | 1      | 2486.2       | 0          | TP       | Undefined           |
| 3   | Sell      | Stop      | 1      | 2488.8       | 0          | TP       | Undefined           |
| 4   | Sell      | Stop      | 1      | 2491.2       | 0          | TP       | Undefined           |
| 5   | Sell      | Stop      | 1      | 2493.6       | 0          | TP       | Undefined           |
TKSOrdersGridSetter.pyL:259  INFO    [2023-09-20 17:11:45,899] [1] [John Doe] [**********] [Test account] [TKSOrdersGridSetter] [YNDX] [success] [Test mode] Only orders parameters were calculated. Real orders do not opening!
TKSOrdersGridSetter.pyL:404  INFO    [2023-09-20 17:11:45,901] >>> Scenario operations completed for all instruments: [John Doe] [Test account] [TKSOrdersGridSetter] 
```

🚀 Успехов вам в автоматизации биржевой торговли! И профита!

Если сценарий был вам полезен, вы можете поддержать авторов по ссылке: https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)
