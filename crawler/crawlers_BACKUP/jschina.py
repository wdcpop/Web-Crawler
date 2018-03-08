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


class JSCHINA(CrawlerAbstract):
    title = u'中国江苏网 - 要闻'
    start_urls = [
        'http://jsnews.jschina.com.cn/jsyw/',
    ]
    url_links_selector = '.NewsList table tr:lt(10) td a'
    content_selector = dict(
        title='#title',
        content='#content',
        date_area='#pubtime_baidu '
    )






