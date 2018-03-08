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


class GSMN(CrawlerAbstract):
    title = u'广西糖网 - ICE糖评'
    start_urls = [
        'http://author.static.gsmn.cn/1010.EC61DE.html',
    ]
    url_area_selector = '.news_m2 > ul:eq(0)'
    url_patterns = [
        re.compile(r'"(http://author\.static\.gsmn\.cn/\d{6}/\d{2}/.+?.html)"')
    ]
    content_selector = dict(
        title='.new_bt h1',
        content='.news_nr',
        date_area='.new_bt'
    )




