#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import hashlib
import xmltodict
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import dateparser


class BJNEWS(CrawlerAbstract):
    title = u'新京报财经 - 行业资讯'
    start_urls = [
        'http://www.bjnews.com.cn/finance/'
    ]
    url_patterns = [
        re.compile(r'"(http://www\.bjnews\.com\.cn/finance/\d{4}/\d{2}/\d{2}/\d{6}\.html)"')
    ]
    content_selector = dict(
        title='h1',
        content='.content',
        date_area='.ntit'
    )





