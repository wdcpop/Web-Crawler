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


class SEMI(CrawlerAbstract):
    title = u'semi大半导体产业网 - 北美半导体订单晴雨表'
    start_urls = [
        'http://www.semi.org.cn/news/rain_list.aspx',
    ]
    url_patterns = [
        re.compile(r'(rain_show\.aspx\?ID=\d{3,4})')
    ]
    content_selector = dict(
        title='#lblTitle',
        content='.contenttext',
        date_area='#lblTime'
    )




