# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
Module contains some html-templates used by reporting methods in TKSBrokerAPI module.

- **TKSBrokerAPI module documentation:** https://tim55667757.github.io/TKSBrokerAPI/docs/tksbrokerapi/TKSBrokerAPI.html
- **Mako Templates for Python:** https://www.makotemplates.org/
- **Open account for trading:** http://tinkoff.ru/sl/AaX1Et1omnH
"""

# Copyright (c) 2022 Gilmillin Timur Mansurovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


MAIN_INFO_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<html>
<head>
    <meta charset="utf-8"/>
    <title>${mainTitle}</title>
    <link rel="stylesheet" type="text/css" href="X:\work\projects\FuzzyMarketAnalytics\public\style.css">
    <style>${commonCSS}
    </style>
</head>
    <body>
        <div id="content"></div>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <script>
            var markdown = `${markdown}`; 
            document.getElementById("content").innerHTML = marked.parse(markdown);
        </script>
        <div id="footer" class="footer-div"><b>Report generated by <a href="https://github.com/Tim55667757/TKSBrokerAPI/blob/master/README_EN.md" target="_blank" rel="noopener noreferrer">TKSBrokerAPI Trade Automation Platform</a></b></div>
    </body>
</html>"""
"""This HTML-template used for translating all Markdown-reports to HTML."""


COMMON_CSS = """
    body {
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' height='100px' width='150px'><text transform='translate(20, 100) rotate(-45)' fill='rgb(176,176,176)' font-size='20' opacity='0.25'>TKSBrokerAPI</text></svg>");
    }

    .footer-div {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        color: #333333;
        background: #E6E6E6;
        margin: 24px 0 24px 0;
        border-radius: 20px 20px 20px 20px;
        padding: 12px;
    }

    p {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        padding: 2px;
        margin: 0;
    }
    
    li {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        padding: 1px 10px;
    }
    
    mark {
        background: #FFFFE6;
        padding: 0 3px;
    }
    
    h1 {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 22px;
        color: #333333;
        margin: 24px 0 12px 0;
    }
    
    h2 {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 20px;
        color: #333333;
        margin: 20px 0 10px 22px;
    }
    
    h3 {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 18px;
        color: #333333;
        margin: 16px 0 8px 52px;
    }
    
    details {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        padding: 2px 0;
        width: 100%;
        border-radius: 10px 10px 10px 10px;
        color: #333333;
    }
    
    summary {
        width: 100%;
        border-radius: 10px 10px 10px 10px;
        background: #CCCCCC;
        height: 20px;
        display: block;
        color: #333333;
        cursor: pointer;
    }
    
    summary::marker {
        display: none;
    }
    
    summary::before {
        content: "\21B7";
        padding-right: 0.5em;
    }
    
    details[open] > summary::before {
        content: "\2B8D";
    }
    
    .expand {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        border: none;
    }
    
    .expand::-ms-expand {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        border-radius: 10px;
    }
    
    table {
        font-family: "Segoe UI", "Frutiger", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", "Arial", sans-serif;
        font-size: 13px;
        width: 100%;
        border-radius: 40px 40px 10px 10px;
        border-spacing: 0;
        text-align: left;
        background: #FFFFFF;
        color: #333333;
    }
    
    td {
        border-style: solid;
        border-width: 0 1px 1px 0;
        border-color: white;
        padding: 12px;
        vertical-align: top;
        background: #E6E6E6;
    }
    
    th {
        border-style: solid;
        border-width: 0 1px 1px 0;
        border-color: white;
        font-size: 14px;
        vertical-align: top;
        background: #BFBFBF;
        text-align: center;
    }
    
    th:first-child {
        background: #BFBFBF;
        border-radius: 40px 0 0 0;
    }
    
    th:last-child {
        background: #BFBFBF;
        border-radius: 0 40px 0 0;
    }

    tr:first-child td:first-child {
        border-style: solid;
        border-width: 0 1px 1px 0;
        border-color: white;
        padding: 12px;
        vertical-align: top;
        background: #E6E6E6;
        border-radius: 0 0 0 0;
    }

    tr:first-child td:last-child {
        border-style: solid;
        border-width: 0 1px 1px 0;
        border-color: white;
        padding: 12px;
        vertical-align: top;
        background: #E6E6E6;
        border-radius: 0 0 0 0;
    }

    tr:last-child td:first-child {
        background: #E6E6E6;
        border-radius: 0 0 0 20px;
    }

    tr:last-child td:last-child {
        background: #E6E6E6;
        border-radius: 0 0 20px 0;
    }"""
"""Common CSS used by all templates."""
