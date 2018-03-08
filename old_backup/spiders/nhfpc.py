#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '卫计委'


class Nhfpc(Spider):
    start_urls = [
        'http://www.nhfpc.gov.cn/zhuzhan/xwfb/lists.shtml',
    ]
    url_pattern = [
        re.compile(r'(\.\./\.\./.+?\d+?/\w+?/.+?shtml)')
    ]
    content_pattern = dict(
        title='#zoomtitle',
        content='.content',
        time='.content_subtitle'
    )
    charset = 'utf8'
