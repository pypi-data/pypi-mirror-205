#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

try:
    from pygmi import main

except ImportError:
    from .pygmi import main

finally:
    main()