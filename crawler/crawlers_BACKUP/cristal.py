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


class CRISTAL(CrawlerAbstract):
    start_urls = [
        'http://www.cristal.com/news-room/Pages/default.aspx',
    ]
    url_links_selector = 'ul.dfwp-list li:lt(5) a:first'
    content_selector = dict(
        title='#main_title',
        content='.article-content',
        date_area='#contactd'
    )




