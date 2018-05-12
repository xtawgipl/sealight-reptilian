from datadource.DBManager import DBSession
from logger.loggerFactory import logger
from model.Entities import TypeBean
from service.BaseService import BaseService


class TypeService(BaseService):

    def count_type(self, session=None):
        """总数"""
        if session is None:
            session = DBSession()
        return session.query(TypeBean).count()

    def find_by_key(self, __id, session=None):
        if session is None:
            session = DBSession()
        return session.query(TypeBean).filter(TypeBean.type_id == __id).first()

    def select_by_model(self, __model_id, session=None):
        if session is None:
            session = DBSession()
        return session.query(TypeBean).filter_by(__model_id=__model_id).all()

    def safe_insert(self, __type, session=None):
        if session is None:
            session = DBSession()
        try:
            if self.find_by_key(__type.type_id, session) is None:
                session.add(__type)
                session.commit()
        except BaseException as e:
            session.rollback()
            logger.error(e)

    def select_by_page(self, offset, limit, session=None):
        """查询，offset起始位置，limit 返回条数 """
        if session is None:
            session = DBSession()
            return session.query(TypeBean).offset(offset).limit(limit).all()


if __name__ == '__main__':
    typeService = TypeService()
    logger.info(typeService.count_type())
    logger.info(typeService.select_by_page(0, 10))
