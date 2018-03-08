#!/usr/bin/env python
# coding:utf8
import os
import logging
import re
import sys
from urlparse import urljoin

from arrow import Arrow
import urllib
from pyquery import PyQuery
import requests
from settings import PROXIES, FOREIGN_PROXIE
from random import choice
from redis import StrictRedis, ConnectionPool
from bloomfilter import BloomFilter
from user_agent import generate_user_agent

import inspect


class Spider(object):
    url_pattern = []
    start_urls = []
    content_pattern = {}
    charset = 'utf8'

    def __init__(self):
        self.log = None  # type:logging.Logger
        self.pq = PyQuery
        self.test_count = 0
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': generate_user_agent(platform='win', navigator='chrome')})
        self.s.headers.update({'CacheControl': 'no-cache'})
        self.s.headers.update({'Pragma': 'no-cache'})
        self.s.headers.update({'Expires': '-1'})
        self._result = []
        self.redis = StrictRedis(connection_pool=ConnectionPool())
        self.blf = BloomFilter(self.redis)
        self.source_name = self.__class__.__name__.upper()
        self.source_title = 'unknown'

    def set_proxy(self, ptype):
        """
        :type ptype:int
        """
        if ptype:
            if ptype == 1:
                proxy_choosed = choice(PROXIES)
                self.s.proxies.update({"http": proxy_choosed, "https": proxy_choosed})
            elif ptype == 2:
                self.s.proxies.update({
                    'http': FOREIGN_PROXIE,
                    'https': FOREIGN_PROXIE
                })
            else:
                pass

    def set_source_title(self, source_title):
        self.source_title = source_title

    def run(self):
        url_details = self.get_urls()
        map(self.parse, url_details)
        return self.result

    def result_hook(self, res):
        return True

    def get_safe_html(self, query):
        return query.text()

    def parse(self, url):

        if self.check_bloomfilter(url): return

        r_detail = self.s.get(url)
        r_detail.encoding = self.charset
        p = self.pq(r_detail.text)

        article_attrs = {}
        for key, value in self.content_pattern.iteritems():
            if isinstance(value, str) or isinstance(value, unicode):
                article_attrs[key] = p(value).remove('style').remove('script').text()
            elif isinstance(value, re.compile('')):
                article_attrs[key] = value.match(r_detail.text).group(1)
        res = dict(
            name=self.source_title,
            link=url,
            **article_attrs
        )
        res['raw'] = r_detail.text
        if not self.result_hook(res):
            return
        res.pop('raw')
        self.addresult(**res)

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
            re.compile(ur'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})'),
            '%Y-%m-%d %H:%M:%S'
        ),
        (
            re.compile(ur'(\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}:\d{2})'),
            '%Y.%m.%d %H:%M:%S'
        ),
        (
            re.compile(ur'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})'),
            '%Y-%m-%d %H:%M'
        ),
        (
            re.compile(ur'(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})'),
            '%Y/%m/%d %H:%M'
        ),
        (
            re.compile(ur'(\d{4}-\d{1,2}-\d{1,2})'),
            '%Y-%m-%d'
        ),
        (
            re.compile(ur'(\d{4}/\d{2}/\d{2})'),
            '%Y/%m/%d'
        ),
        (
            re.compile(ur'(\d{4}年\d{2}月\d{2}日)'),
            '%Y年%m月%d日'
        ),
        (
            re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
            '%Y年%m月%d日'
        ),
        (
            re.compile(ur'(\d{4}\d{2}\d{2})'),
            '%Y%m%d'
        )

    ]

    def parse_time(self, ctime):
        if isinstance(ctime, unicode) or isinstance(ctime, str):
            for time_re, arrow_fmt in self.time_formats:
                findall = time_re.findall(ctime)
                if findall:
                    ret = Arrow.strptime(findall[0].encode('utf8'), arrow_fmt, 'Asia/Shanghai')
                    return ret.timestamp
            return 0
        else:
            return ctime

    def addresult(self, name, title, content, link, time=0):
        res = {'name': self.source_title, 'title': title, 'content': content, 'link': link,
               'host': self.extract_hostname(link),
               'ctime': Arrow.utcnow().timestamp, 'time': self.parse_time(time), 'source': self.source_name}

        if len(title) == 0:
            raise ValueError('标题为空{}'.format(link))
        if len(content) == 0:
            raise ValueError('内容为空{}'.format(link))

        self.result.append(res)

    def check_bloomfilter(self, url):
        self.test_count += 1
        if self.test_count > 10:
            if 'test' in sys.argv: return True
        else:
            if 'test' in sys.argv: return False
        if self.blf.exsits(url, 'bloomfilter_url'):
            return True
        else:
            self.log.info('crawl:{0}'.format(url))
            return False

    def get_urls(self):
        url_details = []
        for url in self.start_urls:
            r = self.s.get(url)
            for url_patt in self.url_pattern:
                url_details += [urljoin(url, _) for _ in url_patt.findall(r.text)]
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(self.__class__))
        return url_details

    @property
    def result(self):
        return self._result

    def clear(self):
        self._result = []

    @staticmethod
    def extract_hostname(url):
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        return host

    def setlogger(self, logger):
        self.log = logger
