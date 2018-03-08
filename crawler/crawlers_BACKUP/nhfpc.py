#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class NHFPC(CrawlerAbstract):
    start_urls = [
        'http://www.nhfpc.gov.cn/zhuzhan/xwfb/lists.shtml',
    ]
    url_patterns = [
        re.compile(r'(\.\./\.\./.+?\d+?/\w+?/.+?shtml)')
    ]
    content_selector = dict(
        title='#zoomtitle',
        content='.content',
        date_area='.content_subtitle'
    )



