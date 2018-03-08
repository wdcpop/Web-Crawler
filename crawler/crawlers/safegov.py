#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SAFEGOV(CrawlerAbstract):
    def get_date_area(self, response):
        return re.compile(ur'<B>发布日期:</B>\s+?<span>(.+?)</span>').findall(response.text)[0]



