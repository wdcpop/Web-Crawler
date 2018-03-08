#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import xmltodict
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class PRNASIA(CrawlerAbstract):
    def get_detail_url_and_title_list(self, response):
        item = xmltodict.parse(response.text)['rss']['channel']['item']
        url_details = map(lambda x: x['link'], item)
        url_details = {}.fromkeys(url_details).keys()
        return [dict(url=self.detail_url_hook(i), content='')
                for i in url_details]

