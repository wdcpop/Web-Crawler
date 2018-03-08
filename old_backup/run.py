#!/usr/bin/env python
# coding:utf8

from gevent import monkey

monkey.patch_all()
import gevent

import sys
import json
from random import choice

# reload(sys)
# sys.setdefaultencoding('utf8')
import traceback
from spider import Spider
from spiders import spider_class_dict
from time import sleep, time

from pymongo import MongoClient
# from spiders.wscn import Wscn
# from spiders.mohrss import Mohrss
# from spiders.eeo import Eeo
# #from spiders.baijia import Baijia
# from spiders.miit import Miit
# from spiders.mof import Mof
# from spiders.mofcom import Mofcom
# from spiders.p5w import P5w
# # from spiders.pbc import Pbc
# from spiders.yicai import Yicai
# from spiders.aastocks import Aastocks
# from spiders.reuters import Reuters
# from spiders.ndrc import Ndrc
# from spiders.csrc import Csrc
# from spiders.sina import Sina
# from spiders.kcaixin import Kcaixin
# from spiders.caixin import Caixin
# from spiders.jinji21 import Jingji21
# from spiders.newscn import Newscn
# from spiders.kuaixun import Kuaixun
# from spiders.stockqq import Stockqq
# from spiders.govnews import Govnews
# from spiders.money163 import Money163
# from spiders.chinanews import Chinanews
# from spiders.chinatimes import Chinatimes
# from spiders.hangyunjie import Hangyunjie
# from spiders.govzhengce import Govzhengce
# from spiders.cnstock import Cnstock
# from spiders.thepaper import ThePaper
# from spiders.jiemian import Jiemian
# from spiders.safegov import SafeGov
# from spiders.sasac import Sasac
# from spiders.techweb import Techweb
# from spiders.techqq import Techqq
# from spiders.techsina import Techsina
# from spiders.mfa import Mfa
# from spiders.sda import Sda
# from spiders.nhfpc import Nhfpc
# from spiders.sportgov import Sportgov
# from spiders.statgov import Statgov
# from spiders.szse import Szse
# from spiders.sse import Sse
# from spiders.dce import Dce
# from spiders.czce import Czce
# from spiders.shfe import Shfe
# from spiders.cffex import Cffex
# from spiders.etnet import EtNet
# from spiders.hket import Hket

from logging import getLogger
from coloredlogs import install
from redis import StrictRedis, ConnectionPool
from arrow import Arrow

redis = StrictRedis(connection_pool=ConnectionPool())
db = MongoClient()
news = db['content']['items']
sources = db['content']['sources']
source_default_configs = db['content']['sourceDefaultConfigs']
log = getLogger(__name__)
install(10, logger=log)
log.setLevel(10)



def spider_loop(proxy_type, sleeptime, spider):
    spider_name = spider.source_name
    # if 'test' not in sys.argv or proxy_type == 2:
    spider.set_proxy(proxy_type)
    spider.clear()
    time_start = time()
    try:
        spider.run()
    except Exception:
        log.warn(u'{0: <30}{1}'.format(spider_name, traceback.format_exc().decode('utf8')))
    time_crawl = 0

    if 'test' in sys.argv:
        if spider.result:
            time_crawl = Arrow.fromtimestamp(choice(spider.result)['time']).to('Asia/Shanghai').format()
            print json.dumps(spider.result[0], ensure_ascii=False, indent=4, encoding='utf8').encode('utf8')

    total_time = time() - time_start
    log.debug(
        u'链接个数:{:<3}-解析个数:{}-解析时间:{}-耗时{:.2f}秒-{}'.format(spider.test_count, len(spider.result), time_crawl, total_time,
                                                          spider_name))
    crawled = dict(
        name=spider_name,
        result_count=len(spider.result),
        crawl_count=spider.test_count,
        totalTime=total_time
    )
    redis.publish('crawled', json.dumps(crawled))
    if 'test' in sys.argv:
        return
    if len(spider.result) > 0:
        log.warning(u'{0: <30}更新:{1}'.format(spider_name, len(spider.result)))
        result = spider.result
        for i in result:
            upserted = news.update({'link': i['link']}, i, True)  # type:dict
            spider.blf.insert(i['link'])
            log.info(upserted)
            if upserted:
                try:
                    redis.publish('news_updated', str(upserted['upserted']))
                except:
                    pass
    sleep(sleeptime)


def crawl(spider_class, delay_time, proxy_type, source_title='unknown'):
    """
    :param spider_class:   爬虫类
    :param sleeptime: 休息时间 秒为单位
    :param proxy_type: 1为国内(代码内) 2为国外(代码内) -1为不使用 5为储存在数据库内的代理地址表
    """
    delay_time = int(delay_time) if delay_time else 2
    proxy_type = int(proxy_type) if proxy_type else 1

    log.info(u'{0} 开启'.format(repr(spider_class).decode('utf8')))
    spider = spider_class()  # type:Spider
    spider.set_source_title(source_title)
    spider.setlogger(log)
    while True:
        let = gevent.spawn(spider_loop, proxy_type, delay_time, spider)
        gevent.wait([let], 120)
        if not let.dead: let.kill(block=True, timeout=20)
        spider.clear()
        spider.test_count = 0
        if 'test' in sys.argv:
            break


def sync_sources_names_to_db():
    for (i, source_name) in enumerate(spider_class_dict):
        sources.update({'machine_name': source_name}, {
            '$set': {
                'machine_name': source_name,
                'title': spider_class_dict[source_name].__module__
            }
        }, True)  # type:dict


def main():
    if 'init_sync' in sys.argv:
        sync_sources_names_to_db()
        return

    spider_configs = {row.get('machine_name'): row
                      for row in sources.find() if row.get('machine_name') and not row.get('disabled')}
    spider_default_configs = source_default_configs.find_one()
    default_delay = spider_default_configs['default_delay']
    # -1: No proxy / 1: kuaidaili proxy / 2: overseas proxy/ 5: proxy list in db
    default_proxy_type = spider_default_configs['default_proxy']

    lets = []
    spider_list = [spider_name for spider_name in spider_class_dict]
    if 'test' in sys.argv and len(sys.argv) == 3:
        spider_list = filter(lambda _: sys.argv[2].upper() == _.upper(), spider_list)

    # 将数据库内的所有爬虫名单遍历
    for spider_name in spider_configs:

        # 如果数据库内的爬虫名称不在文件列表内, 跳过
        if spider_name not in spider_list:
            continue

        lets.append(gevent.spawn(
            crawl,
            spider_class_dict[spider_name],
            spider_configs[spider_name]['delay_sec'] if spider_configs[spider_name].get('delay_sec') else default_delay,
            spider_configs[spider_name]['proxy_type'] if spider_configs[spider_name].get('proxy_type') else default_proxy_type,
            spider_configs[spider_name]['title']
        ))
    gevent.joinall(lets)


if __name__ == '__main__':
    main()
