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


class CQCOAL(CrawlerAbstract):
    title = u'秦皇岛煤炭网 - 煤炭供需,本网快讯'
    start_urls = [
        'http://www.cqcoal.com/',
    ]
    url_patterns = [
        re.compile(r'"(http://news\.cqcoal\.com/a/xinwenzixun/meitanzixun/\d{4}/\d{4}/\d+?\.html)"'),
        re.compile(r'"(http://news\.cqcoal\.com/a/xinwenzixun/benwangkuaixun/\d{4}/\d{4}/\d+?\.html)"')
    ]
    content_selector = dict(
        title='.news_tit',
        content='.text2015',
        date_area='.autor'
    )






