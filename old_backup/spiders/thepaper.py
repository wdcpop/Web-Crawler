#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin

from arrow import Arrow

from spider import Spider

__name__ = '澎湃新闻-财经'


class ThePaper(Spider):
    def __init__(self):
        super(ThePaper, self).__init__()
        self.start_urls = ['http://www.thepaper.cn/channel_scroll.jsp?channelID=25951']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'href="(newsDetail_forward_\d+?)"', r.text)
            url_details=map(lambda x:urljoin('http://www.thepaper.cn',x),url_details)
            if not url_details:
                raise Exception(u'{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        if not title or u'专题' in title:
            self.blf.insert(url)
            return
        content = p('.news_txt').text()
        time_str=p('.news_about').text()
        # time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
