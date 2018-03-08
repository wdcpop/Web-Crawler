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

__name__ = '中国政府-政策'


class Govzhengce(Spider):
    url_pattern = [
        re.compile('(http://www\.gov\.cn/zhengce/content/\d{4}-\d{2}/\d{2}/content_\d+?.htm)'),
    ]

    def __init__(self):
        super(Govzhengce, self).__init__()
        self.start_urls = [
            'http://www.gov.cn/zhengce/zuixin.htm',
        ]

    def run(self):
        url_details = []
        for url in self.start_urls:
            r = self.s.get(url)
            for i in self.url_pattern:
                url_details+=i.findall(r.text)
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        map(self.parse, url_details)
        return self.result


    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('.bd1 tr:eq(2) td:eq(1)').text()
        content = p('.b12c').text()
        time_str = p('.bd1 tr:eq(3) td:eq(3)').eq(-2).text()

        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
