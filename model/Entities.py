#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 10:09
# @Author  : zhangjj
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from model.BaseBean import BaseBean


class UrlManager(BaseBean):
    """url管理器"""
    def __init__(self, url, type_name):
        self.url = url
        self.type_name = type_name

    # 表名:
    __tablename__ = 't_url_manager'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    type_name = Column(String(10))
    url = Column(String(2048))

    def __repr__(self):
        return "id = {}, type_name = {}, url = {}".format(self.id, self.type_name, self.url)


class ManufacturerBean(BaseBean):
    """
    品牌类
    """

    def __init__(self, manufacturer_id, manufacturer_name):
        self.manufacturer_id = manufacturer_id
        self.manufacturer_name = manufacturer_name

    # 表名:
    __tablename__ = 't_manufacturer'
    # 表的结构:
    manufacturer_id = Column(Integer, primary_key=True)
    manufacturer_name = Column(String(2048))
    # 一对多
    modelList = relationship('ModelBean', cascade='all', backref="t_manufacturer")

    def __repr__(self):
        return "manufacturer_id = {}, manufacturer_name = {}, modelList = {}".\
            format(self.manufacturer_id, self.manufacturer_name, self.modelList)


class ModelBean(BaseBean):
    """
    车系列类
    """
    def __init__(self, model_id, model_name, manufacturer_id):
        self.model_id = model_id
        self.model_name = model_name
        self.manufacturer_id = manufacturer_id

    # 表名:
    __tablename__ = 't_model'
    # 表的结构:
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String(2048))
    # “多”的一方的ModelBean表是通过外键关联到manufacturer表的:
    manufacturer_id = Column(Integer, ForeignKey('t_manufacturer.manufacturer_id'))
    manufacturerInfo = relationship(ManufacturerBean)
    typeList = relationship('TypeBean', cascade='all', backref="t_model")

    def __repr__(self):
        return "model_id = {}, model_name = {}, manufacturer_id = {}".\
            format(self.model_id, self.model_name, self.manufacturer_id)


class TypeBean(BaseBean):
    """
    类型表类
    """

    # 表名:
    __tablename__ = 't_type'
    # 表的结构:
    type_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('t_model.model_id'))
    type_from = Column(String(50))
    type_from_year = Column(String(50))
    type_from_month = Column(String(50))
    type_to = Column(String(50))
    type_from = Column(String(50))
    type_to_year = Column(String(50))
    type_to_month = Column(String(50))
    type_kw = Column(String(50))
    type_axles = Column(String(50))
    type_to_year = Column(String(50))
    type_tonnage = Column(String(50))
    variant_id = Column(Integer)
    type_name = Column(String(50))
    kba = Column(String(50))

    modelInfo = relationship(ModelBean)

    lightList = relationship('LightBean', cascade='all', backref="t_type")

    def __init__(self, type_id, model_id, type_from, type_from_year, type_from_month,
                 type_to, type_to_year, type_to_month, type_kw, type_axles, type_tonnage,
                 variant_id, type_name, kba):
        self.type_id = type_id
        self.model_id = model_id
        self.type_from = type_from
        self.type_from_year = type_from_year
        self.type_from_month = type_from_month
        self.type_to = type_to
        self.type_to_year = type_to_year
        self.type_to_month = type_to_month
        self.type_kw = type_kw
        self.type_axles = type_axles
        self.type_tonnage = type_tonnage
        self.variant_id = variant_id
        self.type_name = type_name
        self.kba = kba

    def __repr__(self):
        return "type_id = {}, model_id = {}, type_from = {}, type_from_year = {}, type_from_month = {}, " \
               "type_to = {}, type_to_year = {}, type_to_month = {}, type_kw = {}, type_axles = {}, " \
               "type_tonnage = {}, variant_id = {}, type_name = {}, kba = {}".\
            format(self.type_id, self.model_id, self.type_from, self.type_from_year, self.type_from_month,
                   self.type_to, self.type_to_year, self.type_to_month, self.type_kw, self.type_axles,
                   self.type_tonnage, self.variant_id, self.type_name, self.kba)


class LightBean(BaseBean):
    """
    light表
    """

    # 表名:
    __tablename__ = 't_light'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('t_type.type_id'))
    use_id = Column(Integer)
    pos_id = Column(Integer)
    use_name = Column(String(512))

    typeInfo = relationship(TypeBean)

    def __init__(self, type_id, use_id, pos_id, use_name):
        self.type_id = type_id
        self.use_id = use_id
        self.pos_id = pos_id
        self.use_name = use_name

    def __repr__(self):
        return "id = {}, type_id = {}, use_id = {}, pos_id = {}, use_name = {}".\
            format(self.id, self.type_id, self.use_id, self.pos_id, self.use_name)


class TechnologyBean(BaseBean):
    """
    technology表
    """

    # 表名:
    __tablename__ = 't_technology'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    use_id = Column(Integer)
    type_id = Column(Integer)
    technology_id = Column(Integer)
    technology_name = Column(String(512))

    def __init__(self, use_id, type_id, technology_id, technology_name):
        self.use_id = use_id
        self.type_id = type_id
        self.technology_id = technology_id
        self.technology_name = technology_name

    def __repr__(self):
        return "id = {}, use_id = {}, type_id = {}, technology_id = {}, technology_name = {}".\
            format(self.id, self.use_id, self.type_id, self.technology_id, self.technology_name)


class LightInfosBean(BaseBean):
    """
    light_infos(lamp 灯详情,一个light可应对多个lamp)表
    """

    # 表名:
    __tablename__ = 't_light_infos'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    use_id = Column(Integer)
    type_id = Column(Integer)
    technology_id = Column(Integer)
    order = Column(Integer)
    bullet_list = Column(Text(512))
    lamp_info = Column(String(256))
    linecard_id = Column(Integer)
    linecard_name = Column(String(256))
    linksAutomotive = Column(String(256))
    osram_bestnr = Column(String(256))
    osram_ean = Column(String(256))
    osram_ece = Column(String(256))
    pillar_id = Column(Integer)
    pillar_image = Column(String(256))
    pillar_name = Column(String(256))
    prio = Column(String(256))
    product_image = Column(String(256))
    product_zmp = Column(String(256))
    usp = Column(String(256))

    def __init__(self, use_id, type_id, technology_id, order, bullet_list,
                 lamp_info, linecard_id, linecard_name, linksAutomotive,
                 osram_bestnr, osram_ean, osram_ece, pillar_id, pillar_image,
                 pillar_name, prio, product_image, product_zmp, usp):
        self.use_id = use_id
        self.type_id = type_id
        self.technology_id = technology_id
        self.order = order
        self.bullet_list = bullet_list
        self.lamp_info = lamp_info
        self.linecard_id = linecard_id
        self.linecard_name = linecard_name
        self.linksAutomotive = linksAutomotive
        self.osram_bestnr = osram_bestnr
        self.osram_ean = osram_ean
        self.osram_ece = osram_ece
        self.pillar_id = pillar_id
        self.pillar_image = pillar_image
        self.pillar_name = pillar_name
        self.prio = prio
        self.product_image = product_image
        self.product_zmp = product_zmp
        self.usp = usp

    def __repr__(self):
        return "id = {}, use_id = {}, type_id = {}, technology_id = {}, order = {}, osram_ece = {}".\
            format(self.id, self.use_id, self.type_id, self.technology_id, self.order, self.osram_ece)


if __name__ == '__main__':
    print(UrlManager("1112", "11212"))
    print(ManufacturerBean("1112", "11212"))
