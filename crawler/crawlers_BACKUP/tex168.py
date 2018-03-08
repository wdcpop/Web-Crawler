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


class TEX168(CrawlerAbstract):
    title = u'中国绸都网 - 纺织快讯'
    start_urls = [
        'http://www.168tex.com/NewsList-0212.html',
    ]
    url_links_selector = '.list_con_li a'
    content_selector = dict(
        title='h1',
        content='#Panel1',
        date_area='.info'
    )






