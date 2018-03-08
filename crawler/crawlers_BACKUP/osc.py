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


class OSC(CrawlerAbstract):
    title = u'秦皇岛煤炭网 - 环煤价格指数周评'
    start_urls = [
        'http://www.osc.org.cn/ListInfo.jsp?id=V02'
    ]
    url_patterns = [
        re.compile(r'"(/news/V02/\d{5}_\d{1}\.html)"')
    ]
    content_selector = dict(
        title='.tit h2',
        content='.cont_text',
        date_area='.tit2'
    )



