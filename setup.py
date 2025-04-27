# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with GitHub Actions.


from setuptools import setup, find_packages
import os

verPath = os.path.join(os.path.dirname(__file__), "tksbrokerapi", "_version.py")
ver = {}
exec(open(verPath).read(), ver)
moduleVer = ver["__version__"]

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
    python_requires=">=3.9",  # Minimum supported Python version.

    name="tksbrokerapi",

    version=moduleVer,  # Include the dynamically generated version.

    description="TKSBrokerAPI is a trading platform designed to automate and simplify trading scenarios. It integrates with the Tinkoff Invest API server using the REST protocol. The platform can be used in two flexible ways: Command-Line Interface (CLI) and Python Library. This feature-rich API is perfect for trading enthusiasts and professional developers creating advanced automation solutions.",

    long_description=(
        "![TKSBrokerAPI Logo]"
        "(https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo.png?raw=true)\n\n"
        "*By [Fuzzy Technologies](https://fuzzy-technologies.github.io/)*\n\n\n"
        "🇺🇸 📚 **English Documentation:**\n\n"
        "• Full README with examples: [README_EN.md](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README_EN.md)\n\n"
        "• API Reference: [TKSBrokerAPI module docs](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html)\n\n"
        "• Cumulative Release Notes: [CHANGELOG_EN.md](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/CHANGELOG_EN.md)\n\n\n"
        "🇷🇺 📚 **Документация на русском:**\n\n"
        "• Подробное описание и примеры: [README.md](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/README.md)\n\n"
        "• Документация на модуль: [TKSBrokerAPI module docs](https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html)\n\n\n"
        "• Накопительные релиз-ноты: [CHANGELOG.md](https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/CHANGELOG.md)\n"
    ),

    long_description_content_type="text/markdown",

    license="Apache-2.0",

    license_files=["LICENSE"],

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
