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


class IBUYCHEM(CrawlerAbstract):
    start_urls = [
        'http://www.ibuychem.com/news/info/list/page.html?_ti=1481734197536'
    ]
    url_links_selector = '.zx_con dd h2 a'
    content_selector = dict(
        title='.zx_left h2',
        content='.zx_left',
        date_area='.zx_left .time'
    )






