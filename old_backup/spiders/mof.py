#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '财政部'


class Mof(Spider):
    def __init__(self):
        super(Mof, self).__init__()
        self.start_urls = ['http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(http://.+?\.mof\.gov\.cn/\w+?/\w+?/\d+?/t\d+?_\d+?.html)', r.text)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'gb2312'
        p = self.pq(r_detail.text)

        title = p('.font_biao1').text()
        content = p('td > div ').text()

        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=0
        )
