#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class WSCN(CrawlerAbstract):
    start_urls = [
        'https://api.wallstreetcn.com/v2/posts',
    ]
    content_selector = dict(
        title='.title-text',
        date_area='.title-meta-time'
    )

    def get_detail_url_and_title_list(self, response):
        url_pattern = re.compile(ur'(https?://wallstreetcn.com/node/\d+?)')
        url_details = [_.get('url') for _ in response.json['results']]
        url_details = filter(lambda x: url_pattern.match(x), url_details)
        return [dict(url=self.detail_url_hook(i), content='')
                for i in url_details]

    def get_content(self, response):
        return response.doc('.page-article-content').remove('p:last, img:last').text()



