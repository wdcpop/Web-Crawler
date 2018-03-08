#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

import requests
from lib.taskman import TaskMan
from lib.deduplicator import Deduplicator
from lib.utils import md5randomstring
import time


class BSpider(object):
    def __init__(self, crawler_kls, result_handler_kls, redis, **kwargs):
        self.mname = kwargs.get('machine_name', 'bspider_%s' % md5randomstring())
        self.to_save = kwargs.get('to_save', {})

        self.logger = logging.getLogger(self.mname)
        self.crawler_kls = crawler_kls
        self.result_handler = result_handler_kls(self.mname, self.to_save)

        self.delay = kwargs.get('delay', 2)

        self.redis = redis
        self.deduplicate_prefix = kwargs.get('deduplicate_prefix', 'blf')
        self.deduplicator = Deduplicator(redis, self.deduplicate_prefix)

        self.do_not_send_on_first_fetch = kwargs.get('do_not_send_on_first_fetch', True)
        self.is_first_fetch = True

        self.to_kill_callback = kwargs.get('to_kill_callback')
        self.killed_callback = kwargs.get('killed_callback')

        self.bspid = self.get_bspider_id()

    def get_bspider_id(self):
        import random
        import string
        s = string.lowercase + string.digits
        return ''.join(random.sample(s, 10))

    def run(self, **kwargs):
        self.logger.info(u'%s start running ...' % self.mname)
        try:
            while True:
                taskman = TaskMan(self.mname, self.crawler_kls, self.to_save, self.deduplicator, self.redis,
                                  self.send_returning_result, self.send_strong_fetch_error, self.bspid)
                st = time.time()
                taskman.start()
                ed = time.time()
                t = ed - st
                if self.do_not_send_on_first_fetch and self.is_first_fetch:
                    self.logger.info(u'[{}]完整抓取结果已返回, 耗时{:.2f}秒, 链接数量:[{}], 但是跳过第一次抓取已启用, 跳过!'.format(
                        self.mname, t, taskman.tasks_count))
                    self.is_first_fetch = False
                else:
                    self.send_all_returning_results(taskman.all_returned_results, ed - st, taskman.tasks_count, taskman.crawler)
                if self.to_kill_callback:
                    signal = self.to_kill_callback()
                    if signal:
                        self.logger.info(u'[%s]收到停止信号, 终止循环并退出' % (self.mname))
                        if self.killed_callback:
                            self.killed_callback()
                        return
                del taskman
                time.sleep(self.delay)
        except KeyboardInterrupt:
            print 'Keyboard exit'

    def send_returning_result(self, result):
        try:
            self.result_handler.on_new_result(result)
        except Exception as e:
            self.logger.exception(e)

    def send_all_returning_results(self, results, total_time, tasks_count, crawler):
        try:
            self.result_handler.on_new_results(results, total_time, tasks_count, crawler)
        except Exception as e:
            self.logger.exception(e)

    def send_strong_fetch_error(self, task):
        try:
            self.result_handler.on_strong_fetch_error(task)
        except Exception as e:
            self.logger.exception(e)
