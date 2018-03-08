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


class FEEDTRADEMARKET(CrawlerAbstract):
    start_urls = [
        'http://www.feedtrade.com.cn/news/feedmarket/',
    ]
    url_links_selector = '#context ul:eq(0) li a'
    content_selector = dict(
        title='h1',
        content='.ReplyContent',
        date_area='center'
    )




