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
    use_link_content_as_detail_title = True
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://m.touziyanapp.com/',
        'Origin': 'http://m.touziyanapp.com',
    }
    start_urls = [
        'http://api.touziyanapp.com/article/newsflash_list/?debug=DhGZvOgqdsgAqhrq2xeKGudCQibu5qx2&page=1',
    ]

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
        return res




