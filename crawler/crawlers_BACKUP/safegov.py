#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SAFEGOV(CrawlerAbstract):
    start_urls = [
        'http://www.safe.gov.cn/wps/portal/sy/news_ywfb'
    ]
    url_patterns = [
        re.compile(ur'align="left" ><a href="(/wps/portal/!ut/p/.+?)" target="_blank')
    ]
    content_selector = dict(
        title='strong',
        content='#newsContent',
    )

    def get_date_area(self, response):
        return re.compile(ur'<B>发布日期:</B>\s+?<span>(.+?)</span>').findall(response.text)[0]



