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


class QQFINANCEPRISM(CrawlerAbstract):
    title = u'腾讯财经 - 棱镜'
    start_urls = [
        'http://finance.qq.com/prism.htm'
    ]
    url_patterns = [
        re.compile(r'"(/original/lenjing/.+?\.html)"')
    ]
    content_selector = dict(
        content='#articleContent',
        date_area='.pageNum'
    )

    def get_title(self, response):
        return response.doc('.bd h1').remove('span').text()



