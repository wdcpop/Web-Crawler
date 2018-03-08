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


class CCSTOCKLIANGHUI(CrawlerAbstract):
    start_urls = [
        'http://www.ccstock.cn/finance/lianghui/index.html',
    ]
    url_links_selector = '.listMain ul li a'
    content_selector = {
        'title': 'h1',
        'content': '#newscontent',
        'date_area': '.bt',
    }


