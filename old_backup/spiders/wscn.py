#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '华尔街见闻'


class Wscn(Spider):
    url_pattern=re.compile(ur'(https?://wallstreetcn.com/node/\d+?)')
    start_urls = ['http://api.wallstreetcn.com/v2/posts']
    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details+=map(lambda x:x['url'],r.json()['results'])
        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        url_details=filter(lambda x:self.url_pattern.match(x), url_details)
        map(self.parse,url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('.title-text').text()
        #content = p('.article-content').remove('img').text()
        content = p('.page-article-content').remove('p:last, img:last').text()

        time_str=p('.time').text()

        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
