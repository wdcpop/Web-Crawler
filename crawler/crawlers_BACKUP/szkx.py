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


class SZKX(CrawlerAbstract):
    start_urls = [
        'http://company.cnstock.com/company/scp_gsxw/',
    ]
    url_links_selector = '.main-list .new-list li a'
    content_selector = dict(
        title='.main-content .title',
        content='.main-content .content',
        date_area='.timer'
    )



