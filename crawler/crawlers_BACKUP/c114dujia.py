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


class C114DUJIA(CrawlerAbstract):
    start_urls = [
        'http://www.c114.net/news/116.html',
    ]
    url_links_selector = '.li3-2 ul.list1 li a'
    content_selector = dict(
        title='h1',
        content='#text1 p',
        date_area='.r_time'
    )





