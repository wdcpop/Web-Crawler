#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class JIEMIAN(CrawlerAbstract):
    start_urls = [
        'http://www.jiemian.com/lists/9.html',
        'http://www.jiemian.com/lists/101.html',
        'http://www.jiemian.com/lists/7.html',
        'http://www.jiemian.com/lists/28.html',
        'http://www.jiemian.com/tags/4646/1.html',
        'http://www.jiemian.com/lists/6.html',
    ]
    url_patterns = [
        re.compile(ur'(http://www\.jiemian\.com/article/\d+?\.html)')
    ]
    content_selector = dict(
        title='h1',
        content='.article-content',
        date_area='.date'
    )



