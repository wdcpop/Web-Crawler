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


class OFWEEK(CrawlerAbstract):
    start_urls = [
        'http://display.ofweek.com/CAT-8321303-pannels.html'
    ]
    url_links_selector = '.list_model h3 a'
    content_selector = dict(
        title='H1',
        content='#articleC',
        date_area='.sdate'
    )






