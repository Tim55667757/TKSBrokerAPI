# Anomaly Volumes Detector

[Документация на русском](#Детектор-аномальных-объёмов)

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![task](https://badgen.net/badge/issue/119/red)](https://github.com/Tim55667757/TKSBrokerAPI/issues/119)
[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


## Acknowledgements

* Idea and sponsorship: [Jolids](https://github.com/Jolids)
* Developer: [Timur Gilmullin](https://github.com/Tim55667757)

## Description

**[Anomaly Volumes Detector](https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/AnomalyVolumesDetector)** is a simple TG-bot for detecting anomaly volumes of Buyers and Sellers prices.

The bot monitors the volumes of Buyers and Sellers in the orders book (DOM), looks for anomalies in the number series of volumes and notifies in Telegram. The notification contains: the current price and prices with anomaly volumes.

### Concept

Main steps: 

- The script enters the market on schedule (e.g. crontab format: `timeToWork: "*/2 10-21 * * 1-5"  # At every 2nd minute past every hour from 10 through 22 (including) on every day-of-week from Monday through Friday`, see [other examples](https://crontab.guru/#*/2_10-21_*_*_1-5)).

- In a parallel (multiprocessing) conveyor mode, it requests data on the state of the order book for the specified instruments and with the specified depth of the order book (`depth <= 50`).

- For each order book, it searches for all current anomalies in the volumes of Sellers and Buyers (filtering by [Hampel method](https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample_EN.ipynb) along the entire length of the current DOM).

- If the list of anomalies is not empty, then script generates a human-readable message, for example:
    ```
    Anomalous volumes detected!
    
    * Ticker: [TMOS]
    * Instrument: [Shares] [Tinkoff iMOEX]
    * Date and time: [2023-01-18 15:55:51 UTC]
    * Is in your portfolio: [yes / no]
      
    * Current price / volume / value in the order book:
      * Buy (1st seller price):
        4.212 / 51231 / 220959.303 rub
      * Sell (1st buyer price):
        4.211 / 11416 / 48072.776 rub
      
    * Anomalies among sellers' offers, price / volume / value:
      * 4.31 / 1508321 / 6500863.51 rub
      * 4.27 / 608178 / 2596920.06 rub
      * 4.244 / 1173028 / 4978330.832 rub
      
    * Anomalies among buyers' offers, price / volume / value:
      * 4.202 / 1176972 / 4945636.344 rub
    ```

- Connect to the specified TG-bot by token and send a notification through it.

### Bot launch

All parameters are configured in two configuration files: [`config.yaml`](./config.yaml) and [`secrets.yaml`](./secrets.yaml), which must be present next to the script [`TKSAVDetector.py`](./TKSAVDetector.py). 

The script works with `python >= 3.9`, and dependencies from [`requirements.txt`](./requirements.txt) must also be installed. Steps to start on a new server:

```commandline
git clone https://github.com/Tim55667757/TKSBrokerAPI.git
cd ./TKSBrokerAPI/docs/examples/AnomalyVolumesDetector
python3 -m pip install -r requirements.txt
python3 TKSAVDetector.py config.yaml secrets.yaml
```

If you're using default names `config.yaml` and `secrets.yaml`, then they can be omitted in `python3 TKSAVDetector.py` command.

### Methods

* The `ConfigDecorator()` method is a wrapper (decorator) for loading configuration files and secrets, controlling the start time of iterations on a schedule, for a single run or in infinite mode, as well as for parameterizing the Trade Manager.
     - Decorator `ConfigDecorator()`:
       - loads settings from configuration files,
       - checks the number of CPU available for parallelization,
       - checks if it's working time (according to crontab settings),
       - launches the Trade Manager once or in infinite mode.

* The `TradeManager()` method is a manager for initializing, launching and managing parallel pipelines, which will analyze the state of the order book for a specific set of tickers.
     - Manager `TradeManager()`:
       - initializes the reporter (an instance of the `TinkoffBrokerServer()` class for generating reports),
       - updates the cache for instruments once and gets the user's portfolio so that they are not updated on each pipeline once again,
       - starts iteration over all tickers, splits them into sets,
       - each set sends to its own pipeline for parallelization.


🚀 Good luck for you in trade automation! And profit!

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


---


# Детектор аномальных объёмов

[See doc in English](#Anomaly-Volumes-Detector)

<a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md" target="_blank"><img src="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true" alt="TKSBrokerAPI-Logo" width="780" /></a>

**T**echnologies · **K**nowledge · **S**cience

[![task](https://badgen.net/badge/issue/119/red)](https://github.com/Tim55667757/TKSBrokerAPI/issues/119)
[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)


## Благодарности

* Идея ТГ-бота и спонсорство: [Jolids](https://github.com/Jolids)
* Разработчик: [Тимур Гильмуллин](https://github.com/Tim55667757)

## Описание

**[Детектор аномальных объёмов](https://github.com/Tim55667757/TKSBrokerAPI/tree/develop/docs/examples/AnomalyVolumesDetector)** — это простой ТГ-бот для анализа объёмов спроса и предложения покупателей и продавцов.

Бот следит за объёмами покупателей и продавцов в биржевом стакане, ищет аномалии в числовом ряду объёмов и оповещает о них в Телеграм. Оповещение содержит: текущую цену инструмента и цены с аномальными объёмами.

### Концепция

Основные шаги: 

- Скрипт выходит на рынок по расписанию (например, в формате crontab: `timeToWork: "*/2 10-21 * * 1-5"  # С 10:00 утра до 22:00 вечера (включительно) в будние дни, каждые 2 минуты`, см. другие [примеры](https://crontab.guru/#*/2_10-21_*_*_1-5)).

- В параллельном (мультипроцессном) конвейерном режиме запрашивает данные по состоянию биржевого стакана по указанным инструментам и с указанной глубиной стакана (`depth <= 50`).

- Для каждого стакана ищет все текущие аномалии в объёмах продавцов и покупателей (фильтрация [методом Хампеля](https://nbviewer.org/github/Tim55667757/TKSBrokerAPI/blob/develop/docs/examples/HampelFilteringExample.ipynb) по всей длине текущего стакана).

- Если список аномалий по инструменту получился не пустой, то сформировать оповещение, например, такого вида:
    ```
    Обнаружены аномальные объёмы!
    
    * Тикер: [TMOS]
    * Инструмент: [Shares] [Тинькофф iMOEX]
    * Дата и время: [2023-01-18 15:55:51 UTC]
    * Есть в вашем портфеле: [да / нет]
    
    * Текущая цена / объём / стоимость в стакане:
      * На покупку (Buy, 1-я цена продавцов):
        4.212 / 51231 / 220959.303 rub
      * На продажу (Sell, 1-я цена покупателей):
        4.211 / 11416 / 48072.776 rub
    
    * Аномалии среди предложений продавцов, цена / объём / стоимость:
      * 4.31 / 1508321 / 6500863.51 rub
      * 4.27 / 608178 / 2596920.06 rub
      * 4.244 / 1173028 / 4978330.832 rub
    
    * Аномалии среди предложений покупателей, цена / объём / стоимость:
      * 4.202 / 1176972 / 4945636.344 rub
    ```

- Подключиться к указанному ТГ-боту по токену и отправить через него оповещение.

### Запуск бота

Все параметры настраиваются в двух конфигурационных файлах: [`config.yaml`](./config.yaml) и [`secrets.yaml`](./secrets.yaml), которые должны присутствовать рядом со скриптом [`TKSAVDetector.py`](./TKSAVDetector.py). 

Скрипт работает с `python >= 3.9`, а также должны быть установлены зависимости из [`requirements.txt`](./requirements.txt). Шаги для запуска на новом сервере:

```commandline
git clone https://github.com/Tim55667757/TKSBrokerAPI.git
cd ./TKSBrokerAPI/docs/examples/AnomalyVolumesDetector
python3 -m pip install -r requirements.txt
python3 TKSAVDetector.py config.yaml secrets.yaml
```

Если используются дефолтные файлы конфигурации `config.yaml` и `secrets.yaml`, то в команде `python3 TKSAVDetector.py` их можно не указывать.

### Основные методы

* Метод `ConfigDecorator()` — обёртка (декоратор) для загрузки файлов конфигурации и секретов, управления временем запуска итераций по расписанию, для однократного запуска или в бесконечном режиме, а также для параметризации менеджера.
    - Декоратор `ConfigDecorator()`:
      - загружает настройки из файлов конфигурации,
      - проверяет количество доступных для распараллеливания запросов CPU,
      - проверяет рабочее ли сейчас время (согласно настройкам crontab),
      - однократно или в бесконечном режиме запускает менеджер.

* Метод `TradeManager()` — менеджер для инициализации, запуска и управления параллельными конвейерами, на которых будет исполняться анализ состояния стакана для конкретного набора тикеров.
    - Менеджер `TradeManager()`:
      - инициализирует репортер (экземпляр класса `TinkoffBrokerServer()` для генерации отчётов),
      - однократно обновляет кеш по инструментам и получает портфель пользователя, чтобы они не обновлялись на каждом конвейере лишний раз,
      - запускает итерацию по всем тикерам, разбивает их на наборы,
      - каждый набор отправляет на свой конвейер для параллелизации.


🚀 Успехов вам в автоматизации биржевой торговли! И профита!

[![gift](https://badgen.net/badge/gift/donate/green)](https://yoomoney.ru/fundraise/4WOyAgNgb7M.230111)