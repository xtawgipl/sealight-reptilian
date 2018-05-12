#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 15:40
# @Author  : zhangjj
# 常量类

# 生成的excel表存放地址
EXCEL_PATH = "D:/data/"

# 获取所有品牌如 BMW等
ALL_MANUFACTURER_URL = "https://am-application.osram.info/en/getAllManufacturer/1.json"

# 获取品牌的所有系列(型号),如 BMW的 x5 x6等
# 占位符为品牌的id,如BMW的品牌id为6
ALL_MODEL_URL = "https://am-application.osram.info/en/getAllModel/{}/1.json"

# 根据车型号id查所有灯
# 占位符为型号的id,如X5的型号id为7552
ALL_TYPE_URL = "https://am-application.osram.info/en/getAllType/{}.json"

# 根据type_id获取对应下的所有灯（包括前 后 类 三种灯）,占位符为type_id
ALL_LIGHT_URL = "https://am-application.osram.info/en/getAllUse/{}.json"

# 根据 use_id, type_id获取灯的工艺类型，第一个点位符为use_id 第二个为type_id
ALL_TECHNOLOGY_URL = "https://am-application.osram.info" \
                     "/en/getAllTechnology/{}/{}.json"

# 根据 use_id, type_id， technology_id 获取 灯详情; 第一个点位符为use_id 第二个为type_id 第三个为technology_id
LAMPS_BY_USE_URL = "https://am-application.osram.info/en/getLampsByUse/{}/{}/{}.json"

# 前灯pos_id集合
FRONT_POS_ID_LIST = [409]

# 后灯pos_id集合
REAR_POS_ID_LIST = [410]

# 内类pos_id集合
INTERNAL_POS_ID_LIST = [411]
