#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SASAC(CrawlerAbstract):
    title = u'国资委 - 要闻,通知公告,地方动态'
    start_urls = [
        'http://www.sasac.gov.cn/n85881/n85901/index.html',
        'http://www.sasac.gov.cn/n85881/n85911/index.html',
        'http://www.sasac.gov.cn/n86302/n86376/index.html',
    ]
    url_patterns = [
        re.compile(ur'(\.\./\.\./n\d+?/n\d+?/c\d+?/content\.html)')
    ]
    content_selector = dict(
        title='h1',
        content='.tcon',
        date_area='#con_time'
    )


