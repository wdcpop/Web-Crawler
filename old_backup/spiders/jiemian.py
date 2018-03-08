#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '界面网'


class Jiemian(Spider):
    url_pattern = re.compile(ur'(http://www\.jiemian\.com/article/\d+?\.html)')

    def __init__(self):
        super(Jiemian, self).__init__()
        self.start_urls = ['http://www.jiemian.com/lists/9.html']

    def run(self):
        url_details = []
        for url in self.start_urls:
            r = self.s.get(url)
            url_details += self.url_pattern.findall(r.text)
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        map(self.parse, url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return

        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        content = p('.article-content').text()

        time_str = p('.date').text()
        if not content:
            self.blf.insert(url)
            return
        self.addresult(
                name=__name__,
                title=title,
                content=content,
                link=url,
                time=time_str
        )
