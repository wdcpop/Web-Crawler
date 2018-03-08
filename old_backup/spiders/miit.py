#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '工信部'


class Miit(Spider):
    start_urls = [
        'http://www.miit.gov.cn/n1146290/n1146392/index.html',
        'http://www.miit.gov.cn/n1146290/n1146402/index.html',
        'http://www.miit.gov.cn/n1146290/n4388791/index.html'
    ]
    url_pattern = [
        re.compile(r'href=(.+?/content.html) target')
    ]
    content_pattern = dict(
        title='h1',
        content='.ccontent',
        time='#con_time'
    )
