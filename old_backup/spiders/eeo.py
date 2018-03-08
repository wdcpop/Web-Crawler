#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '经济观察'


class Eeo(Spider):
    def __init__(self):
        super(Eeo, self).__init__()
        self.start_urls = ['http://www.eeo.com.cn/politics/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'"(http://www\.eeo\.com\.cn/\d+?/\d+?/\d+?\.shtml)"', r.text)
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

        title = p('.wz_bt').text()
        content = p('.wz_zw').text()

        time_str=p('#pubtime_baidu').text()
        # time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
