#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '上证快讯'


class Cnstock(Spider):
    charset = 'gbk'
    content_pattern = dict(
        title='h1',
        content='.content',
        time='.timer'
    )

    def __init__(self):
        super(Cnstock, self).__init__()
        self.start_urls = ['http://news.cnstock.com/bwsd/index.html']

    def run(self):
        url_patterns = [
            re.compile(r'href="(http://.+?\.cnstock\.com/company/.+?\.html{0,1})"'),
            re.compile(r'href="(http://.+?\.cnstock\.com/stock/.+?\.html{0,1})"'),
            re.compile(r'href="(http://.+?\.cnstock\.com/news/.+?\.html{0,1})"'),
            re.compile(r'href="(http://.+?\.cnstock\.com/theme/.+?\.html{0,1})"'),
            re.compile(r'href="(http://.+?\.cnstock\.com/xg/.+?\.html{0,1})"'),
        ]
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            r.encoding=self.charset
            query=self.pq(r.text)
            content=query('#bw-list').html()
            for url_pattern in url_patterns:
                url_details += url_pattern.findall(content)
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        for url_detail in url_details:
            self.parse(url_detail)
        return self.result

