#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '21经济'


class Jingji21(Spider):
    def __init__(self):
        super(Jingji21, self).__init__()
        self.start_urls = ['http://www.21jingji.com/channel/herald/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(http://m\.21jingji\.com/article/\d{8}/herald/[\d\w]+?\.html)', r.text)
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

        title = p('h1').text()
        content = p('.txtContent').text()

        time_str=p('h1').next().text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
