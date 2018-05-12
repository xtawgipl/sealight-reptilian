#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 22:35
# @Author  : zhangjj
import xlwt

import Constants

if __name__ == '__main__':
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("see", cell_overwrite_ok=True)
    sheet.write(0, 1, "sfsafasdfadsfadf\nsfalkjkasdfjsafjl\n\rlkjsfldskjdsf",
                xlwt.easyxf('align: wrap on, vert center;align: horiz center'))
    workbook.save(Constants.EXCEL_PATH + "{}.xls".format("saaaa"))