from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import LightInfosBean
from service.BaseService import BaseService


class LightInfosService(BaseService):

    def find_by_keys(self, __type_id, __use_id, __technology_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(LightInfosBean)\
            .filter(LightInfosBean.type_id == __type_id) \
            .filter(LightInfosBean.use_id == __use_id) \
            .filter(LightInfosBean.technology_id == __technology_id).first()

    def safe_insert(self, __light_infos, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_keys(__light_infos.type_id, __light_infos.use_id, __light_infos.technology_id, session) is None:
                session.add(__light_infos)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)