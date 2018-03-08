#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SHFE(CrawlerAbstract):
    start_urls = [
        'http://www.shfe.com.cn/news/notice/index.html',
    ]
    url_patterns = [
        re.compile(r'(/news/notice/\d+?\.html)')
    ]
    content_selector = dict(
        title='h1',
        content='.article-detail-text',
        date_area='.article-date'
    )





