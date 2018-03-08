#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '体育总局'


class Sportgov(Spider):
    start_urls = [
        'http://www.sport.gov.cn/n10503/index.html',
    ]
    url_pattern = [
        re.compile(r'(\.\./n\d+?/c\d+?/content\.html)')
    ]
    content_pattern = dict(
        title='.wz_title',
        time='.wz_info',
        content='.wz_con',
    )
    charset = 'utf8'
