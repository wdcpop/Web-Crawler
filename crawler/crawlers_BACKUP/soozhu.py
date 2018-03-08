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


class SOOZHU(CrawlerAbstract):
    title = u'搜猪网 - 生猪价格日评'
    start_urls = [
        'http://www.soozhu.com/c/dianping/riping/',
    ]
    url_patterns = [
        re.compile(r'"(/article/\d{6}/)"')
    ]
    content_selector = dict(
        title='h1',
        content='.article_body',
        date_area='.article_head'
    )




