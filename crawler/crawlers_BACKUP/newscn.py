#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class NEWSCN(CrawlerAbstract):
    start_urls = [
        'http://www.news.cn/fortune/gd.htm',
        'http://www.news.cn/politics/leaders/gdxw.htm',
        'http://www.news.cn/tech/qqbb.htm',
        'http://www.news.cn/local/yw.htm',
        'http://www.xinhuanet.com/politics/24xsyw.htm',
        'http://www.xinhuanet.com/politics/gwycwhy/',
        'http://www.xinhuanet.com/politics/gd.htm',
    ]
    url_links_selector = ''
    url_patterns = [
        re.compile(r'(http://news\.xinhuanet\.com/fortune/\d{4}-\d{2}/\d{2}/c_\d+?\.htm)'),
        re.compile(r'(http://news\.xinhuanet\.com/politics/\d{4}-\d{2}/\d{2}/c_\d+?\.htm)'),
        re.compile(r'(http://news\.xinhuanet\.com/tech/\d{4}-\d{2}/\d{2}/c_\d+?\.htm)')
    ]
    content_selector = dict(
        title='#title, h1, .h-title',
        content='.article, #content, #p-detail',
        date_area='.time, #pubtime, h-info'
    )

