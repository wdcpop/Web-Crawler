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


class CHINAISA(CrawlerAbstract):
    """
    这个爬虫和一般爬虫不一样, 由于detail_url每次抓取都部一样, 所以使用了index_page页内的链接标题(<a></a>中的内容)作去重
    """
    def index_page(self, response):
        details = self.get_detail_url_and_title_list(response)

        for detail in details:
            url_origin = detail.get('url')
            url = urljoin(response.url, url_origin)

            # 如果链接标题已抓过, 则跳过
            if detail.get('content') and self.deduplicator.is_url_recorded(detail.get('content')):
                continue

            self.crawl(url,
                       callback='detail_page',
                       anti_duplicate=False,  # 不使用默认的url去重池
                       headers=self.headers,
                       timeout=self.timeout,
                       save={'link_content': detail.get('content')})

    def result_hook(self, res, response):
        # 抓取完成后, 将列表页的链接标题加入去重池
        self.deduplicator.record_url_good(response.save.get('link_content'))
        return res




