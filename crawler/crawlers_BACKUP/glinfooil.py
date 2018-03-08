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


class GLINFOOIL(CrawlerAbstract):
    start_urls = [
        'http://list.oil.glinfo.com/article/p-460-------------1.html',
    ]
    url_links_selector = '#articleList ul li a'
    content_selector = dict(
        title='h1',
        content='#text',
        date_area='.info'
    )





