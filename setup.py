# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with Travis CI


from setuptools import setup
import os

__version__ = "1.2"

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
    __version__ += ".dev0"  # set version as major.minor.localbuild if local build: python setup.py install

print("TKSBrokerAPI build version = {}".format(__version__))

setup(
    name="tksbrokerapi",

    version=__version__,

    description="Simple python API to work with Tinkoff Open API and access to the TKS Broker server using REST protocol.",

    long_description="See full documentation with examples on GitHub Pages: https://tim55667757.github.io/TKSBrokerAPI",

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
        "trade",
        "tinkoff",
        "tinkoff-api",
        "python-api",
        "openapi",
    ],

    tests_require=[
        "pytest>=7.1.2",
        "requests>=2.25.1",  # Apache-2.0 license
        "pandas>=1.2.2",
        "python-dateutil>=2.8.1",  # Apache-2.0 license
        "PriceGenerator>=1.2.74",  # Apache-2.0 license
    ],

    install_requires=[
        "requests>=2.25.1",  # Apache-2.0 license
        "pandas>=1.2.2",
        "python-dateutil>=2.8.1",  # Apache-2.0 license
        "PriceGenerator>=1.2.74",  # Apache-2.0 license
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
