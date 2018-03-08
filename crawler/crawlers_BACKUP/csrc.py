#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CSRC(CrawlerAbstract):
    start_urls = [
        'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/',
    ]
    url_patterns = [
        re.compile(r"(./\d+?/t\d+?_\d+?\.html)")
    ]
    content_selector = dict(
        title='title',
        content='.Custom_UnionStyle',
        date_area='.time'
    )



