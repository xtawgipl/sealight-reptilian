#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 14:43
# @Author  : zhangjj
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from datadource import DBConfig

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(DBConfig.DB_USER, DBConfig.DB_PASSWORD, DBConfig.DB_HOST, DBConfig.DB_PORT, DBConfig.DB_DBNAME), connect_args={'charset': 'UTF8'}, echo=True, encoding='UTF-8')
session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)

