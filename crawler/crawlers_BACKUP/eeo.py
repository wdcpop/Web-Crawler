#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class EEO(CrawlerAbstract):
    start_urls = [
        'http://www.eeo.com.cn/politics/',
        'http://www.eeo.com.cn/freelist/jzyw/',
    ]
    url_patterns = [
        re.compile(r"(http://www\.eeo\.com\.cn/\d+?/\d+?/\d+?\.shtml)")
    ]
    content_selector = dict(
        title='.wz_bt',
        content='.wz_zw',
        date_area='#pubtime_baidu'
    )



