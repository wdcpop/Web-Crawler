#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class ETNET(CrawlerAbstract):
    def get_content(self, response):
        if not self.single_config.get('content_selector', {}).get('content'):
            return ''

        doc = response.doc(self.single_config.get('content_selector', {}).get('content'))
        res = doc.html()

        return res
