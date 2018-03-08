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


class TTTC(CrawlerAbstract):
    start_urls = [
        'http://www.zf826.com/category/365/',
    ]
    url_links_selector = '.entry-header a'
    content_selector = dict(
        title='.site-content h1',
        content='.content-main',
        date_area='.date'
    )



