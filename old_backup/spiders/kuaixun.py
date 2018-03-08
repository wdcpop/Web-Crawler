#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '证券时报'


class Kuaixun(Spider):
    def __init__(self):
        super(Kuaixun, self).__init__()
        self.start_urls = ['http://kuaixun.stcn.com/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'http://kuaixun\.stcn\.com/\d+?/\d+?/\d+?\.shtml', r.text)
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
        content = p('.txt_con').remove('p:eq(0)').remove('.om').text()
        content = re.sub(r'show_quote\(.*?\);', '', content)
        time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})', p('.info').text())[0]
        src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        title=p('.intal_tit h2').text()
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
