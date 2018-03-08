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


class TRENDFORCE(CrawlerAbstract):
    title = u'集邦科技 - 新闻发布'
    start_urls = [
        'http://press.trendforce.cn/',
    ]
    url_links_selector = '.sideright ul.list > li > a'
    content_selector = dict(
        title='.pre-title',
        content='.content',
        date_area='.con-icon'
    )






