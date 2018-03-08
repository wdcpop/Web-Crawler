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


class MONEY163JY(CrawlerAbstract):
    title = u'网易财经 - 交运'
    start_urls = [
        'http://money.163.com/special/002526O5/transport.html',
    ]
    url_area_selector = '.col_l'
    url_patterns = [
        re.compile(r'"(http://money\.163\.com/1\d/\d+?/\d+?/.+?.html)"')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['MONEY163']



