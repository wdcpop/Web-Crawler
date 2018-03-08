#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SZSE(CrawlerAbstract):
    start_urls = [
        'http://www.szse.cn/main/disclosure/bsgg_front/',
        'http://www.szse.cn/main/szhk/ggtywxx/ywtz/',
        'http://www.szse.cn/main/rule/',
    ]
    url_patterns = [
        re.compile(r'(/main/disclosure/bsgg_front/\d+?\.shtml)'),
        re.compile(r'(/main/szhk/ggtywxx/ywtz/\d+?\.shtml)'),
        re.compile(r'(/main/rule/bsywgz/\d+?\.shtml)')

    ]
    content_selector = dict(
        title='.yellow_bt15',
        content='.td10 p',
        date_area='.botborder1',
    )



