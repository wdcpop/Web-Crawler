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


class ZGKYB(CrawlerAbstract):
    start_urls = [
        'http://www.zgkyb.com/yw/',
    ]
    url_links_selector = '#news #news1 h3 a, #news #newslist1 ul li a'
    content_selector = dict(
        title='.title h2',
        content='.content',
        date_area='.title'
    )




