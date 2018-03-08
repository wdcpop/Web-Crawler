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
    title = u'腾讯财经 - 滚动2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Referer': 'http://roll.finance.qq.com/'  # 不填Referer将被拒
    }
    start_urls = [
        'http://roll.finance.qq.com/interface/roll.php?0.3151006646586709&cata=&site=finance&date=&page=1&mode=1&of=json'
    ]
    content_selector = dict(
        title='h1',
        content='#Cnt-Main-Article-QQ',
        date_area='.pubTime, .a_time'
    )

    def get_detail_url_and_title_list(self, response):
        html = response.json.get('data', {}).get('article_info', '')
        url_details = re.compile(r'(http://finance.qq.com/a/\d{8}/\d*?\.htm)').findall(html)
        return [dict(url=self.detail_url_hook(i), content='')
                for i in url_details]



