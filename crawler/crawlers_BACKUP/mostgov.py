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


class MOSTGOV(CrawlerAbstract):
    title = u'科技部 - 工作,科技动态'
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.most.gov.cn/kjbgz/',
        'http://www.most.gov.cn/gnwkjdt/',
    ]
    url_area_selector = ''
    url_patterns = [
        re.compile(r'"(\./\d{6}/t\d{8}_\d{6}\.htm)"')
    ]
    content_selector = dict(
        title='',
        content='#Zoom',
        date_area='.gray12'
    )





