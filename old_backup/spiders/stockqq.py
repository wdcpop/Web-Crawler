#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '腾讯证券'


class Stockqq(Spider):
    def __init__(self):
        super(Stockqq, self).__init__()
        self.start_urls = ['http://stock.qq.com/l/stock/list20150525114649.htm']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(http://stock\.qq\.com/a/\d{8}/\d+?\.htm)', r.text)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'gb2312'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        if title=='':
            self.blf.insert(url)
            return
        content = p('p').text()

        time_str=p('.pubTime').text()
        if time_str!='':
            time_str = re.findall(ur'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})', time_str)[0]
            src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        else:
            src_time=0
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
