#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MONEY163(CrawlerAbstract):
    start_urls = [
        'http://money.163.com/special/00251G8F/news_json.js',
    ]
    url_patterns = [
        re.compile(r'"(http://money\.163\.com/1\d/\d+?/\d+?/.+?.html)"')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['MONEY163']



