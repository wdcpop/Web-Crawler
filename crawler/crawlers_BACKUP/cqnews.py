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


class CQNEWS(CrawlerAbstract):
    title = u'华龙网 - 重庆要闻'
    start_urls = [
        'http://cq.cqnews.net/html/node_35734.htm',
    ]
    url_links_selector = '.left_news ul li a'
    content_selector = dict(
        title='h1',
        content='.wenziduanluo',
        date_area='.pl'
    )





