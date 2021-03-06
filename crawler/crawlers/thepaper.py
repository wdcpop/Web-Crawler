#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class THEPAPER(CrawlerAbstract):
    def result_hook(self, res, response):
        if not res.get('title'):  # 他们的编辑还没弄好文章, 过会再抓
            res = dict()
            res['acknowledged'] = False

        elif u'专题' in res.get('title'):  # 如果标题里有"专题", 不发送结果并且不再抓
            res = dict()
            res['acknowledged'] = True

        return res



