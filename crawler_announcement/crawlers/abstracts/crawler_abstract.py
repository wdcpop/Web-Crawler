#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from arrow import Arrow
import logging

from bspider.crawlers.basic_crawler import BasicCrawler
import re
import json
import random
from lxml import etree
import lxml.html
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
from redis import StrictRedis, ConnectionPool

time_formats = [
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2})'),
        '%Y年%m月%d日%H:%M'
    ),
    (
        re.compile(ur'(\d{1,2}月\d{1,2}日\d{2}:\d{2})'),
        '%m月%d日%H:%M'
    ),
    (
        re.compile(ur'(\d{1,2}月\d{1,2}日\s\d{2}:\d{2})'),
        '%m月%d日 %H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}\.\d{1,2}\.\d{1,2}\s\d{2}:\d{2}:\d{2})'),
        '%Y.%m.%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}/\d{1,2}/\d{1,2}\s\d{2}:\d{2})'),
        '%Y/%m/%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2})'),
        '%Y-%m-%d'
    ),
    (
        re.compile(ur'(\d{4}/\d{1,2}/\d{1,2})'),
        '%Y/%m/%d'
    ),
    (
        re.compile(ur'(\d{1,2}/\d{1,2}/\d{4})'),
        '%m/%d/%Y'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}\d{2}\d{2})'),
        '%Y%m%d'
    ),
    (
        re.compile(ur'(\S+\s\d{1,2},\s\d{4})'),
        '%b %d, %Y'
    )

]


def get_one_proxy(proxy_type=1):
    redis = StrictRedis(host='127.0.0.1', port=6379)

    proxy_list = [
        "http://reg:noxqofb0@61.158.163.86:16816",
        "http://reg:noxqofb0@120.24.68.197:16816",
        "http://reg:noxqofb0@112.74.206.133:16816",
        "http://reg:noxqofb0@120.26.167.133:16816",
        "http://reg:noxqofb0@115.28.102.240:16816",
        "http://reg:noxqofb0@27.54.242.222:16816",
        "http://reg:noxqofb0@110.76.185.162:16816",
        "http://reg:noxqofb0@114.215.140.117:16816",
        "http://reg:noxqofb0@122.114.137.18:16816",
        "http://reg:noxqofb0@120.26.160.155:16816"
    ]

    if proxy_type == -1:
        return None

    if proxy_type == 1:
        pass
    elif proxy_type == 2:
        l = redis.get('kuaidaili_foreign_proxy_list')
        proxy_list = json.loads(l)
    elif proxy_type == 3:
        l = redis.get('kuaidaili_foreign_proxy_list')
        proxy_list = json.loads(l)
    elif proxy_type == 10:
        l = redis.get('kuaidaili_proxy_list')
        proxy_list = json.loads(l)
    elif proxy_type == 20:
        l = redis.get('kuaidaili_foreign_proxy_list')
        proxy_list = json.loads(l)
    else:
        pass

    return random.choice(proxy_list)


class CrawlerAbstract(BasicCrawler):
    removing_style_and_script = True
    use_link_content_as_detail_title = False
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}
    timeout = 20

    start_urls = []
    url_links_selector = ''
    url_area_selector = ''
    url_patterns = []
    content_selector = dict()

    preset_content_selector = {
        'CNR': dict(
            title='h2:first',
            content='.articleMain',
            date_area='.source'
        ),
        'MONEY163': dict(
            title='h1, .ep-h1, .con1_ltle',
            content='.post_text',
            date_area='.post_time_source, .ep-time-soure, .con1_date'
        ),
        'PBC': dict(
            title='title',
            content='.content',
            date_area='#shijian'
        ),
        'CAIXIN': dict(
            title='h1',
            content='#Main_Content_Val',
            date_area='#pubtime_baidu'
        )
    }

    def on_start(self):
        self.actual_proxy = get_one_proxy(1)

        print 'self.actual_proxy', self.actual_proxy
        start_urls = self.start_urls_hook(self.start_urls)
        for url in start_urls:
            self.crawl(url, callback='index_page', headers=self.headers, timeout=self.timeout,
                       proxy=self.actual_proxy)

    def index_page(self, response):

        details = self.get_detail_url_and_title_list(response)

        res_list = []
        for d in details:
            if not d.get('url'):
                continue

            if self.deduplicator.is_url_recorded(d.get('url')):
                continue

            res = {
                "acknowledged": True,
                "link": d.get('url'),
                "host": "{0.netloc}".format(urlsplit(response.url)),
                "title": d.get('content'),
                "time_human": '',
                "time": '',
                "ctime": int(time.time()),
                "content": '',
            }

            self.deduplicator.record_url_good(d.get('url'))

            res_list.append(res)

        return res_list


    def start_urls_hook(self, urls):
        return urls

    def detail_url_hook(self, url):
        return url

    def get_detail_url_and_title_list(self, response):
        details = []
        if not self.url_patterns and not self.url_links_selector:
            return []

        if self.url_patterns:
            if self.url_area_selector:
                area_html = response.doc(self.url_area_selector).html()
            else:
                area_html = response.text

            if area_html:
                for url_patt in self.url_patterns:
                    for m in url_patt.finditer(area_html):
                        try:
                            found = m.group(1)
                        except IndexError as e:
                            # 有的正则匹配没有用括号
                            found = m.group(0)
                        right_part_html = area_html[m.start():]
                        content_found_all = re.match(r'.*?>(.*?)</a>', right_part_html)
                        content_found = content_found_all.group(1) if content_found_all else ''

                        details.append(dict(url=self.detail_url_hook(found), content=content_found))

        if self.url_links_selector:
            for link in response.doc(self.url_links_selector).items():
                details.append(dict(url=self.detail_url_hook(link.attr('href')), content=link.text()))

        return details
