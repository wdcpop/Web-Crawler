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
from datetime import datetime


class TOUZIYAN(CrawlerAbstract):
    def get_detail_url_and_title_list(self, response):
        url_details = [dict(
            url='http://api.touziyanapp.com/article/newsflash_data/?debug=DhGZvOgqdsgAqhrq2xeKGudCQibu5qx2&nid={}'.format(
                _.get('nid')),
            content=_.get('title')
        ) for _ in response.json['data']['newsflash']]
        return url_details

    def get_date_area(self, response):
        return datetime.fromtimestamp(
            int(response.json['data']['ctime'])
        ).strftime('%Y-%m-%d %H:%M:%S')


    def result_hook(self, res, response):
        res['link'] = response.json['data']['share_url']
        res['content'] = res['title']
        pattern = re.compile(ur'【(.*?)】')
        match = pattern.match(res['title'])
        if match:
            res['title'] = match.group(1)
        return res



