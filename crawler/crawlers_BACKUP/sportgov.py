#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SPORTGOV(CrawlerAbstract):
    start_urls = [
        'http://www.sport.gov.cn/n10503/index.html',
    ]
    url_patterns = [
        re.compile(r'(\.\./n\d+?/c\d+?/content\.html)')
    ]
    content_selector = dict(
        title='.wz_title',
        content='.wz_con',
        date_area='.wz_info'
    )




