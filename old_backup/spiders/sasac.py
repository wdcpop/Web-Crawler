#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import re
from urlparse import urljoin

from spider import Spider

__name__ = '国资委'


class Sasac(Spider):
    url_pattern = re.compile(ur'(n\d+?/n\d+?/c\d+?/content\.html)')
    def __init__(self):
        super(Sasac, self).__init__()
        self.start_urls = [
            'http://www.sasac.gov.cn/n85881/n85901/index.html'
        ]

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details += self.url_pattern.findall(r.text)
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        url_details=map(lambda x:urljoin('http://www.sasac.gov.cn/',x),url_details)
        map(self.parse, url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        content = p('.tcon').text()
        if not content:
            self.blf.insert(url)
            return
        time_str =p('#con_time').text()
        # time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日)', time_str)[0]
        # src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
                name=__name__,
                title=title,
                content=content,
                link=url,
                time=time_str
        )
