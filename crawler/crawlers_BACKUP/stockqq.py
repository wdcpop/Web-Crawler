#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class STOCKQQ(CrawlerAbstract):
    start_urls = [
        'http://stock.qq.com/l/stock/list20150525114649.htm',
    ]
    url_patterns = [
        re.compile(r'(http://stock\.qq\.com/a/\d{8}/\d+?\.htm)')
    ]
    content_selector = dict(
        title='h1',
        content='p',
        date_area='.pubTime'
    )



