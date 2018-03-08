#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SDA(CrawlerAbstract):
    start_urls = [
        'http://www.sda.gov.cn/WS01/CL0051/',
    ]
    url_patterns = [
        re.compile(r'(\.\./CL0051/\d+?\.html)')
    ]
    content_selector = dict(
        title='.articletitle3',
        content='.articlecontent3',
        date_area='.articletddate3'
    )



