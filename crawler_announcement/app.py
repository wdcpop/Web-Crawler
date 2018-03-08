#!/usr/bin/env python
# coding:utf8
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import threading

import json
from random import choice
from arrow import Arrow

# reload(sys)
# sys.setdefaultencoding('utf8')
import traceback

from bspider import BSpider
from crawler_announcement.crawlers import crawler_class_dict, crawler_class_list
from lib.helper import app_config
from lib.proxies import get_proxy_urls
from crawler_announcement.result_handlers.my_result_handler import MyResultHandler

import signal
import Queue
import multiprocessing
import time

# logging
import logging
from logging import FileHandler
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('App')

# data
from pymongo import MongoClient
from redis import StrictRedis, ConnectionPool

redis = StrictRedis(connection_pool=ConnectionPool())
db = MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'])
maindb = db[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
sources = maindb['sources']
source_default_configs = maindb['sourceDefaultConfigs']


class App():
    """爬虫池管理者"""
    def __init__(self):
        pass

    def start_one(self, name):
        def process_start():
            bs = BSpider(
                crawler_class_dict[name],
                MyResultHandler,
                redis,
                delay=10,
                machine_name=name,
                do_not_send_on_first_fetch=True,
                deduplicate_prefix='blf_annc')
            bs.run()

        p = multiprocessing.Process(target=process_start)

        try:
            p.start()
        except KeyboardInterrupt:
            print 'Keyboard exit'

    def start(self):
        """
        启动所有爬虫
        """
        logger.info(u'启动所有爬虫中...')
        for n in crawler_class_list:
            self.start_one(n)

        logger.info(u'所有爬虫已启动')


def main():
    app = App()
    app.start()


if __name__ == '__main__':
    def setup_logger_global(name, single=False):
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s][%(name)s] => %(message)s')

        filename = 'logs/crawler_announcement.log'

        handler = RotatingFileHandler(filename, mode='a', maxBytes=200 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(getattr(logging, 'INFO'))
        log.addHandler(handler)


    def setup_logger_single(name):
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s][%(name)s] => %(message)s')

        handler = RotatingFileHandler('logs/crawlers_announcement/%s.log' % name, mode='a', maxBytes=5 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(getattr(logging, 'INFO'))
        log.addHandler(handler)


    for name, crawler_kls in crawler_class_dict.iteritems():
        setup_logger_single(name)

    setup_logger_global('bspider')
    setup_logger_global('App')
    setup_logger_global('fetcher')
    setup_logger_global('ResultHandler')

    main()
