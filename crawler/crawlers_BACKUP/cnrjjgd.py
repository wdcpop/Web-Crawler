#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CNRJJGD(CrawlerAbstract):
    title = u'央广网 - 经济之声'
    start_urls = [
        'http://china.cnr.cn/jjgd/'
    ]
    url_patterns = [
        re.compile(r'(http://www\.cnr\.cn/china/jjgd/\d{8}/t\d{8}_\d+?.shtml)')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CNR']



