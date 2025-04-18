# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with GitHub Actions.


from setuptools import setup, find_packages
import os
from tksbrokerapi.TKSBrokerAPI import __version__ as ver

moduleVer = ver  # The "major.minor" version is derived from TKSBrokerAPI, while the build number is defined by the build server.
devStatus = "4 - Beta"  # Default development status.

VERSION_OFFSET = 200  # Offset for the build number.

# Determine if the build is running inside a CI environment (GitHub Actions):
if "GITHUB_RUN_NUMBER" in os.environ and "GITHUB_REF" in os.environ:
    print("This is GitHub Actions build")
    print("GITHUB_RUN_NUMBER = {}".format(os.environ["GITHUB_RUN_NUMBER"]))
    print("GITHUB_REF = {}".format(os.environ["GITHUB_REF"]))

    # Extract the branch/tag name from GITHUB_REF (e.g., refs/heads/branch-name):
    branchName = os.environ["GITHUB_REF"].split("/")[-1]

    # Generate the version based on the branch name and build number:
    moduleVer += ".{}{}".format(
        "" if "release" in branchName or branchName == "master" else "dev",
        int(os.environ["GITHUB_RUN_NUMBER"]) + VERSION_OFFSET,
    )

    # Update the development status for release branches:
    devStatus = "5 - Production/Stable" if "release" in branchName or branchName == "master" else devStatus

else:
    print("This is a local build")

    moduleVer += ".dev0"  # For local builds, use the dev0 suffix.

# Print the determined version for the build
print("TKSBrokerAPI build version = {}".format(moduleVer))

# Read dependencies from `requirements.txt`:
with open("requirements.txt", "r", encoding="utf-8") as f:
    installRequires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Configure setuptools for the TKSBrokerAPI project:
setup(
    name="tksbrokerapi",

    version=moduleVer,  # Include the dynamically generated version.

    description="TKSBrokerAPI is a trading platform designed to automate and simplify trading scenarios. It integrates with the Tinkoff Invest API server using the REST protocol. The platform can be used in two flexible ways: Command-Line Interface (CLI) and Python Library. This feature-rich API is perfect for trading enthusiasts and professional developers creating advanced automation solutions.",

    long_description="See full documentation with examples: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md\n\nTKSBrokerAPI module documentation: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html\n\nПодробная документация на русском с примерами: https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README.md\n\nДокументация на модуль TKSBrokerAPI: https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html",

    license="Apache-2.0",

    author="Timur Gilmullin",

    author_email="tim55667757@gmail.com",

    url="https://github.com/Tim55667757/TKSBrokerAPI/",

    download_url="https://github.com/Tim55667757/TKSBrokerAPI.git",

    entry_points={"console_scripts": ["tksbrokerapi=tksbrokerapi.TKSBrokerAPI:Main"]},

    classifiers=[
        "Development Status :: {}".format(devStatus),
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],  # Classifiers are based on PyPI specifications: https://pypi.org/classifiers/

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

    install_requires=installRequires,  # Load dependencies from `requirements.txt`.

    packages=find_packages(),  # Automatically find packages in the project.

    include_package_data=True,  # Automatically include files from `MANIFEST.in`.

    zip_safe=True,
)
