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


class EASTDAY(CrawlerAbstract):
    title = u'东方网 - 上海政务'
    start_urls = [
        'http://news.eastday.com/gd2008/shzw/index.html',
    ]
    url_links_selector = '.leftsection ul li a'
    content_selector = dict(
        title='h1',
        content='#zw2',
        date_area='.timer '
    )






