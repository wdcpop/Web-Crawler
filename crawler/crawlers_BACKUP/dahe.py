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


class DAHE(CrawlerAbstract):
    title = u'大河网'
    start_urls = [
        'http://news.dahe.cn/sz/',
    ]
    url_links_selector = '#listAll li:lt(10) a'
    content_selector = dict(
        title='h1',
        content='#mainCon',
        date_area='#pubtime_baidu'
    )





