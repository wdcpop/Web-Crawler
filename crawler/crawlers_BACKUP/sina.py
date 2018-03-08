#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SINA(CrawlerAbstract):
    start_urls = [
        'http://roll.finance.sina.com.cn/finance/gncj/hgjj/index.shtml'
    ]
    url_patterns = [
        re.compile(r'(http://finance\.sina\.com\.cn/[\w/]+?/\d{4}-\d{2}-\d{2}/doc-\w+?\.shtml)')
    ]
    content_selector = dict(
        title='#artibodyTitle',
        content='.article, #artibody',
        date_area='.time-source, #pub_date'
    )



