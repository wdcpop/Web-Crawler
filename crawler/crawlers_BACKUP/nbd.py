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


class NBD(CrawlerAbstract):
    title = u'每日经济新闻'
    start_urls = [
        'http://www.nbd.com.cn/columns/3',
    ]
    url_links_selector = 'ul.u-news-list li a'
    content_selector = dict(
        title='h1',
        content='.g-articl-text',
        date_area='.u-time'
    )






