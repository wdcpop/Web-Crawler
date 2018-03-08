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

__name__ = '人社部'


class Mohrss(Spider):
    start_urls = [
        'http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yiliao/',
    ]
    url_pattern = [
        re.compile(r'(\./\d{6}/t\d{8}_\d+?\.html)')
    ]
    content_pattern = dict(
        title='.insMainConTitle_b',
        content='#insMainConTxt',
        time='.insMainConTitle_c'
    )
