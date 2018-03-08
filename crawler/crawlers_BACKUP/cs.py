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


class CS(CrawlerAbstract):
    title = u'中证网'
    start_urls = [
        'http://www.cs.com.cn/sylm/jsbd/',
    ]
    url_links_selector = '.subleftbox ul li a'
    content_selector = dict(
        title='h1',
        content='.Dtext',
        date_area='.ctime01',
    )






