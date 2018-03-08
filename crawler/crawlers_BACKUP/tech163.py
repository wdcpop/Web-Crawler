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


class TECH163(CrawlerAbstract):
    title = u'网易科技 - 快讯'
    start_urls = [
        'http://tech.163.com/',
    ]
    url_links_selector = '.newest-lists ul li:lt(5) a'
    content_selector = CrawlerAbstract.preset_content_selector['MONEY163']



