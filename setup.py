# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with Travis CI


from setuptools import setup
import os
from tksbrokerapi.TKSBrokerAPI import __version__ as ver

__version__ = ver  # The "major.minor" version gives from TKSBrokerAPI and the build number define at the build-server

devStatus = "4 - Beta"

if "TRAVIS_BUILD_NUMBER" in os.environ and "TRAVIS_BRANCH" in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ["TRAVIS_BUILD_NUMBER"]))
    print("TRAVIS_BRANCH = {}".format(os.environ["TRAVIS_BRANCH"]))

    __version__ += ".{}{}".format(
        "" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else "dev",
        os.environ["TRAVIS_BUILD_NUMBER"],
    )

    devStatus = "5 - Production/Stable" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else devStatus

else:
    print("This is local build")
    __version__ += ".dev0"  # set version as major.minor.dev0 if local build used

print("TKSBrokerAPI build version = {}".format(__version__))

setup(
    name="tksbrokerapi",

    version=__version__,

    description="TKSBrokerAPI is the trading platform for automation and simplifying the implementation of trading scenarios, as well as working with Tinkoff Invest API server via the REST protocol. The TKSBrokerAPI platform may be used in two ways: from the console, it has a rich keys and commands, or you can use it as Python module.",

    long_description="See full documentation with examples: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md\n\nTKSBrokerAPI module documentation: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html\n\nПодробная документация на русском с примерами: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md\n\nДокументация на модуль TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html",

    license="Apache-2.0",

    author="Timur Gilmullin",

    author_email="tim55667757@gmail.com",

    url="https://github.com/Tim55667757/TKSBrokerAPI/",

    download_url="https://github.com/Tim55667757/TKSBrokerAPI.git",

    entry_points={"console_scripts": ["tksbrokerapi = tksbrokerapi.TKSBrokerAPI:Main"]},

    classifiers=[
        "Development Status :: {}".format(devStatus),
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],  # classifiers are from here: https://pypi.org/classifiers/

    keywords=[
        "history",
        "csv",
        "stock",
        "prices",
        "candlesticks",
        "statistics",
        "cli",
        "client",
        "rest",
        "rest-api",
        "api-client",
        "trading-api",
        "trading",
        "trading-platform",
        "trade",
        "tinkoff",
        "tinkoff-api",
        "python-api",
        "openapi",
        "platform",
    ],

    tests_require=[
        "pytest >= 7.1.2",  # MIT License
        "requests >= 2.25.1",  # Apache-2.0 license
        "pandas >= 1.5.2",  # MIT License
        "openpyxl >= 3.0.10",  # MIT License
        "Mako >= 1.2.4",  # MIT License
        "python-dateutil >= 2.8.1",  # Apache-2.0 license
        "PriceGenerator >= 1.3.81",  # Apache-2.0 license
        "FuzzyRoutines >= 1.0.3",  # MIT License
    ],

    install_requires=[
        "requests >= 2.25.1",  # Apache-2.0 license
        "pandas >= 1.5.2",  # MIT License
        "numpy >= 1.23.5",  # BSD-3-Clause license
        "openpyxl >= 3.0.10",  # MIT License
        "Mako >= 1.2.4",  # MIT License
        "python-dateutil >= 2.8.1",  # Apache-2.0 license
        "PriceGenerator >= 1.3.81",  # Apache-2.0 license
        "FuzzyRoutines >= 1.0.3",  # MIT License
    ],

    packages=[
        "tksbrokerapi",
    ],

    package_data={
        "tksbrokerapi": [
        ],
    },

    include_package_data=True,

    zip_safe=True,
)
