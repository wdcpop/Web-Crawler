#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class GOVZHENGCE(CrawlerAbstract):
    start_urls = [
        'http://www.gov.cn/zhengce/zuixin.htm',
    ]
    url_patterns = [
        re.compile('(http://www\.gov\.cn/zhengce/content/\d{4}-\d{2}/\d{2}/content_\d+?.htm)'),
    ]
    content_selector = dict(
        title='.bd1 tr:eq(2) td:eq(1)',
        content='.b12c',
        date_area='.bd1 tr:eq(3) td:eq(3)'
    )



