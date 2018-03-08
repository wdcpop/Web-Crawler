#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CFFEX(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.cffex.com.cn/tzgg/jysgg/',
    ]
    url_patterns = [
        re.compile(r'"javascript\:openWindow\(\'(\./\d{6}/t\d{8}_\d{5}\.html)\'\)"')
    ]
    content_selector = dict(
        content='.cas_content',
        date_area='.cas_content'
    )

