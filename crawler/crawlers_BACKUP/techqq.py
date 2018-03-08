#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class TECHQQ(CrawlerAbstract):
    start_urls = [
        'http://n.rss.qq.com/rss/tech_rss.php',
    ]
    url_patterns = [
        re.compile(ur'(http://tech\.qq\.com/a/\d+?/\d+?\.htm)')
    ]
    content_selector = dict(
        title='h1',
        content='#Cnt-Main-Article-QQ',
        date_area='.pubTime'
    )



