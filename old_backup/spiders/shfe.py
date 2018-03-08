#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '上期所'


class Shfe(Spider):
    start_urls = [
        'http://www.shfe.com.cn/news/notice/index.html',
    ]
    url_pattern = [
        re.compile(r'(/news/notice/\d+?\.html)')
    ]
    content_pattern = dict(
        title='h1',
        content='.article-detail-text',
        time='.article-date'
    )
