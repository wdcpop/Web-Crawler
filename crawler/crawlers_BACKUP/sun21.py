#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import hashlib
import xmltodict
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import dateparser


class SUN21(CrawlerAbstract):
    title = u'中国工程机械商贸网'
    start_urls = [
        'http://news.21-sun.com/list/guandian_3_1.htm',
    ]
    url_area_selector = '#newslist'
    url_patterns = [
        re.compile(r'"(http://news\.21-sun\.com/detail/\d{4}/\d{2}/\d+?\.shtml)"')
    ]
    content_selector = dict(
        title='.contTitle',
        content='.content',
        date_area='.contTip'
    )





