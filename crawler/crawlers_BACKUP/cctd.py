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


class CCTD(CrawlerAbstract):
    start_urls = [
        'http://www.cctd.com.cn/list-10-1.html',
        'http://www.cctd.com.cn/list-106-1.html',
        'http://www.cctd.com.cn/list-42-1.html',
        'http://www.cctd.com.cn/list-22-1.html',
    ]
    url_links_selector = '#new_table tr td li a'
    content_selector = dict(
        title='h1',
        content='#Zoom',
        date_area='.news_tool'
    )





