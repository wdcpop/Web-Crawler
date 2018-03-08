#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-7
"""

import re
from arrow import Arrow
from spider import Spider

__name__ = '网易财经'

class Money163(Spider):
    url_pattern=re.compile(r'"(http://money\.163\.com/1\d/\d+?/\d+?/.+?.html)"')
    def __init__(self):
        super(Money163, self).__init__()
        self.start_urls = [
            'http://money.163.com/special/00251G8F/news_json.js',
        ]

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = self.url_pattern.findall( r.text)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url):
            return
        r_detail = self.s.get(url)
        r_detail.encoding = 'gb2312'
        if u'http://money.163.com/special/special.html' in r_detail.text:
            self.blf.insert(url)
            return
        p = self.pq(r_detail.text)
        content = p('p').text()
        time_str = p('.post_time_source').text()
        if time_str == '':
            time_str = p('.ep-time-soure').text()
        if time_str == '':
            time_str = p('.con1_date').text()
        if time_str == '':
            time_str = p('.left').text()
        if time_str == '':
            time_str = p('.info').text()
        title = p('h1').text()
        if title == '':
            title = p('.ep-h1').text()
        if title == '':
            title = p('.con1_ltle').text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
