#!/usr/bin/env python
# coding:utf8

import logging

global_logger = logging.getLogger('ResultHandler')

import sys
import json
import time
from datetime import datetime
from time import sleep

from pymongo import MongoClient
from redis import StrictRedis, ConnectionPool
from bspider.result_handlers.basic_result_handler import BasicResultHandler
from lib.helper import app_config


class MyResultHandler(BasicResultHandler):
    def __init__(self, spider_mname, to_save):
        self.spider_mname = spider_mname

        self.logger = logging.getLogger(self.spider_mname)

        self.redis = StrictRedis(
            host=app_config['REDIS_TO_SEND_RESULT']['HOST'],
            port=app_config['REDIS_TO_SEND_RESULT']['PORT'],
            password=app_config['REDIS_TO_SEND_RESULT']['PASS'],
            db=app_config['REDIS_TO_SEND_RESULT']['DB']
        )

        self.client = MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'])
        self.content_db = self.client[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
        self.items_table = self.content_db['ann_items']
        self.err_items_table = self.content_db['ann_err_items']

    def on_new_result(self, result):
        '''返回一个url的抓取结果(如果成功且为新)'''
        global_logger.debug(u'[{}]有新的抓取结果: '.format(result))
        pass

    def on_new_results(self, results, total_time, urls_count=None, crawler=None):
        '''返回一整次抓取的所有结果(仅返回成功且为新的结果)'''
        links_count = urls_count - 1

        # 清洗results, 每个result必需标题和内容有一个不为空
        filtered_results = [r for r in results if r and (r.get('title') or r.get('content'))]

        log_results = u'[{}]完整抓取结果已返回, 链接个数:{}, 所有新抓取个数:{}, 有结果的新抓取个数:{}, 使用的代理:{}, 耗时{:.2f}秒'.format(
            self.spider_mname, links_count, len(results), len(filtered_results), crawler.actual_proxy, total_time)
        global_logger.info(log_results)
        self.logger.info(log_results)

        if not filtered_results:
            return

        results = filtered_results

        log_new_results = u'[{}]新抓取的结果: [{}]'.format(self.spider_mname, ', '.join([r.get('title', '')[:10] for r in results]))
        global_logger.info(log_new_results)
        self.logger.info(log_new_results)

        crawled = dict(
            name=self.spider_mname,
            result_count=len(results),
            crawl_count=links_count,
            totalTime=total_time
        )
        try:
            self.redis.publish('ann_crawled', json.dumps(crawled))
        except Exception as e:
            self.logger.exception(e)
            self.logger.info(u'[{}]发送给redis:crawled失败: {}'.format(self.spider_mname, json.dumps(crawled)))

        if len(results) > 0:
            global_logger.debug(u'{0: <30}更新:{1}'.format(self.spider_mname, len(results)))
            for i in results:
                if not i.get('title') and not i.get('content'):
                    continue

                i['source'] = self.spider_mname
                try:
                    inserted = self.items_table.insert_one(i)
                except Exception as e:
                    self.logger.exception(e)
                    self.logger.info(u'[{}]新结果插入数据库失败: {}'.format(self.spider_mname, i))
                    continue

                if not inserted:
                    self.logger.info(u'[{}]新结果插入数据库失败: {}'.format(self.spider_mname, i))
                    continue

                self.logger.info(u'[{}]新结果已插入数据库, 返回的objectId: {}'.format(self.spider_mname, str(inserted.inserted_id)))

                try:
                    self.redis.publish('ann_news_updated', str(inserted.inserted_id))
                except Exception as e:
                    self.logger.exception(e)
                    self.logger.info(u'[{}]发送给redis:news_updated失败: {}'.format(self.spider_mname, str(inserted.inserted_id)))
        self.logger.info(u'[{}]结果处理完成。'.format(self.spider_mname))

    def on_strong_fetch_error(self, task):
        '''返回一个url的超过5次错误后的抓取结果'''
        global_logger.error(u'[{}]严重的抓取错误: '.format(self.spider_mname, task))
        # self.err_items_table.update({'url': task.get('url')}, task, True)  # type:dict
