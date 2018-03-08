#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class MOF(CrawlerAbstract):
    start_urls = [
        'http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/',
        'http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/',
        'http://szs.mof.gov.cn/zhengwuxinxi/zhengcefabu/',
    ]
    url_area_selector = 'body'
    url_patterns = [
        re.compile(r'(http://.+?\.mof\.gov\.cn/\w+?/\w+?/\d+?/t\d+?_\d+?.html)')
    ]
    content_selector = dict(
        title='.font_biao1',
        content='td > div ',
        date_area=''
    )



