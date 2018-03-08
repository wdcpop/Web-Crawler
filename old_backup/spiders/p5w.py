#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow

from spider import Spider

__name__ = '全景快讯'


class P5w(Spider):
    def __init__(self):
        super(P5w, self).__init__()
        self.start_urls = ['http://www.p5w.net/kuaixun/tj/']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            r.encoding='gb2312'
            query=self.pq(r.text)
            items=query('.manlist3 li')
            url_details=[]
            for item in items:
                link=self.pq(item)('a:first')
                url_details.append(link.attr('href'))
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
        content = p('.article_content2').text()
        if not content:
            self.blf.insert(url)
            return
        time_str=p('time').text()
        # time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日 %H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
