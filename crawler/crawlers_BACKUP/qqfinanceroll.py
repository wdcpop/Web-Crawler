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


class QQFINANCEROLL(CrawlerAbstract):
    title = u'腾讯财经 - 滚动要闻'
    start_urls = [
        'http://finance.qq.com/gdyw.htm'
    ]
    # url_area_selector = '.main'  # pyquery unable to get this from QQ
    url_patterns = [
        re.compile(r'"(/a/\d{8}/\d{6}.htm)"')
    ]
    content_selector = dict(
        title='.hd h1',
        content='#Cnt-Main-Article-QQ',
        date_area='.hd'
    )

    def get_detail_url_and_title_list(self, response):
        url_details = []
        area_found = re.compile(ur'<!-- 新闻热度排行 -->([\s\S]+?)<!-- \/新闻热度排行 -->').findall(response.text)

        if area_found:
            url_details += re.compile(r'"(/a/\d{8}/\d{6}.htm)"').findall(area_found[0])

        return [dict(url=self.detail_url_hook(i), content='')
                for i in url_details]



