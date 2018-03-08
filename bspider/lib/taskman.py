#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

logger = logging.getLogger('bspider')

from pyspider.fetcher import Fetcher as PYFetcher
from .fetcher import Fetcher
from .response import rebuild_response
from .message_queue.redis_queue import RedisQueue
from six.moves import queue as Queue
import inspect
import time
from tornado import gen, ioloop, httpclient
import random
import string

import threading


class TaskMan(object):
    '''
    Task分发器
    第一层task可能触发十个第二层task, 从而触发百个第三层task,
    每层task将被推入message_queue依次完成, 层层之间也将依次完成,
    直到最后没有任何task后结束
    '''

    def __init__(self, mname, crawler_kls, to_save, deduplicator, redis_inst, on_return_result, on_strong_fetch_error, bspider_id):
        self.crawler = crawler_kls(deduplicator, to_save)
        self.crawler.cleanup()

        self.redis = redis_inst
        self.deduplicator = deduplicator
        self.on_return_result = on_return_result
        self.on_strong_fetch_error = on_strong_fetch_error

        self.concurrency = 10

        self.mname = mname
        self.redis_queue_name = 'tq_%s_%s' % (mname, bspider_id)
        self.task_queue = RedisQueue(self.redis_queue_name, redis_inst=redis_inst)
        # self.fetcher = PYFetcher(None, None, 100, proxyer.get_random_one(), True)
        self.fetcher = Fetcher(None, None, 100)
        self.task_fetching = set()
        self.return_results_pool = []
        self.tasks_count = 0
        self.remaining_tasks_count = 0

    def _do_one_task(self, task=None):
        # logger.info(u'Now doing task (fetch & run code): %s' % task)

        if task.get('next_func') == 'on_start':
            # first loop
            following_tasks, returned_results, error_info = self.crawler.run_task({'next_func': 'on_start', 'url': ''})
            if error_info:
                self._mark_task_finished(task)
                return False
            self._put_next_tasks_into_queue(following_tasks, task)
            return False

        if not task.get('next_func'):
            self._mark_task_finished(task)
            return False

        if task.get('anti_duplicate'):
            if self.deduplicator.is_url_recorded_good(task.get('url')):
                self._mark_task_finished(task)
                return False
            if self.deduplicator.is_url_recorded_err_5times(task.get('url')):
                self.send_strong_fetch_error(task)
                self._mark_task_finished(task)
                return False

        return True

    def _on_fetch_result(self, type, task, result):
        """
        :param type: 'http', 'phantomjs', 'data' or 'none'
        :param task: task
        :param result: result
        :return:
        """
        logger.debug(u'Got fetch result...%s' % type)
        following_tasks = []
        returned_results = None

        if result.get('error'):
            self.deduplicator.record_url_err(task.get('url'))
            self._mark_task_finished(task)
            return

        response = rebuild_response(result)

        # 正常情况下不该出现exception, 如果有的话超过5次exception将加入去重池不再执行task
        try:
            following_tasks, returned_results, error_info = self.crawler.run_task(task, response)
        except Exception as e:
            error_info = str(e)

        if error_info:
            self.deduplicator.record_url_err(task.get('url'))  # 确认抓取失败后, 记录错误, 超过5次错误加入url去重池
            self._mark_task_finished(task)
            return

        if returned_results:
            self.send_returning_result(returned_results)

            if isinstance(returned_results, list):
                all_acknowledged = True
                for r in returned_results:
                    if r.get('other_acknowledged_urls'):
                        for url in r.get('other_acknowledged_urls'):
                            self.deduplicator.record_url_good(url)  # 将用户自定义的url加入url去重池

                    if not r.get('acknowledged'):
                        all_acknowledged = False

                if all_acknowledged:
                    self.deduplicator.record_url_good(task.get('url'))  # 确认抓取成功后, 加入url去重池

                self.return_results_pool += returned_results

            else:
                if returned_results.get('acknowledged'):
                    self.deduplicator.record_url_good(task.get('url'))  # 确认抓取成功后, 加入url去重池

                if returned_results.get('other_acknowledged_urls'):
                    for url in returned_results.get('other_acknowledged_urls'):
                        self.deduplicator.record_url_good(url)  # 将用户自定义的url加入url去重池

                self.return_results_pool.append(returned_results)

        self._put_next_tasks_into_queue(following_tasks, task)

    def _put_next_tasks_into_queue(self, next_tasks, original_task):
        """将tasks推入队列"""
        logger.debug(u'[%s] Next tasks: %s' % (self.mname, next_tasks))
        if next_tasks:
            for next_task in next_tasks:
                self.tasks_count += 1
                self.remaining_tasks_count += 1
                logger.debug(u'[%s] Next tasks: %s' % (self.mname, next_tasks))
                self.task_queue.put(next_task)
        self._mark_task_finished(original_task)

    def _mark_task_finished(self, original_task):
        self.remaining_tasks_count -= 1

    @gen.coroutine
    def _fetch_and_put_queue(self, next_task):
        logger.info(u'[%s] Fetching: %s' % (self.mname, next_task.get('url')))
        result = yield self.fetcher.fetch(next_task)
        logger.info(u'[%s] Fetched: %s' % (self.mname, next_task.get('url')))
        self._on_fetch_result(None, next_task, result)

    @gen.coroutine
    def _cosume_queue_loop(self):
        while self.remaining_tasks_count != 0:
            logger.debug(u'[%s] Remaining tasks in queue: %s' % (self.mname, self.remaining_tasks_count))
            try:
                next_task = self.task_queue.get_nowait()
                logger.info(u'[%s] Picking one task from queue: %s' % (self.mname, next_task.get('taskid')))
                need_to_fetch = self._do_one_task(next_task)
                if need_to_fetch:
                    logger.debug(u'[%s] Task need to fetch: %s' % (self.mname, next_task.get('taskid')))
                    # if next_task['taskid'] in self.task_fetching:
                    #     continue
                    self.task_fetching.add(next_task['taskid'])

                    logger.debug(u'[%s] Doing task fetch: %s' % (self.mname, next_task.get('taskid')))
                    yield self._fetch_and_put_queue(next_task)
                else:
                    logger.debug(u'[%s] Task does NOT need to fetch: %s' % (self.mname, next_task.get('taskid')))
                    continue

            except KeyboardInterrupt:
                return
            except Queue.Empty:
                yield gen.sleep(0.1)
                continue

    @gen.coroutine
    def loop(self):
        for _ in range(self.concurrency):
            # logger.info(u'[%s] loop %s' % (self.mname, _))
            self._cosume_queue_loop()

        while self.remaining_tasks_count != 0:
            # logger.info(u'[%s] Monitor checking remaining tasks in queue: %s' % (self.mname, self.remaining_tasks_count))
            yield gen.sleep(0.1)
        # logger.info(u'[%s] Monitor checking remaining tasks in queue: %s' % (self.mname, self.remaining_tasks_count))
        return

    def start(self):
        self.redis.delete(self.redis_queue_name)
        self.tasks_count = 1
        self.remaining_tasks_count = 1
        self._do_one_task({'next_func': 'on_start', 'url': ''})

        logger.info(u'[%s] Start looping' % self.mname)
        self.fetcher.ioloop.run_sync(self.loop)  # this might take a while, break when all tasks done
        logger.info(u'[%s] Looping ended' % self.mname)

    def send_returning_result(self, result):
        self.on_return_result(result)

    def send_strong_fetch_error(self, task):
        self.on_strong_fetch_error(task)

    @property
    def all_returned_results(self):
        return self.return_results_pool

