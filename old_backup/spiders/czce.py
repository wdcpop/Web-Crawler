#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from spider import Spider

__name__ = '郑商所'


class Czce(Spider):
    start_urls = [
        'http://www.czce.com.cn/portal/jysdt/ggytz/A090601index_1.htm',
    ]

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            r.encoding='gb2312'
            p=self.pq(r.text)
            for title in p('.title a').items():
                name= title.text()
                link =urljoin(url,title.attr('href'))
                if not self.check_bloomfilter(link):
                    self.addresult(name=__name__,title=name,content=u'详情点原文链接，是pdf 文件来的..',link=link)
    def parse(self, url):
        pass
