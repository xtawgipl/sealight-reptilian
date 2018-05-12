from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import UrlManager
from service.BaseService import BaseService


class UrlManagerService(BaseService):

    def find_by_key(self, __id, session=None):
        if session is None:
            session = DBSession()
        return session.query(UrlManager).filter(UrlManager.id == __id).first()

    def find_by_url(self, __url, session=None):
        if session is None:
            session = DBSession()
        return session.query(UrlManager).filter(UrlManager.url == __url).first()

    def has_fetch(self, __url, session=None):
        if session is None:
            session = DBSession()
        url_manager = self.find_by_url(__url, session)
        if url_manager is None:
            return False
        else:
            return True

    def safe_insert(self, __url_manager, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_key(__url_manager.id, session) is None:
                session.add(__url_manager)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)
