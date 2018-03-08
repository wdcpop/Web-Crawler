#!/usr/bin/env python
#coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import re
from urlparse import urljoin

from spider import Spider

__name__ = '中国政府-新闻'


class Govnews(Spider):
    url_pattern = [
        re.compile('(/xinwen/\d{4}-\d{2}/\d{2}/content_\d+?\.htm)'),
    ]

    def __init__(self):
        super(Govnews, self).__init__()
        self.start_urls = [
            'http://www.gov.cn/xinwen/gundong.htm'
                           ]


    def run(self):
        url_details = []
        for url in self.start_urls:
            r = self.s.get(url)
            for i in self.url_pattern:
                url_details += i.findall(r.text)
                url_details = [urljoin('http://www.gov.cn/',i) for i in url_details]
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        map(self.parse, url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('.article h1').text()
        if title=='':title=p('.pages-title').text()
        content = p('.pages_content').text()
        if content=='':
            self.blf.insert(url)
            return
        time_str=p('.pages-date').text()

        #time_str = re.findall(ur'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', time_str)[0]
        #src_time = Arrow.strptime(time_str.encode('utf8'), '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
