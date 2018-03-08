#!/usr/bin/env python
# coding:utf8

import dotenv
import yaml
import os
from random import choice
from .proxies import proxy_list

cur_path = os.path.dirname(os.path.realpath(__file__))


def get_config():
    env = dotenv.get_key('%s/../.env' % cur_path, 'env')
    config = yaml.safe_load(open("%s/../configs/config.%s.yml" % (cur_path, env)))
    return config

app_config = get_config()


def get_proxy(proxy_type):
    """
    :type proxy_type:int
    """
    if proxy_type:
        if proxy_type == 1:
            proxy_choosed = choice(proxy_list)
            return {"http": proxy_choosed, "https": proxy_choosed}
        elif proxy_type == 2:
            return {
                'http': app_config['FOREIGN_PROXIE'],
                'https': app_config['FOREIGN_PROXIE']
            }