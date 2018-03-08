#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MFA(CrawlerAbstract):
    start_urls = [
        'http://www.mfa.gov.cn/web/zyxw/',
    ]
    url_patterns = [
        re.compile(r'(\./t\d+?\.shtml)')
    ]
    content_selector = dict(
        title='#News_Body_Title',
        content='.content',
        date_area='#News_Body_Time'
    )



