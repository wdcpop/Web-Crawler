#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class HANGYUNJIE(CrawlerAbstract):
    start_urls = [
        'http://www.ship.sh/info.php',
    ]
    url_patterns = [
        re.compile(r'\./(news_detail\.php\?nid=\d{5,}?)')
    ]
    content_selector = dict(
        title='h1',
        content='.content',
        date_area='.f12_hui'
    )

