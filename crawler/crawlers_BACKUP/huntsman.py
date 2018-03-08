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


class HUNTSMAN(CrawlerAbstract):
    title = u'亨斯迈集团 - 新闻'
    start_urls = [
        'http://www.huntsman.com/corporate/a/Newsroom',
    ]
    url_links_selector = '.contentwrapper:lt(10) .title > a'
    content_selector = dict(
        title='.newstitle',
        content='.newsbody',
        date_area=''
    )






