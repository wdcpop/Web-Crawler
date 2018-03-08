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


class CNHUBEI(CrawlerAbstract):
    title = u'荆楚网 - 湖北政务要闻'
    start_urls = [
        'http://news.cnhubei.com/hbzw/yw/',
    ]
    url_links_selector = '.left_content ul li a'
    content_selector = dict(
        title='.left_content > .title',
        content='.content_box',
        date_area='.mintitle'
    )






