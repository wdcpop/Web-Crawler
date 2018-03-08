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


class MOHURD(CrawlerAbstract):
    title = u'中国住建部 - 政策'
    start_urls = [
        'http://www.mohurd.gov.cn/wjfb/index.html',
    ]
    url_patterns = [
        re.compile(r'"(http://www\.mohurd\.gov\.cn/wjfb/\d{6}/t\d{8}_\d{6}.html)"')
    ]
    content_selector = dict(
        title='.tit',
        content='body > table > tbody > tr:eq(1) > td > table:eq(1)',
        date_area=''
    )





