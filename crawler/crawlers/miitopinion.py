#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import hashlib
import xmltodict
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import dateparser


class MIITOPINION(CrawlerAbstract):
    def detail_url_hook(self, url):
        return re.sub(re.compile(r";jsessionid=.+?\?"), '?', url)


