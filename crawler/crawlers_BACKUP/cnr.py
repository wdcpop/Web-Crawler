#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CNR(CrawlerAbstract):
    start_urls = [
        'http://roll.cnr.cn/finance/',
    ]
    url_patterns = [
        re.compile(r'(http://www\.cnr\.cn/list/finance/\d{8}/t\d{8}_\d+?\.shtml)'),
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CNR']



