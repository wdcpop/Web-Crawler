#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow

from spider import Spider

__name__ = '商务部'


class Mofcom(Spider):
    def __init__(self):
        super(Mofcom, self).__init__()
        self.start_urls = ['http://www.mofcom.gov.cn/article/ae/ai/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'"(/article/ae/ai/\d{6}/\d+?\.shtml)"', r.text)
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

        title = p('#artitle').text()
        content = p('.artCon').text()

        time_str=p('script').text()
        time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', time_str)[0]
        src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
