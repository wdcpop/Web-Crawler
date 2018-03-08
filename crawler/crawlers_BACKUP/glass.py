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


class GLASS(CrawlerAbstract):
    start_urls = [
        'http://www.glass.com.cn/glassnews/kind_33_page_1',
    ]
    url_links_selector = 'ul.news_list:lt(2) li a'
    content_selector = dict(
        title='h1',
        content='.newsinfo_cont',
        date_area='.detail',
    )






