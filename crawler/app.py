#!/usr/bin/env python
# coding:utf8
import sys, os, gc

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#sys.path.append("/home/wdcpop/WALL/NewsCrawler/crawler/crawlers/abstracts")
import threading

import json
from random import choice
from arrow import Arrow
# reload(sys)
# sys.setdefaultencoding('utf8')
import traceback

from bspider import BSpider
from lib.helper import app_config
from lib.proxies import get_proxy_urls

from crawler.crawlers.abstracts.crawler_abstract import CrawlerAbstract
from crawler.result_handlers.my_result_handler import MyResultHandler
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
        self.init()
        self.under_command = False

    def cleanup(self):
        self.default_delay = None
        self.default_proxy_type = None
        if hasattr(self, 'pool'):
            del self.pool
        self.pool = None
        gc.collect()

    def init(self):
        self.cleanup()
        crawler_configs = {row.get('machine_name'): row
                                for row in sources.find() if row.get('machine_name') and not row.get('disabled')}

        crawler_default_configs = source_default_configs.find_one()
        self.default_delay = crawler_default_configs['default_delay']
        self.default_proxy_type = crawler_default_configs[
            'default_proxy']  # -1: No proxy / 1: kuaidaili proxy / 2: overseas proxy/ 5: proxy list in db

        actual_crawling_names = []

        # 测试单(多)个爬虫, 示例: python crawler/app.py aastocks cb baijia
        if len(sys.argv) >= 2:
            names = [_ for i, _ in enumerate(sys.argv) if i >= 1]
            for name in names:
                # print name
                # 需要debug数据库配置时, 取消以下两行注释
                # if name.upper() not in self.crawler_configs:
                #     continue
                if crawler_configs.get(name.upper(), {}).get('start_urls'):
                    actual_crawling_names.append(name.upper())
        else:
            # 将数据库内的所有爬虫名单遍历
            for crawler_name in crawler_configs:
                # 如果数据库内的爬虫名称不在文件列表内, 跳过
               # if crawler_name not in crawler_class_list:
                #    continue
                if crawler_configs[crawler_name].get('start_urls'):
                    actual_crawling_names.append(crawler_name)

        self.pool = {name: {
            'queue1': None,
            'queue2': None,
            'stopped': False,
            # 'reloaded': False,
            'p': None,
        } for name in actual_crawling_names}

        return crawler_configs

    def pre_start_one(self, name, single_config, do_not_send_on_first_fetch=True):
        from crawlers import crawler_class_dict
        delay_sec = single_config.get('delay_sec')
        delay_sec = delay_sec if delay_sec else self.default_delay
        delay_sec = int(delay_sec)
        single_config['delay_sec'] = delay_sec
        proxy_type = single_config.get('proxy_type')
        proxy_type = proxy_type if proxy_type else self.default_proxy_type
        single_config['proxy_type'] = int(proxy_type)


        running_craw_name = crawler_class_dict.get(name)
        if running_craw_name:
            print 'local. ..'
            crawler_class = crawler_class_dict[name]
        else:
            crawler_class = CrawlerAbstract


        #
        # proxy_list = []
        # if proxy_type == -1:
        #     proxy_list = []
        # elif proxy_type == 1:
        #     proxy_list = get_proxy_urls()
        # elif proxy_type == 2:
        #     proxy_list = [app_config['FOREIGN_PROXIE']]

        queue1 = multiprocessing.Queue()
        queue2 = multiprocessing.Queue()

        # 信号1, 给子进程调用以终止它的抓取循环
        def to_kill():
            try:
                r = queue1.get_nowait()
            except Queue.Empty:
                r = None
            if r == 'to_stop':
                return True
            else:
                return False

        # 信号2, 给子进程调用以通知主进程它已经结束了
        def killed():
            queue2.put_nowait('stopped')

        def process_start(crawler_class):
            # running_craw_name = crawler_class_dict.get(name)
            # if not running_craw_name:     # need more config to test on the url
            #     print ' we are now running crawlers from DB...'
            #     online_crawler = CrawlerAbstract
            # else:
            #     if not single_config.get('start_urls'):
            #         logger.info(u'No result find from the current DataBase Collections: {}'.format(running_craw_name))
            #         return

            bs = BSpider(
                crawler_class,
                MyResultHandler,
                redis,
                delay=delay_sec,
                machine_name=name,
                do_not_send_on_first_fetch=False,
                to_save={'config': single_config},
                to_kill_callback=to_kill,
                killed_callback=killed)
            bs.run()

        p = multiprocessing.Process(target=process_start, args=(crawler_class,))

        self.pool[name].update({'queue1': queue1, 'queue2': queue2, 'p': p})

    def stop_one(self, name):
        # self.pool[name]['queue1'].put_nowait('to_stop')
        self.pool[name]['p'].terminate()

    def stop(self):
        """
        停止所有爬虫, 发送信号, 需要等待, 请勿在未完全停止的情况下再次启动
        """
        logger.info(u'停止所有爬虫中...')
        for n in self.pool:
            self.stop_one(n)
        logger.info(u'已发送停止信号给所有爬虫')

    def start(self, do_not_send_on_first_fetch=True):
        """
        启动所有爬虫
        """
        crawler_configs = self.init()
        logger.info(u'启动所有爬虫中...')
        for n in self.pool:
            single_config = crawler_configs.get(n, {})
            self.pre_start_one(n, single_config, do_not_send_on_first_fetch)

        del crawler_configs
        try:
            for n in self.pool:
                self.pool[n]['p'].start()
        except KeyboardInterrupt:
            print 'Keyboard exit'

        logger.info(u'所有爬虫已启动')

    def restart(self):
        """
        重启所有爬虫(硬重启): 也就是全停再全启, 更安全
        需要等待所有爬虫都停止, 再统一启动
        """

        logger.info(u'重启所有crawler中...')
        if self.under_command:
            logger.info(u'有其他命令正在执行中, 请稍后...')
            return
        self.under_command = True

        pool = {name: self.pool[name] for name in self.pool if self.pool[name]['p'].is_alive()}
        self.stop()

        logger.info(u'Wait for all the running crawlers...')
        while True:
            logger.info(
                u'存活列表: {}'.format({n: '==> STILL ALIVE <==' if pool[n]['p'].is_alive() else 'DEAD' for n in pool}))

            all_stopped = True
            for name in pool:
                if pool[name]['p'].is_alive():
                    all_stopped = False
            if all_stopped:
                break
            logger.info(u'仍有crawler未停止... 等待中... ')
            time.sleep(2)

        # logger.info(u'Wait for all the running crawlers...')
        # while True:
        #     for name in pool:
        #         if not pool[name]['stopped']:
        #             logger.info(u'检查爬虫: {}'.format(name))
        #             try:
        #                 r = pool[name]['queue2'].get_nowait()
        #             except Queue.Empty:
        #                 r = None
        #             logger.info(u'检查爬虫{}完毕, 是否已停止: {}'.format(name, r == 'stopped'))
        #             if r and r == 'stopped':
        #                 pool[name]['stopped'] = True
        #                 pool[name]['p'].terminate()
        #                 del pool[name]['queue1']
        #                 del pool[name]['queue2']
        #                 del pool[name]['p']
        #
        #     logger.info(
        #         u'已/未停止列表: {}'.format({n: pool[n]['stopped'] for n in pool}))
        #
        #     all_stopped = True
        #     for name in pool:
        #         if not pool[name]['stopped']:
        #             all_stopped = False
        #     if all_stopped:
        #         break
        #     logger.info(u'仍有crawler未停止... 等待中... ')
        #     time.sleep(2)

        logger.info(u'所有crawler都已停止')

        self.start(False)  # 以重启方式启动的爬虫, 第一次抓取如果有新仍然发送, 以避免漏掉新闻

        self.under_command = False


def set_crawlers_log():
    def setup_logger_single(name):
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s][%(name)s] => %(message)s')

        handler = RotatingFileHandler('logs/crawlers/%s.log' % name, mode='a', maxBytes=5 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(getattr(logging, 'INFO'))
        log.addHandler(handler)

    for single_config in sources.find():
        if single_config.get('machine_name'):
            setup_logger_single(single_config.get('machine_name'))


def main(init_start=False):
    """
    爬虫调度者
    爬虫每次被调度重启时, 会重新识别本地配置文件和在数据库中的配置(代理,间隔等)
    但是注意: 爬虫文件不会, 更新了爬虫文件还是需要重启哦! => "python app.py"
1
    :param init_start: 是否在程序启动时启动所有爬虫, 如果为否, 将等待redis的启动信号
    """
    app = App()

    redis.delete('crawler_signals')
    sub = redis.pubsub()
    sub.subscribe(['crawler_signals'])

    if init_start:
        app.start()
    try:
        while True:
            msg = sub.get_message()
            if msg:
                if msg.get('data') == 'restart':
                    app.restart()

                    set_crawlers_log()

                    redis.publish('crawler_signals_feedback', 'restarted')
                elif msg.get('data') == 'stop':
                    app.stop()
                elif msg.get('data') == 'start':
                    app.start()
                # elif msg.get('data') == 'reload':
                #     app.reload()
            time.sleep(2)
    except KeyboardInterrupt:
        print 'Keyboard exit'


if __name__ == '__main__':
    def setup_logger_global(name, single=False):
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s][%(name)s] => %(message)s')

        if not single:
            filename = 'logs/crawler.log'
        else:
            filename = 'logs/nc_%s.log' % name

        handler = RotatingFileHandler(filename, mode='a', maxBytes=200 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(getattr(logging, 'INFO'))
        log.addHandler(handler)

    set_crawlers_log()

    setup_logger_global('bspider')
    setup_logger_global('App', True)
    setup_logger_global('fetcher')
    setup_logger_global('ResultHandler', True)

    main(init_start=True)
