#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider


class SampleSpider(Spider):
    start_urls = [
        'http://www.dce.com.cn/portal/cate?cid=1272437227100',
    ]
    url_pattern = [
        re.compile(r'(/portal/info\?cid=\d+?&iid=\d+?&type=CMS.OPERATION_NOTIFY)')
    ]
    content_pattern = dict(
        title='#news_title',
        content='#news_content_body',
    )
    charset = 'gb2312'
