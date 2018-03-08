#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import json


class SZSE(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://disclosure.szse.cn//disclosure/fulltext/plate/szlatest_24h.js',
    ]

    def get_detail_url_and_title_list(self, response):
        content_found = response.text.strip().split('=[', 1)[1]
        pre_json = '[' + content_found[:-1]
        r = []
        try:
            r = json.loads(pre_json)
        except:
            print 'json err!'
            return []
        return [dict(
            url='http://disclosure.szse.cn/m/' + _[1],
            content=_[2]
        ) for _ in r]




