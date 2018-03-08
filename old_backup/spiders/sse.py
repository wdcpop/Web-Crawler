#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '上交所'


class Sse(Spider):
    start_urls = [
        'http://www.sse.com.cn/disclosure/announcement/general/',
    ]
    url_pattern = [
        re.compile(r'(/disclosure/announcement/general/c/c_\d+?_\d+?\.shtml)')
    ]
    content_pattern = dict(
        title='h2',
        time='.article_opt',
        content='.allZoom',
    )
    charset = 'utf8'
