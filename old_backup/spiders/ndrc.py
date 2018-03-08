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

__name__ = '发改委'


class Ndrc(Spider):
    start_urls = [
        'http://www.ndrc.gov.cn/zcfb/zcfbghwb/',
        'http://bgt.ndrc.gov.cn/zcfb/',
        'http://www.ndrc.gov.cn/xwzx/xwfb/',
        'http://tzs.ndrc.gov.cn/tzgz/',
        'http://gys.ndrc.gov.cn/gyfz/index.html',
    ]
    url_pattern = [
        re.compile(r'(\./\d+?/t\d+?_\d+?\.html)')
    ]
    content_pattern = dict(
        title='title',
        content='.txt1',
    )
    categorys = [
        ('xwfb', '新闻发布'),
        ('zcfbghwb', '规划文本'),
        ('gyfz', '工业发展'),
        ('tzgz', '投资工作'),
        ('zcfb', '政策发布'),
    ]

    def result_hook(self, res):
        res['time'] = self.parse_time(res['link'])
        for cate, cate_name in self.categorys:
            if cate in res['link']:
                res['name'] = '{}-{}'.format(__name__, cate_name)
        return True
