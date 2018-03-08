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


class GGII(CrawlerAbstract):
    start_urls = [
        'http://www.gg-ii.com/a/shichangshuju/',
    ]
    url_links_selector = '.insideBlist a'
    content_selector = dict(
        title='.insideM h2',
        content='.insideB',
        date_area='.insideM strong'
    )






