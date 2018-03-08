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
    for source_name, source_kls in crawler_class_dict.iteritems():
        print source_name

        to_set = {
            'start_urls': source_kls.start_urls
        }

        if hasattr(source_kls, 'title'):
            to_set.update({'title': source_kls.title})

        if hasattr(source_kls, 'url_links_selector'):
            to_set.update({'url_links_selector': source_kls.url_links_selector})

        if hasattr(source_kls, 'content_selector'):
            to_set.update({'content_selector': source_kls.content_selector})

        if hasattr(source_kls, 'url_area_selector'):
            to_set.update({'url_area_selector': source_kls.url_area_selector})

        if hasattr(source_kls, 'url_patterns'):
            to_set.update({'url_patterns': [_.pattern for _ in source_kls.url_patterns]})

        if hasattr(source_kls, 'headers'):
            to_set.update({'headers': source_kls.headers})

        print to_set

        sources.update({'machine_name': source_name}, {
            '$set': to_set
        }, upsert=True)

if __name__ == '__main__':
    sync_sources()