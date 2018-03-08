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


class DATIANXIA(CrawlerAbstract):
    title = u'打天下网'
    start_urls = [
        'http://www.datianxia.cc/',
    ]
    url_links_selector = '.post .entry-title a'
    content_selector = dict(
        title='.entry-title',
        content='.entry-content',
        date_area='.entry-meta'
    )


