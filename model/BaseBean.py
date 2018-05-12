#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 14:49
# @Author  : zhangjj
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseBean(Base):
    __abstract__ = True

    """ 为所有Model提供公用方法 """
