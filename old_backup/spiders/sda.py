#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '食药监总局'


class Sda(Spider):
    start_urls = [
        'http://www.sda.gov.cn/WS01/CL0051/',
    ]
    url_pattern = [
        re.compile(r'(\.\./CL0051/\d+?\.html)')
    ]
    content_pattern = dict(
        title='.articletitle3',
        content='.articlecontent3',
        time='.articletddate3'
    )
    charset = 'gbk'
