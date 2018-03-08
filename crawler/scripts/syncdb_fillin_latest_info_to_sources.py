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
items = maindb['items']

def sync_sources():
    for source in sources.find().limit(1000):
        latest_item = [i for i in items.find({'source': source.get('machine_name')}, {'_id': 0}).sort([('ctime', -1)]).limit(1)]

        if not latest_item:
            continue

        to_set = {
            'latestArticleTitle': latest_item[0].get('title'),
            'latestArticleCreated': latest_item[0].get('ctime'),
        }

        sources.update({
            'machine_name': source.get('machine_name')
        }, {
            '$set': to_set
        })


if __name__ == '__main__':
    sync_sources()