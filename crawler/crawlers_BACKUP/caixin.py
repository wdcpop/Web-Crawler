#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CAIXIN(CrawlerAbstract):
    start_urls = [
        'http://mappv4.caixin.com/channel/list_lastnew_20_1.json',
    ]
    content_selector = dict(
        title='h1',
        content='#Main_Content_Val',
        date_area='#pubtime_baidu'
    )

    def get_detail_url_and_title_list(self, response):
        details = []
        for item in response.json.get('data'):
            url = item.get('web_article_url')
            if url is None:
                url = item.get('web_url')
            if url is None:
                url = item.get('from_web_url')

            for name in ['companies', 'economy', 'finance', 'china', 'international']:
                if name in url:
                    details.append(dict(url=url, content='test'))

        return details

