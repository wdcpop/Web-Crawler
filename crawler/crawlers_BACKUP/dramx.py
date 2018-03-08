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


class DRAMX(CrawlerAbstract):
    title = u'集邦科技 - 市场观察'
    start_urls = [
        'http://www.dramx.com/WeeklyResearch/MarketView/',
    ]
    url_links_selector = '.group1_tit a'
    content_selector = dict(
        title='#ctl00_ContentPlaceHolder1_Post_PD h2',
        content='#ctl00_ContentPlaceHolder1_Post_PD > div:eq(2)',
        date_area='#content_info'
    )






