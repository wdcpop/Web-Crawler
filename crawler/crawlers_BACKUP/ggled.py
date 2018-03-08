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


class GGLED(CrawlerAbstract):
    title = u'高工LED - 资讯'
    start_urls = [
        'http://www.gg-led.com/news.html',
    ]
    url_links_selector = '#ArticleCntwz .news-content:lt(5) a'
    content_selector = dict(
        title='#ArticleTit',
        content='#ArticleCnt_main',
        date_area='.new-suroce'
    )




