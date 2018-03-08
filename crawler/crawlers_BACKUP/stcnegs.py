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


class STCNEGS(CrawlerAbstract):
    start_urls = [
        'http://egs.stcn.com/index.php?app=wz&mod=News&act=lists',
    ]
    url_links_selector = '.quikly-news-list ul li a.share'
    content_selector = dict(
        title='h1',
        content='.detail',
        date_area='.state'
    )






