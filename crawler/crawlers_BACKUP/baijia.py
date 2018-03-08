#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class BAIJIA(CrawlerAbstract):
    start_urls = [
        'http://baijia.baidu.com/?tn=listarticle&labelid=6',
    ]
    url_patterns = [
        re.compile(r'"(http://.+?\.baijia\.baidu\.com/article/\d+?)"')
    ]
    content_selector = dict(
        title='h1',
        content='.article-detail',
        date_area='.time'
    )


