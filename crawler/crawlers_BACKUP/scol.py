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


class SCOL(CrawlerAbstract):
    title = u'四川在线 - 要闻'
    start_urls = [
        'http://sichuan.scol.com.cn/dwzw/',
    ]
    url_patterns = [
        re.compile(r'"(http://sichuan\.scol\.com\.cn/dwzw/\d{6}/\d+?.html)"')
    ]
    content_selector = dict(
        title='#webreal_scol_title',
        content='#scol_txt',
        date_area='#pubtime_baidu'
    )





