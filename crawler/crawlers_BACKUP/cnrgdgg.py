#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CNRGDGG(CrawlerAbstract):
    title = u'央广网 - 独家快讯'
    start_urls = [
        'http://china.cnr.cn/gdgg/'
    ]
    url_patterns = [
        re.compile(r'(http://www\.cnr\.cn/china/gdgg/\d{8}/t\d{8}_\d+?.shtml)')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CNR']



