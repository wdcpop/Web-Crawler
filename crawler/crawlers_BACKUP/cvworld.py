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


class CVWORLD(CrawlerAbstract):
    start_urls = [
        'http://www.cvworld.cn/news/sycnews/guangyao/',
        'http://www.cvworld.cn/news/truck/shuju/',
    ]
    url_links_selector = '.left_con .post a'
    content_selector = dict(
        title='h1',
        content='#NewContent p',
        date_area='.info'
    )






