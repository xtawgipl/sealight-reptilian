#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 16:03
# @Author  : zhangjj
from datadource.DBManager import DBSession
from logger.loggerFactory import logger


class BaseService(object):
    __abstract__ = True

    def insert(self, entity, session=None):
        if session is None:
            session = DBSession()
        try:
            session.add(entity)
            session.commit()
        except BaseException as e:
            session.rollback()
            print(e)
            logger.error(e)

    def select_all(self, entity, session=None):
        if session is None:
            session = DBSession()
        return session.query(entity).all()
