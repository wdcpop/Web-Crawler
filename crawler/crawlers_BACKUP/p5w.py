#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class P5W(CrawlerAbstract):
    start_urls = [
        'http://www.p5w.net/kuaixun/tj/',
    ]
    url_links_selector = '.manlist3 li a:first'
    content_selector = dict(
        title='h1',
        content='.article_content2',
        date_area='time'
    )



