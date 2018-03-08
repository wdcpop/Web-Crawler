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


class YNSUGAR(CrawlerAbstract):
    start_urls = [
        'http://www.ynsugar.com/Article/hot/Index.html'
    ]
    url_links_selector = '.hui_bk table:eq(5) td > a'
    content_selector = dict(
        title='.hui_bk table:eq(1)',
        content='.hui_bk table:eq(5)',
        date_area='.hui_bk table:eq(3)'
    )






