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


class CSTEEL(CrawlerAbstract):
    start_urls = [
        'http://www.csteelnews.com/xwzx/xydt/'
    ]
    url_links_selector = '.lieb li a'
    content_selector = dict(
        title='.zwcon h1',
        content='.zwcon .zw',
        date_area='.zwcon h2'
    )






