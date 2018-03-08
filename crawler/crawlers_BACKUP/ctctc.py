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


class CTCTC(CrawlerAbstract):
    start_urls = [
        'http://www.ctctc.cn/node/351.jspx',
    ]
    url_links_selector = '.list ul li a'
    content_selector = dict(
        title='.article_title',
        content='.article_content',
        date_area='.article_info_l'
    )






