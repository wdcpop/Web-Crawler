#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SSE(CrawlerAbstract):
    start_urls = [
        'http://www.sse.com.cn/disclosure/announcement/general/',
    ]
    url_patterns = [
        re.compile(r'(/disclosure/announcement/general/c/c_\d+?_\d+?\.shtml)')
    ]
    content_selector = dict(
        title='h2',
        content='.allZoom',
        date_area='.article_opt',
    )



