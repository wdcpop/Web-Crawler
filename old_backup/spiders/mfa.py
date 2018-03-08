#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import re
from spider import Spider

__name__ = '外交部'


class Mfa(Spider):
    start_urls = [
        'http://www.mfa.gov.cn/web/zyxw/',
    ]
    url_pattern = [
        re.compile(r'(\./t\d+?\.shtml)')
    ]
    content_pattern = dict(
        title='.title',
        content='.content',
        time='#News_Body_Time'
    )
