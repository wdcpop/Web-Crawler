#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow
from urlparse import urljoin
from spider import Spider

__name__ = '中国新闻网'


class Chinanews(Spider):
    def __init__(self):
        super(Chinanews, self).__init__()
        self.start_urls = [
            'http://www.chinanews.com/cj/gd.shtml',
        ]

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(/cj/\d{4}/\d{2}-\d{2}/\d+?\.shtml)', r.text)
            url_details = map(lambda x: urljoin('http://www.chinanews.com', x), url_details)
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

        if u'中国新闻网-404页面' in r_detail.text:
            self.blf.insert(url)
            return
        title = p('h1').text()
        content = p('.left_zw').text()

        time_str = p('.left-t').text()
        time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日\s\d{2}:\d{2})', time_str)[0]
        src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日 %H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
