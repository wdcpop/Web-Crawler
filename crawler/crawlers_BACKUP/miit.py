#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MIIT(CrawlerAbstract):
    start_urls = [
        'http://www.miit.gov.cn/n1146290/n1146392/index.html',
        'http://www.miit.gov.cn/n1146290/n1146402/index.html',
        'http://www.miit.gov.cn/n1146290/n4388791/index.html',
        'http://www.miit.gov.cn/n1146285/n1146352/n3054355/n3057585/n3057589/index.html',
        'http://www.miit.gov.cn/n1146295/n1652858/index.html',
    ]
    url_patterns = [
        re.compile(r'href=(.+?/content.html) target')
    ]
    content_selector = dict(
        title='h1',
        content='.ccontent',
        date_area='#con_time'
    )



