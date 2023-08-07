#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

import re
from setuptools import setup, find_packages
from setuptools import *

with open("idx.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pygmi/pygmi.py').read(),
    re.M
    ).group(1)

setup(
    name='pygmi-get',
    packages=["pygmi"],
    entry_points = {
        "console_scripts": ["pygmi-get = pygmi.pygmi:main"]
    },
    version=version,
    description='A simple package installer for Python that eliminates the need for venvs.',
    long_description=long_description,
    url="https://github.com/AquaQuokka/pygmi",
    author="AquaQuokka",
    license='BSD-3-Clause',
    py_modules=['pygmi'],
    scripts=['pygmi/pygmi.py'],
    install_requires=["click"],
)
