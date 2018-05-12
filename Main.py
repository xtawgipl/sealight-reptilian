#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 16:11
# @Author  : zhangjj


import Reptilian
from OutputExcel import OutputExcel

if __name__ == '__main__':
    # Reptilian.fetch_all_data()

    excelUtil = OutputExcel()
    excelUtil.export_excel()
