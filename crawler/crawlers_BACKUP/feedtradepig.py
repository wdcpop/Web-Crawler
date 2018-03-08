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


class FEEDTRADEPIG(CrawlerAbstract):
    start_urls = [
        'http://www.feedtrade.com.cn/livestock/pigsprice/',
    ]
    url_links_selector = u'center > table:eq(3) > tr > td:eq(0) > table:eq(2) > tr > td > table > tr > td > ul:lt(3) > li > a[title*="日报"]'
    content_selector = dict(
        title='h1',
        content='.ReplyContent',
        date_area='center > table:eq(4) > tr > td:eq(0) > table:eq(0) > tr:eq(1)'
    )




