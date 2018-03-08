#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CNRYGXW(CrawlerAbstract):
    title = u'央广网 - 新闻'
    start_urls = [
        'http://china.cnr.cn/ygxw/'
    ]
    url_patterns = [
        re.compile(r'(http://www\.cnr\.cn/china/ygxw/\d{8}/t\d{8}_\d+?.shtml)')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CNR']



