#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow
from lxml.html import HtmlElement

from spider import Spider

__name__ = '财新一线'


class Kcaixin(Spider):
    def __init__(self):
        super(Kcaixin, self).__init__()
        self.start_urls = ['http://k.caixin.com/web/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            p=self.pq(r.text)
            for url_detail in p('dd h2 a'):
                self.parse(urljoin(url,self.pq(url_detail).attr('href')),self.pq(url_detail).text())
        return self.result

    def parse(self, url,data):
        if self.check_bloomfilter(url): return
        # r_detail = self.s.get(url)
        # r_detail.encoding = 'gb2312'
        # p = self.pq(r_detail.text)

        # title = p('.f22').text()
        # content = p('.f16').text()
        #
        # time_str=p('.f14').text()
        # time_str = re.findall(r'.*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}).*', time_str)[0]
        # src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=data,
            content=data,
            link=url,
            time=0
        )
