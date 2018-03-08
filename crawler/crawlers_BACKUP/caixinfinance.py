#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CAIXINFINANCE(CrawlerAbstract):
    title = u'财新网 - 金融'
    start_urls = [
        'http://finance.caixin.com/news/',
        'http://finance.caixin.com/caixinfinance/',
    ]
    url_area_selector = '.stitXtuwen_list'
    url_patterns = [
        re.compile(r'"(http://finance\.caixin\.com/\d{4}-\d{2}-\d{2}/\d+?.html)"')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['CAIXIN']




