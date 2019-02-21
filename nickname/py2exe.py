#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'transform main.py to nn.exe'
__author__ = 'Whyn'
"""
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['main.py', '-F', '-c', '--noconsole']
    # opts = ['main.py', '-F', '-c', '--icon=nn.ico', '--upx-dir', 'upx394d']
    run(opts)
