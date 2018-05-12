from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import TechnologyBean
from service.BaseService import BaseService


class TechnologyService(BaseService):

    def find_by_keys(self, __type_id, __use_id, __technology_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(TechnologyBean)\
            .filter(TechnologyBean.type_id == __type_id) \
            .filter(TechnologyBean.use_id == __use_id) \
            .filter(TechnologyBean.technology_id == __technology_id).first()

    def find_by_type_use(self, __type_id, __use_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(TechnologyBean)\
            .filter(TechnologyBean.type_id == __type_id) \
            .filter(TechnologyBean.use_id == __use_id).all()

    def safe_insert(self, __technology, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_keys(__technology.type_id, __technology.use_id, __technology.technology_id, session) is None:
                session.add(__technology)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)