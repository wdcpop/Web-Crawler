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


class QQROLL(CrawlerAbstract):
    def get_detail_url_and_title_list(self, response):
        html = response.json.get('data', {}).get('article_info', '')
        url_details = re.compile(r'(http://finance.qq.com/a/\d{8}/\d*?\.htm)').findall(html)
        return [dict(url=self.detail_url_hook(i), content='')
                for i in url_details]



