#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class KUAIXUN(CrawlerAbstract):
    start_urls = [
        'http://kuaixun.stcn.com/',
    ]
    url_patterns = [
        re.compile(r'http://kuaixun\.stcn\.com/\d+?/\d+?/\d+?\.shtml')
    ]
    content_selector = dict(
        title='.intal_tit h2',
        date_area='.info'
    )

    def get_content(self, response):
        return response.doc('.txt_con').remove('p:eq(0)').remove('.om').text()



