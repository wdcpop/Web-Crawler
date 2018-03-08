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


class SCI99(CrawlerAbstract):
    title = u'卓创资讯 - 行业新闻'
    start_urls = [
        'http://www.sci99.com/news-772.html',
    ]
    url_area_selector = '.ul_w682'
    url_patterns = [
        re.compile(r'(/news/\d{8}\.html)')
    ]
    content_selector = dict(
        title='.news_title',
        content='#panel_news',
        date_area='.news_share'
    )





