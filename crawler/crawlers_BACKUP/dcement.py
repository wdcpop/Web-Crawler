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


class DCEMENT(CrawlerAbstract):
    title = u'数字水泥网 - 市场,行业'
    start_urls = [
        'http://www.dcement.com/Category_49/Index.aspx',
        'http://www.dcement.com/Category_43/Index.aspx',
    ]
    url_links_selector = '.pageList a'

    content_selector = dict(
        title='.articleCon .title',
        content='.conTxt',
        date_area='.property'
    )




