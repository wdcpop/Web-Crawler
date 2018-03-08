#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import hashlib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SMM(CrawlerAbstract):
    title = u'上海有色网 - 滚动'
    start_urls = [
        'http://news.smm.cn/live?category=al',
    ]

    def index_page(self, response):
        rs = []
        for i in response.doc('.live .live_body').items():
            daystr = i.attr('data_date_attr')

            for j in i('.live_list li').items():

                title = j('p').text()
                random_str_from_title = hashlib.md5(title.encode('utf-8')).hexdigest()
                fakeurl = "{}#{}".format(response.url, random_str_from_title)

                findall = re.compile(ur'(\d{2}:\d{2})').findall(j('.live_body_time').text())
                date = {}
                if findall:
                    full_date_str = '{} {}'.format(daystr, findall[0])
                    date = self.get_datestr_and_dateint(full_date_str)

                if self.deduplicator.is_url_recorded(fakeurl):
                    continue

                rs.append({
                    "acknowledged": True,
                    "other_acknowledged_urls": [fakeurl],
                    "shall_be_sent": True,
                    "link": fakeurl,
                    "host": "{0.netloc}".format(urlsplit(response.url)),
                    "title": title,
                    "time_human": date.get('dateint'),
                    "time": date.get('datestr'),
                    "ctime": int(time.time()),
                    "content": '无'
                })
        return rs



