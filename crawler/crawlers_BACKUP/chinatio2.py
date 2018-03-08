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


class CHINATIO2(CrawlerAbstract):
    title = u'中国钛白粉网'
    start_urls = [
        'http://www.chinatio2.net/News/Infolist.aspx?CategoryID=20',
        'http://www.chinatio2.net/News/Infolist.aspx?CategoryID=28',
    ]
    url_patterns = [
        re.compile(r'"(ShowInfo\.aspx\?ID=\d{5})"')
    ]
    content_selector = dict(
        title='.sub01 > div:eq(1) > em',
        content='.sub01 > div:eq(1)',
        date_area='.title'
    )




