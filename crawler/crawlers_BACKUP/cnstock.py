#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CNSTOCK(CrawlerAbstract):
    start_urls = [
        'http://news.cnstock.com/bwsd/index.html',
    ]
    url_links_selector = '#bw-list li a'

    content_selector = dict(
        title='h1',
        content='.content',
        date_area='.timer'
    )



