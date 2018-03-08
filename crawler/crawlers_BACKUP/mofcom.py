#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MOFCOM(CrawlerAbstract):
    removing_style_and_script = False  # for catching the datestr in script
    start_urls = [
        'http://www.mofcom.gov.cn/article/ae/ai/',
        'http://www.mofcom.gov.cn/article/ae/ag/'
    ]
    url_patterns = [
        re.compile(r'"(/article/ae/\S{2}/\d{6}/\d+?\.shtml)"')
    ]
    content_selector = dict(
        title='#artitle',
        content='.artCon',
        date_area='script'
    )



