#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class ETNET(CrawlerAbstract):
    start_urls = [
        'http://news.etnet.com.cn/all',
    ]
    url_patterns = [
        re.compile(r"http://news\.etnet\.com\.cn/all-jishixinwen/\d+\.htm")
    ]
    content_selector = dict(
        title='.textheading',
        content='.Newstextall',
        date_area='.functiontuData'
    )

    def get_content(self, response):
        if not self.content_selector.get('content'):
            return ''

        doc = response.doc(self.content_selector.get('content'))
        res = doc.html()

        return res
