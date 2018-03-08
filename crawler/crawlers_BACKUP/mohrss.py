#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MOHRSS(CrawlerAbstract):
    start_urls = [
        'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yiliao/',
    ]
    url_patterns = [
        re.compile(r'(\./\d{6}/t\d{8}_\d+?\.html)')
    ]
    content_selector = dict(
        title='.insMainConTitle_b',
        content='#insMainConTxt',
        date_area='.insMainConTitle_c'
    )




