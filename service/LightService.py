from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import LightBean
from service.BaseService import BaseService


class LightService(BaseService):

    def find_by_keys(self, __type_id, __use_id, __pos_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(LightBean)\
            .filter(LightBean.type_id == __type_id) \
            .filter(LightBean.use_id == __use_id) \
            .filter(LightBean.pos_id == __pos_id).first()

    def select_by_type(self, __type_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(LightBean).filter_by(type_id=__type_id).all()

    def safe_insert(self, __light, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_keys(__light.type_id, __light.use_id, __light.pos_id, session) is None:
                session.add(__light)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)
