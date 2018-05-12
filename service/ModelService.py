#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 17:35
# @Author  : zhangjj
from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import ModelBean
from service.BaseService import BaseService


class ModelService(BaseService):

    def find_by_key(self, __id, session=None):
        if session is None:
            session = DBSession()
        return session.query(ModelBean).filter(ModelBean.model_id == __id).first()

    def select_by_manufacturer(self, __manufacturer_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(ModelBean).filter_by(manufacturer_id=__manufacturer_id).all()

    def safe_insert(self, __model, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_key(__model.model_id, session) is None:
                session.add(__model)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)


if __name__ == '__main__':
    service = ModelService()
    # model = ModelBean(2, "test53223", 1)
    # service.insert(model)
    #
    # selectall = service.select_all(ModelBean)
    # logger.info("----")
    # logger.info("--> {}".format(selectall))

    model = service.find_by_key(11)
    logger.info("----")
    logger.info(model)
    logger.info("2222")

