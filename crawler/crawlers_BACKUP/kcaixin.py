#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class KCAIXIN(CrawlerAbstract):
    start_urls = [
        'http://k.caixin.com/web/',
    ]
    url_links_selector = 'dd h2 a'
    content_selector = dict(
        title='title',
        content='.newsCon02',
        date_area='.curm'
    )



