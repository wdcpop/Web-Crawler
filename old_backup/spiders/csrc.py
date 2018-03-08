#!/usr/bin/env python
#coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import re
from arrow import Arrow

from spider import Spider

__name__ = '证监会要闻'


class Csrc(Spider):
    def __init__(self):
        super(Csrc, self).__init__()
        self.start_urls = ['http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(\./\d+?/t\d+?_\d+?\.html)', r.text)
            url_details=map(lambda x:'{0}{1}'.format('http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd',x[1:]),url_details)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('title').text()
        content = p('.Custom_UnionStyle').text()
        time_str=p('.time').text()
        # time_str = re.findall(r'(\d{4}-\d{2}-\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str.encode('utf8'), '%Y-%m-%d', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
