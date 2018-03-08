#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CHINANEWS(CrawlerAbstract):
    start_urls = [
        'http://www.chinanews.com/cj/gd.shtml',
    ]
    url_links_selector = '.content_list li a'
    content_selector = dict(
        title='title',
        content='.left_zw',
        date_area='.left-t, .Submit_time'
    )




