#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CAIXINCOMPANIES(CrawlerAbstract):
    title = u'财新网 - 公司'
    start_urls = [
        'http://companies.caixin.com/news/',
    ]
    url_area_selector = '.stitXtuwen_list'
    url_patterns = [
        re.compile(r'"(http://companies\.caixin\.com/\d{4}-\d{2}-\d{2}/\d+?.html)"')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CAIXIN']




