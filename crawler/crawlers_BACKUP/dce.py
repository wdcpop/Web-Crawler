#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class DCE(CrawlerAbstract):
    start_urls = [
        'http://www.dce.com.cn/dalianshangpin/yw/fw/jystz/ywtz/index.html',
    ]
    url_patterns = [
        re.compile(r"(/dalianshangpin/yw/fw/jystz/ywtz/\d+?/index.html)")
    ]
    content_selector = dict(
        title='.tit_header h2',
        content='.detail_content',
        date_area='.noice_date'
    )



