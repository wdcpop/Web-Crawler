#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class JINGJI21(CrawlerAbstract):
    start_urls = [
        'http://m.21jingji.com/channel/capital/',
        'http://m.21jingji.com/channel/business/',
        'http://m.21jingji.com/channel/politics/',
        'http://m.21jingji.com/channel/finance/',
    ]
    url_patterns = [
        re.compile(r'(http://m\.21jingji\.com/article/\d{8}/herald/[\d\w]+?\.html)')
    ]
    content_selector = dict(
        title='h1',
        content='.txtContent',
        date_area='.titleHead'
    )




