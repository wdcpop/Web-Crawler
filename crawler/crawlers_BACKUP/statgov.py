#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class STATGOV(CrawlerAbstract):
    start_urls = [
        'http://www.stats.gov.cn/tjsj/zxfb/',
    ]
    url_patterns = [
        re.compile(r'(\./\d{6}/t\d+?_\d+?\.html)')
    ]
    content_selector = dict(
        title='.xilan_tit',
        content='.xilan_con',
        date_area='.xilan_titf',
    )




