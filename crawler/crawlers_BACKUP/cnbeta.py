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


class CNBETA(CrawlerAbstract):
    title = u'cnBeta - 科学探索'
    start_urls = [
        'http://www.cnbeta.com/topics/448.htm'
    ]
    url_area_selector = '.items '
    url_patterns = [
        re.compile(r'"(http://www.cnbeta.com/articles/\d{6,7}\.htm)"')
    ]
    content_selector = dict(
        title='#news_title',
        content='.article_content',
        date_area='.title_bar'
    )





