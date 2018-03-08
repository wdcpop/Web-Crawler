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


class C114ROLL(CrawlerAbstract):
    start_urls = [
        'http://www.c114.net/news/roll.asp?y={{y}}&m={{m}}&d={{d}}&o=true',
    ]
    url_links_selector = '.ro1-2 ul.ro2 li a'
    content_selector = dict(
        title='h1',
        content='#text1 p',
        date_area='.r_time'
    )

    def start_urls_hook(self, urls):
        new_urls = []
        for url in urls:
            if '{{y}}' in url:
                now = Arrow.utcnow().to('Asia/Shanghai')
                url = url.replace(
                    '{{y}}', now.format('YY')).replace(
                    '{{m}}', now.format('MM')).replace(
                    '{{d}}', now.format('DD'))
            new_urls.append(url)
        return new_urls






