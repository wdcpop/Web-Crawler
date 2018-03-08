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


class CNCOTTON(CrawlerAbstract):
    start_urls = [
        'http://www.cncotton.com/sy_59/ydxw/',
    ]
    url_links_selector = '.content .listbox a'
    content_selector = dict(
        title='.mtitle',
        content='.content',
        date_area='.mtitlebtm'
    )




