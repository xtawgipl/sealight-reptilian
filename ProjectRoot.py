#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 17:00
# @Author  : zhangjj

import os
import platform


def get_root():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return os.path.dirname(os.path.abspath(__file__)) + separator
