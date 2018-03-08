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


class CNAL(CrawlerAbstract):
    title = u'中铝网'
    start_urls = [
        'https://news.cnal.com/',
    ]
    url_links_selector = '.cnal-item-new .cnal-tit2 > a'
    content_selector = dict(
        title='h1',
        content='.cnal-details-con',
        date_area='.text-center',
    )






