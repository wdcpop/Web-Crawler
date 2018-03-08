#!/usr/bin/env python
# coding:utf8
import re

import xmltodict
from arrow import Arrow

from spider import Spider

__name__ = '路透中文'


class Reuters(Spider):
    def __init__(self):
        super(Reuters, self).__init__()
        self.start_urls = [
            'http://cn.reuters.com/rssFeed/chinaNews/',
            'http://cn.reuters.com/rssFeed/CNIntlBizNews/',
                           ]

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details += xmltodict.parse(r.text)['rss']['channel']['item']
        url_details = map(lambda x: x['link'], url_details)
        url_details = {}.fromkeys(url_details).keys()

        if not url_details:
            raise Exception('{0} 找不到详情页链接!'.format(__name__))
        map(self.parse,url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        content = p('#article-text').text()

        time_str=p('.timestamp').text()
        if content=='':
            self.blf.insert(url)
            return
        #time_str = re.match(ur'(\d{4})年 (\d{1,2})月 (\d{1,2})日.+?(\d{2}):(\d{2})', time_str).groups()
        #time_str=map(int,time_str)
        #src_time = Arrow.utcnow().replace(year=time_str[0],month=time_str[1],day=time_str[1],hour=time_str[1],minute=time_str[1],second=0).timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
