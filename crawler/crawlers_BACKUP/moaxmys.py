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


class MOAXMYS(CrawlerAbstract):
    start_urls = [
        'http://www.xmys.moa.gov.cn/xxjc/',
    ]
    url_links_selector = '.cont_r_list ul li:lt(5) a'
    content_selector = dict(
        title='.lefter',
        content='.leftwu1',
        date_area='.leftsan1'
    )




