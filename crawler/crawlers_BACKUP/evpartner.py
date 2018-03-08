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


class EVPARTNER(CrawlerAbstract):
    title = u'电动汽车资源网 - 最新要闻,政策法规,产销数据'
    start_urls = [
        'http://www.evpartner.com/news/list-1.html',
        'http://www.evpartner.com/news/policy-0-0-0-0-1.html',
        'http://www.evpartner.com/news/list-11-1.html',
    ]
    url_area_selector = '.new-list-noa'
    url_patterns = [
        re.compile(r'"(.*?/news/\d+?/detail-\d+?\.html)"')
    ]
    content_selector = dict(
        title='.article-title',
        content='#newscontent',
        date_area='.article-font'
    )




