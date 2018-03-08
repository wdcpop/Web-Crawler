#!/usr/bin/env python
# coding:utf8
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import threading

from pyquery import PyQuery
import requests
import json
from random import choice
from arrow import Arrow

# reload(sys)
# sys.setdefaultencoding('utf8')
import traceback

from lib.helper import app_config

import re
import hashlib
import signal
import Queue
import multiprocessing
import time
import arrow
from bspider.lib.deduplicator import Deduplicator

from weibo import login_pre, login
from Sina_spider3.Sina_spider3.cookies import getCookie

# logging
import logging
from logging import FileHandler
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('weibo_crawler')

# data
from pymongo import MongoClient
from redis import StrictRedis, ConnectionPool

redis = StrictRedis(connection_pool=ConnectionPool())
deduplicator = Deduplicator(redis)

db = MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'])
maindb = db[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
weibo_items = maindb['weibo_items']



def get_info(session, cookies):
    if session:
        r = session.get("http://m.weibo.cn/index/feed?format=cards")
    else:
        r = requests.get("http://m.weibo.cn/index/feed?format=cards", cookies=cookies)

    try:
        result = r.json()
    except Exception as e:
        logger.exception(e)
        logger.info('请求返回错误, 请检查')
        return False

    if isinstance(result, dict):
        if result.get("msg") == u"请先登录":
            logger.error('返回需要登录, 请检查')
            return False

    if not result[0] or not result[0].get('card_group') or not len(result[0].get('card_group')):
        logger.error('返回字段错误, 请检查')
        return False

    count = len(result[0].get("card_group"))
    text_list = []

    for obj_arr in result[0].get("card_group"):
        save_obj = {}
        obj = obj_arr.get("mblog")

        # uniq = hashlib.md5(obj.get("text").encode('utf-8')).hexdigest()
        if deduplicator.is_url_recorded('wb_id_%s' % obj.get("id")):
            continue

        save_obj["item_id"] = obj.get("id")
        save_obj["item_bid"] = obj.get("bid")

        user = obj.get('user')
        if user:
            save_obj["source_id"] = obj.get("user").get("id")
            save_obj["source_name"] = obj.get("user").get("screen_name")
        save_obj["name"] = save_obj.get("source_name", "nobody")

        clean_text = PyQuery(obj.get("text")).text()
        title_found_all = re.match(ur'.*【(.*?)】', clean_text)
        title = title_found_all.group(1) if title_found_all else clean_text
        save_obj["title"] = title

        save_obj["content"] = obj.get("text")
        save_obj["original_pic"] = obj.get("original_pic")

        save_obj["pics"] = [_.get('url') for _ in obj.get("pics", [])]

        page_info = obj.get('page_info')
        if page_info:
            save_obj["page_id"] = page_info.get('page_id')
            save_obj["page_url"] = page_info.get('page_url')
            save_obj["page_pic"] = page_info.get('page_pic')

        save_obj["ctime"] = arrow.utcnow().timestamp
        save_obj["time"] = obj.get("created_timestamp")
        save_obj["link"] = "http://weibo.com/%s/%s" % (save_obj.get("source_id"), save_obj["item_bid"])

        inserted = weibo_items.insert_one(save_obj)
        deduplicator.record_url_good('wb_id_%s' % obj.get("id"))
        text_list.append(obj.get("text")[:10])
        redis.publish('weibo_news_updated', str(inserted.inserted_id))

    logger.info(u'抓取到消息: %s, 去重后收集消息: %s' % (count, text_list))
    return True


def start():
    # pincode = login_pre('zhuyuhao@wallstreetcn.com')
    # if not pincode:
    #     session = login('zhuyuhao@wallstreetcn.com', 'rocksXGB123!', '')
    # else:
    #     session = login('zhuyuhao@wallstreetcn.com', 'rocksXGB123!', pincode)

    c = getCookie(u'zhuyuhao@wallstreetcn.com', 'rocksXGB123!')
    cookies = json.loads(c)

    while True:
        try:
            if_continue = get_info(None, cookies)
        except Exception as e:
            logger.exception(e)
            logger.info('code error')
            if_continue = False
        if not if_continue:
            break
        time.sleep(choice([11.8, 12.3, 13.1, 15.5]))


def main():
    i = 1
    while True:
        start()
        logger.error('启动程序退出, 等待%s秒后重新登录抓取' % str(i*600))
        time.sleep(i*600)
        i += 1

if __name__ == '__main__':
    def setup_logger_global(name, single=False):
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s][%(name)s] => %(message)s')

        filename = 'logs/%s.log' % name

        handler = RotatingFileHandler(filename, mode='a', maxBytes=200 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(getattr(logging, 'INFO'))
        log.addHandler(handler)

    setup_logger_global('weibo_crawler')

    main()
