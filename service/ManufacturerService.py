#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 14:52
# @Author  : zhangjj
from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import ManufacturerBean
from service.BaseService import BaseService


class ManufacturerService(BaseService):

    def find_by_key(self, __id, session=None):
        if session is None:
            session = DBSession()
        return session.query(ManufacturerBean).filter(ManufacturerBean.manufacturer_id == __id).first()

    def safe_insert(self, __manufacturer, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_key(__manufacturer.manufacturer_id, session) is None:
                session.add(__manufacturer)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)

if __name__ == '__main__':

    service = ManufacturerService()
    # manufacturer = ManufacturerBean(5, "test5")
    # service.insert(manufacturer)

    selectall = service.select_all(ManufacturerBean)
    logger.info("----")
    logger.info("--> {}".format(selectall))
    for item in selectall:
        logger.info(item)
