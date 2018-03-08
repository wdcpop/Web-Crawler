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


class EASTMONEY(CrawlerAbstract):
    title = u'东方财富'
    start_urls = [
        'http://finance.eastmoney.com/news/cywjh.html'
    ]
    url_links_selector = '.repeatList ul li .text a'
    content_selector = dict(
        title='h1',
        content='#ContentBody',
        date_area='.time'
    )






