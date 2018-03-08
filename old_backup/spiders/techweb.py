#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = 'TechWeb'


class Techweb(Spider):
    charset = 'utf8'
    start_urls = ['http://www.techweb.com.cn/roll/']
    url_pattern = [re.compile(ur'(http://www\.techweb\.com\.cn/.+?/\d{4}-\d{2}-\d{2}/\d+?\.shtml)')]
    content_pattern = dict(
        title='.title',
        content='#artibody',
        time='#pubtime_baidu',
    )
