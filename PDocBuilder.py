# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

"""
A coroutine that generates the API documentation for the TKSBrokerAPI module using pdoc-engine: https://pdoc.dev/docs/pdoc.html

To build new documentation:
1. Remove the `./docs` directory from the repository root.
2. Go to the root of the repository.
3. Just run: `python PDocBuilder.py`.
"""


import os
import sys
import pdoc
from pathlib import Path


curdir = os.path.curdir

sys.path.extend([
    curdir,
    os.path.abspath(os.path.join(curdir, "tksbrokerapi")),
])

pdoc.render.configure(
    docformat="restructuredtext",
    favicon="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/favicon-128x128.png?raw=true",
    footer_text="⚙ Technologies. Knowledge. Science.",
    logo="https://github.com/Tim55667757/TKSBrokerAPI/blob/develop/docs/media/TKSBrokerAPI-Logo-text-only.png?raw=true",
    show_source=False,
    template_directory=Path("docs", "templates").resolve(),
)
pdoc.pdoc(
    Path("tksbrokerapi").resolve(),
    output_directory=Path("docs").resolve(),
)
