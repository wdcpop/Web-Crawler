#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '腾讯科技'


class Techqq(Spider):
    url_pattern=re.compile(ur'(http://tech\.qq\.com/a/\d+?/\d+?\.htm)')
    def __init__(self):
        super(Techqq, self).__init__()
        self.start_urls = ['http://n.rss.qq.com/rss/tech_rss.php']

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details+=self.url_pattern.findall(r.text)
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        map(self.parse,url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return

        r_detail = self.s.get(url)
        r_detail.encoding = 'gb2312'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        content = p('#Cnt-Main-Article-QQ').text()
        time_str=p('.pubTime').text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
