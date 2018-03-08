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


class FGWTZ(CrawlerAbstract):
    start_urls = [
        'http://www.sdpc.gov.cn/zcfb/zcfbtz/',
    ]
    url_links_selector = '.list_02 a '
    content_selector = dict(
        title='.box3 p font',
        content='.txt1 .TRS_Editor ',
        date_area=''
    )




