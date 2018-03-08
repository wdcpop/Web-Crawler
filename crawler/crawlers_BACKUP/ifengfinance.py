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


class IFENGFINANCE(CrawlerAbstract):
    title = u'凤凰财经 - 宏观'
    start_urls = [
        'http://finance.ifeng.com/macro/'
    ]
    url_area_selector = '.yib_left'
    url_patterns = [
        re.compile(r'"(http://finance\.ifeng\.com/a/\d{8}/.+?.shtml)"')
    ]
    content_selector = dict(
        title='#artical_topic',
        content='#artical_real',
        date_area='#artical_sth'
    )



