#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow

from spider import Spider

__name__ = '华夏时报'


class Chinatimes(Spider):
    url_pattern=re.compile(r'"(/article/\d+?\.html)"')
    def __init__(self):
        super(Chinatimes, self).__init__()
        self.start_urls = ['http://www.chinatimes.cc/finance']

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details += self.url_pattern.findall(r.text)
        url_details=map(lambda x:urljoin('http://www.chinatimes.cc/',x),url_details)
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

        title = p('.title').text()
        content = p('.infoMain').text()

        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=0
        )
