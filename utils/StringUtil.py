#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 15:40
# @Author  : zhangjj
# 字符串工具类


class StringUtil(object):

    @staticmethod
    def strip(_str):
        """去掉字符串两头的引号"""
        return _str.lstrip("\"").lstrip("'").rstrip("\"").rstrip("'")


if __name__ == '__main__':
    print(StringUtil.strip("\"'sfsfsdf'\""))