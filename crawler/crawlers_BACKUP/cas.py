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


class SAMPLE(CrawlerAbstract):
    title = u'中科院 - 科研进展'
    start_urls = [
        'http://www.cas.cn/syky/'
    ]
    url_patterns = [
        re.compile(r'"(./\d{6}/t\d{8}_\d+?.shtml)"')
    ]
    content_selector = dict(
        title='.cztxxb1y',
        content='#cztxxb1x',
        date_area='.cztxxb1z'
    )
