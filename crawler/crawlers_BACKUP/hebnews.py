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


class HEBNEWS(CrawlerAbstract):
    title = u'河北新闻网 - 时政要闻'
    start_urls = [
        'http://hebei.hebnews.cn/node_103.htm',
    ]
    url_links_selector = '.feed-item a'
    content_selector = dict(
        title='h1',
        content='.text, .contentbox',
        date_area='.source, #pubtime_baidu'
    )






