#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '中金所'


class Cffex(Spider):
    start_urls = [
        'http://www.cffex.com.cn/tzgg/jysgg/',
    ]
    url_pattern = [
        re.compile(r"javascript:openWindow\('(./\d{6}/t\d{8}_\d+?\.html)'\)")
    ]
    content_pattern = dict(
        title='body center>table table:eq(0) table:eq(0) table:eq(0) table:eq(0) table table',
        content='body center>table table:eq(0) table:eq(0) table:eq(0) table:eq(0) table .cas_content',
        time='body center>table table:eq(0) table:eq(0) table:eq(0) table:eq(0) table .cas_content'
    )
