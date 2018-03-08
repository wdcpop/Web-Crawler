#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '深交所'


class Szse(Spider):
    start_urls = [
        'http://www.szse.cn/main/disclosure/bsgg_front/',
    ]
    url_pattern = [
        re.compile(r'(/main/disclosure/bsgg_front/\d+?\.shtml)')
    ]
    content_pattern = dict(
        title='.yellow_bt15',
        time='.botborder1',
        content='.td10 p',
    )
    charset = 'gb2312'
