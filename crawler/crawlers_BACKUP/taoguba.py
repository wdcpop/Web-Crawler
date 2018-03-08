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


class TAOGUBA(CrawlerAbstract):
    title = u'淘财经'
    start_urls = [
        'http://www.taoguba.com/',
    ]
    url_area_selector = '.content'
    url_patterns = [
        re.compile(r'"(http://www\.taoguba\.com/\?p=\d+?)"')
    ]
    content_selector = dict(
        title='h1',
        content='.article-content',
        date_area='.meta'
    )




