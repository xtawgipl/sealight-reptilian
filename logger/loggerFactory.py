#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 15:36
# @Author  : zhangjj
# @File    : loggerFactory.py

import logging
import logging.config as config
import yaml
import os

import ProjectRoot

DEFAULT_CONFIG_PATH = "logger.yml"
DEV_MODE = "dev"
PRO_MODE = "pro"
DEFAULT_MODE = PRO_MODE
ENV_KEY = 'LOG_CFG'


def setup_config():
    config_path = ProjectRoot.get_root() + DEFAULT_CONFIG_PATH
    print("日志配置文件 ： " + config_path)
    evn_config_path = os.getenv(ENV_KEY, None)
    if evn_config_path:
        config_path = evn_config_path
    if os.path.exists(config_path):
        with open(config_path, "rt") as f:
            logging.config.dictConfig(yaml.safe_load(f.read()))
    return logging.getLogger(DEFAULT_MODE)


logger = setup_config()
