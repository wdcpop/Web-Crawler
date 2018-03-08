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


class QIANLONGBEIJING(CrawlerAbstract):
    title = u'千龙网 - 北京要闻'
    start_urls = [
        'http://beijing.qianlong.com/yaowenjujiao/',
    ]
    url_links_selector = '#mainContent > ul > li:lt(10) > a'
    content_selector = dict(
        title='h1',
        content='#content',
        date_area='.pubDate'
    )






