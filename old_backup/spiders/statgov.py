#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '统计局'


class Statgov(Spider):
    start_urls = [
        'http://www.stats.gov.cn/tjsj/zxfb/',
    ]
    url_pattern = [
        re.compile(r'(\./\d{6}/t\d+?_\d+?\.html)')
    ]
    content_pattern = dict(
        title='.xilan_tit',
        time='.xilan_titf',
        content='.xilan_con',
    )
    charset = 'utf8'
