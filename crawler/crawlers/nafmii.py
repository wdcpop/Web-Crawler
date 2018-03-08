#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class NAFMII(CrawlerAbstract):
    def get_date_area(self, response):
        return response.url.rsplit(r'/t', 1)[1][:8].decode('utf-8')
