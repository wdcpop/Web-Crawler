#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SINA(CrawlerAbstract):
    def get_detail_url_and_title_list(self, response):
        details = []
        for item in response.json.get('result').get('data'):
            url = item.get('url') if item.get('url') else item.get('wapurl')
            if not url:
                continue
            details.append(dict(url=url, content=item.get('title', '文章标题解析是失败')))
        return details


