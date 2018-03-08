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


class WWW10S1(CrawlerAbstract):
    start_urls = [
        'http://www.10s1.com/yksbj/hqfx/',
    ]
    url_links_selector = '.list_content_l ul li:lt(5) a'
    content_selector = dict(
        title='h1',
        content='#allow',
        date_area='.content_brief'
    )




