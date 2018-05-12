#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 15:57
# @Author  : zhangjj
# 爬虫,网页爬取

from concurrent.futures import ThreadPoolExecutor

import Constants
from model.Entities import ManufacturerBean, ModelBean, TypeBean, UrlManager, LightBean, TechnologyBean, LightInfosBean
from service.LightInfosService import LightInfosService
from service.LightService import LightService
from service.ManufacturerService import ManufacturerService
from service.ModelService import ModelService
from service.TechnologyService import TechnologyService
from service.TypeService import TypeService
from service.UrlManagerService import UrlManagerService
from utils.StringUtil import StringUtil

import json
import requests
from logger.loggerFactory import logger


USER_AGENT = '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'''

# 网络失败重试次数
DEFAULT_FETCH_NUM = 20

urlManagerService = UrlManagerService()
manufacturerService = ManufacturerService()
modelService = ModelService()
typeService = TypeService()

# 创建线程池
executor = ThreadPoolExecutor(50)


def get_html(__url, fetch_num = None):
    if fetch_num is None:
        fetch_num = DEFAULT_FETCH_NUM
    headers = {
        'User-Agent': USER_AGENT
    }
    for i in range(0, fetch_num):
        try:
            logger.info("开始抓取[{}] : {} ".format(i + 1, __url))
            html = requests.get(__url, headers=headers)
            break
        except BaseException as e:
            pass
    html.encoding = "UTF-8"
    logger.debug(logger.info("网页内容 : {} ".format(html.text)))
    return html


def get_json(__url):
    html = get_html(__url)
    return json.loads(html.text)


def fetch_manufacturer():
    """抓取品牌"""
    if urlManagerService.has_fetch(Constants.ALL_MANUFACTURER_URL):
        logger.info("manufacturer_URL : {} 已经抓取过".format(Constants.ALL_MANUFACTURER_URL))
    else:
        all_manufacturer = get_json(Constants.ALL_MANUFACTURER_URL)
        if all_manufacturer["error"] == 0:
            all_manufacturer_dict = all_manufacturer["result"]
            for manufacturer_id in all_manufacturer_dict:
                logger.info("{} --> {}".format(manufacturer_id, all_manufacturer_dict[manufacturer_id]))
                manufacturerService.safe_insert(ManufacturerBean(StringUtil.strip(manufacturer_id),
                                                                 StringUtil.strip(all_manufacturer_dict[manufacturer_id][
                                                                                      "Manufacturer_name"])))
                all_model_url = Constants.ALL_MODEL_URL.format(manufacturer_id)
                fetch_model(all_model_url, manufacturer_id, modelService, typeService)
            urlManagerService.safe_insert(UrlManager(Constants.ALL_MANUFACTURER_URL, "manufacturer"))
        else:
            logger.info("品牌获取失败...")


def fetch_model(__url, __manufacturer_id, __modelService, __typeService):
    """抓取model数据"""
    if urlManagerService.has_fetch(__url):
        logger.info("Model_URL : {} 已经抓取过".format(__url))
    else:
        all_model = get_json(__url)
        if all_model["error"] == 0:
            all_model_list = all_model["result"]
            for modelItem in all_model_list:
                logger.info("model : {} --> {}".format(modelItem["model_id"], modelItem["model_name"]))
                __modelService.safe_insert(ModelBean(modelItem["model_id"], modelItem["model_name"], __manufacturer_id))
                all_type_url = Constants.ALL_TYPE_URL.format(modelItem["model_id"])
                fetch_type(all_type_url, __typeService)
            urlManagerService.safe_insert(UrlManager(__url, "model"))
        else:
            logger.info("model获取失败...")


def fetch_type(__url, __typeService):
    """抓取type数据"""
    if urlManagerService.has_fetch(__url):
        logger.info("type_URL : {} 已经抓取过".format(__url))
    else:
        all_type = get_json(__url)
        if all_type["error"] == 0:
            all_type_list = all_type["result"]
            for typeItem in all_type_list:
                logger.info("type : {} --> {}".format(typeItem["type_id"], typeItem))
                type_from_year = typeItem["type_from"][0:4]
                type_from_month = typeItem["type_from"][4:6]
                type_to_year = typeItem["type_to"][0:4]
                type_to_month = typeItem["type_to"][4:6]
                typeBean = TypeBean(typeItem["type_id"], typeItem["model_id"],
                                    typeItem["type_from"], type_from_year,
                                    type_from_month, typeItem["type_to"],
                                    type_to_year, type_to_month,
                                    typeItem["type_kw"], typeItem["type_axles"],
                                    typeItem["type_tonnage"], typeItem["variant_id"],
                                    typeItem["type_name"], typeItem["kba"])
                __typeService.safe_insert(typeBean)
            url_manager = UrlManager(__url, "type")
            urlManagerService.safe_insert(url_manager)
        else:
            logger.info("type获取失败...")


def fetch_all_light():
    limit = 20
    offset = 0
    count = typeService.count_type()
    while True:
        if count <= offset:
            break
        if limit > count - offset:
            limit = count - offset
        type_list = typeService.select_by_page(offset, limit)
        offset = offset + limit
        executor.submit(fetch_all_light2, LightService(), TechnologyService(), LightInfosService(), type_list)


def fetch_all_light2(lightService, technologyService, lightInfosService, type_list):
    for type in type_list:
        all_light_url = Constants.ALL_LIGHT_URL.format(type.type_id)
        if urlManagerService.has_fetch(all_light_url):
            logger.info("light_URL : {} 已经抓取过".format(all_light_url))
        else:
            all_light = get_json(all_light_url)
            if all_light["error"] == 0:
                all_light_list = all_light["result"]
                for use_id in all_light_list:
                    light = all_light_list[use_id]
                    lightBean = LightBean(type.type_id, light["use_id"], light["pos_id"], light["use_name"])
                    lightService.safe_insert(lightBean)
                    fetch_technology(technologyService, lightInfosService, type.type_id, light["use_id"])
                url_manager = UrlManager(all_light_url, "light")
                urlManagerService.safe_insert(url_manager)
            else:
                logger.info("light获取失败...")


def fetch_technology(technologyService, lightInfosService, _type_id, _use_id):
    _url = Constants.ALL_TECHNOLOGY_URL.format(_use_id, _type_id)
    if urlManagerService.has_fetch(_url):
        logger.info("technology_URL : {} 已经抓取过".format(_url))
    else:
        all_technology = get_json(_url)
        if all_technology["error"] == 0:
            all_technologys = all_technology["result"]
            for technology in all_technologys:
                if type(all_technologys) == dict:
                    technology_id = all_technologys[technology]["technology_id"]
                    technology_name = all_technologys[technology]["technology_name"]
                else:  # list
                    technology_id = technology["technology_id"]
                    technology_name = technology["technology_name"]
                technologyBean = TechnologyBean(_use_id, _type_id, technology_id, technology_name)
                technologyService.safe_insert(technologyBean)
                fetch_light_infos(lightInfosService, _use_id, _type_id, technology_id)
            url_manager = UrlManager(_url, "technology")
            urlManagerService.safe_insert(url_manager)
        else:
            logger.info("technology获取失败...")


def fetch_light_infos(lightInfosService, __use_id, __type_id, __technology_id):
    _url = Constants.LAMPS_BY_USE_URL.format(__use_id, __type_id, __technology_id)
    if urlManagerService.has_fetch(_url):
        logger.info("light_infos(lamps)_URL : {} 已经抓取过".format(_url))
    else:
        light_infos = get_json(_url)
        if light_infos["error"] == 0:
            light_info_list = light_infos["result"]
            order = 0
            for light_info in light_info_list:
                lightInfosBean = LightInfosBean(__use_id, __type_id, __technology_id, order, light_info["bullet_list"],
                                                light_info["lamp_info"], light_info["linecard_id"], light_info["linecard_name"],
                                                light_info["linksAutomotive"], light_info["osram_bestnr"], light_info["osram_ean"],
                                                light_info["osram_ece"], light_info["pillar_id"], light_info["pillar_image"],
                                                light_info["pillar_name"], light_info["prio"], light_info["product_image"],
                                                light_info["product_zmp"], light_info["usp"])
                lightInfosService.safe_insert(lightInfosBean)
                order += 1
            url_manager = UrlManager(_url, "light_infos(lamps)")
            urlManagerService.safe_insert(url_manager)
        else:
            logger.info("light_infos(lamps)获取失败...")


def fetch_all_data():
    """抓所有数据"""
    fetch_manufacturer()
    fetch_all_light()
