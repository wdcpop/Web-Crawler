#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow

from spider import Spider

__name__ = '阿斯达克'


class Aastocks(Spider):
    url_pattern=re.compile(r'(/sc/stocks/news/aafn-content/NOW\.\d+?/\w+?-news)')
    def __init__(self):
        super(Aastocks, self).__init__()
        self.start_urls = ['http://www.aastocks.com/sc/stocks/news/aafn']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            #.grid_11
            url_details = self.url_pattern.findall(self.pq(r.text)('.grid_11').html())
            url_details=map(lambda x:urljoin(url,x),url_details)
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

        title = p('#lblSTitle').text()
        content = p('#spanContent').text()

        time_str=p('#spanDateTime').text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
