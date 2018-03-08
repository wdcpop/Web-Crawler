#!/usr/bin/env python
# coding:utf8
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), os.pardir))

import json

from pymongo import MongoClient

from crawler.crawlers import crawler_class_dict
from lib.helper import app_config
db = MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'], connect=False)
maindb = db[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
sources = maindb['sources']


def sync_sources():
    for source_name, source_kls in sources.find():
        print source_name

        to_set = {
            'start_urls': source_kls.start_urls
        }

        if hasattr(source_kls, 'title'):
            to_set.update({'title': source_kls.title})

        if hasattr(source_kls, 'source_title'):
            to_set.update({'source_title': source_kls.source_title})

        print to_set

        sources.update({'machine_name': source_name}, {
            '$set': to_set
        }, upsert=True)


if __name__ == '__main__':
    sync_sources()