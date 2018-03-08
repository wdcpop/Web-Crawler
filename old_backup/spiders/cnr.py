#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '央广网-经济之声'


class Cnr(Spider):
    def __init__(self):
        super(Cnr, self).__init__()
        self.start_urls = ['http://roll.cnr.cn/finance/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(http://www\.cnr\.cn/list/finance/\d{8}/t\d{8}_\d+?\.shtml)', r.text)
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

        title = p('.f22').text()
        content = p('.f16').text()

        time_str=p('.f14').text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
