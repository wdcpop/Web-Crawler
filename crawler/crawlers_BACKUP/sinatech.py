#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class XHTECH(CrawlerAbstract):
    title = u'新华网 - 科技播报'
    start_urls = [
        'http://www.news.cn/tech/qqbb.htm'
    ]
    url_patterns = [
        re.compile(r'(http://news\.xinhuanet\.com/tech/\d{4}-\d{2}/\d+?/\S+?\.htm)')
    ]
    content_selector = dict(
        title='#title',
        content='.article',
        date_area='.time'
    )



