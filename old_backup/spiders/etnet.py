#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '经济通'

class EtNet(Spider):
    start_urls = [
        'http://news.etnet.com.cn/all',
    ]
    url_pattern = [
        re.compile(r"http://news.etnet.com.cn/all-jishixinwen/\d+\.htm")
    ]
    content_pattern = dict(
        title='.textheading',
        content='.Newstextall',
        time='.functiontuData'
    )





