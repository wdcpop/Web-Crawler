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


class GMWTECH(CrawlerAbstract):
    title = u'光明网 - 科技滚动'
    start_urls = [
        'http://tech.gmw.cn/newspaper/index.htm',
    ]
    url_area_selector = '#news_list'
    url_patterns = [
        re.compile(r'"(http://tech\.gmw\.cn/newspaper/\d{4}-\d{2}/\d{2}/content_\d+?.htm)"')
    ]
    content_selector = dict(
        title='h1',
        content='#contentMain',
        date_area='#contentMsg'
    )





