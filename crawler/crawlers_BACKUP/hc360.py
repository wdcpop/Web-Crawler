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


class HC360(CrawlerAbstract):
    title = u'慧聪化工网'
    start_urls = [
        'http://info.chem.hc360.com/list/zxzx.shtml',
        'http://info.cm.hc360.com/list/list_cm_qushi.shtml',
    ]
    url_links_selector = '.main_left table:first tr td a, #wezi141 table:first tr td a'
    content_selector = dict(
        title='#title h1',
        content='#artical',
        date_area='#endData'
    )



