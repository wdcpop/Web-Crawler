#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CHINATIMES(CrawlerAbstract):
    start_urls = [
        'http://www.chinatimes.cc/finance',
    ]
    url_patterns = [
        re.compile(r'"(/article/\d+?\.html)"')
    ]
    content_selector = dict(
        title='h1',
        content='.infoMain',
        date_area='#pubtime_baidu'
    )



