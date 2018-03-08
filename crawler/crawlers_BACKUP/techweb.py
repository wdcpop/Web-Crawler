#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class TECHWEB(CrawlerAbstract):
    start_urls = [
        'http://www.techweb.com.cn/roll/',
    ]
    url_patterns = [
        re.compile(ur'(http://www\.techweb\.com\.cn/.+?/\d{4}-\d{2}-\d{2}/\d+?\.shtml)')
    ]
    content_selector = dict(
        title='.title > h1',
        content='#artibody',
        date_area='#pubtime_baidu'
    )





