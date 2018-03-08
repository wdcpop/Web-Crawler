#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class CZCE(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.czce.com.cn/portal/jysdt/ggytz/A090601index_1.htm',
    ]
    url_links_selector = '.title:lt(5) a'
    content_selector = dict(
        title='',
        content='',
        date_area=''
    )

