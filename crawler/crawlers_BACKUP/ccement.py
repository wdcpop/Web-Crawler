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


class CCEMENT(CrawlerAbstract):
    title = u'中国水泥网'
    start_urls = [
        'http://www.ccement.com/news/list/0-d0-t0.html '
    ]
    url_links_selector = '.list_list ul li:lt(5) a'
    content_selector = dict(
        title='.xl_title',
        content='.text',
        date_area='.sctime'
    )






