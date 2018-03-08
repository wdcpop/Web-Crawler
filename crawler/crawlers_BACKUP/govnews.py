#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class GOVNEWS(CrawlerAbstract):
    start_urls = [
        'http://www.gov.cn/xinwen/gundong.htm',
        'http://www.gov.cn/xinwen/yaowen.htm',
    ]
    url_patterns = [
        re.compile(r'(/xinwen/\d{4}-\d{2}/\d{2}/content_\d+?\.htm)')
    ]
    content_selector = dict(
        title='.article h1, .pages-title',
        content='.pages_content',
        date_area='.pages-date'
    )




