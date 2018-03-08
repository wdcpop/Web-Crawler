#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract


class SHSE(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.sse.com.cn/disclosure/announcement/general/',
    ]
    url_links_selector = '#sse_list_1 a'





