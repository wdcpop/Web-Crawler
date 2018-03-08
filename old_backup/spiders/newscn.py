#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '新华网'


class Newscn(Spider):
    allow_source=[u'新华社',u'新华网']
    def __init__(self):
        super(Newscn, self).__init__()
        self.start_urls = [
            'http://www.news.cn/fortune/gd.htm',
            'http://www.xinhuanet.com/politics/24xsyw.htm',
            'http://www.news.cn/politics/leaders/gdxw.htm']

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url)
            url_details += re.findall(r'(http://news\.xinhuanet\.com/fortune/\d{4}-\d{2}/\d{2}/c_\d+?\.htm)', r.text)
            url_details += re.findall(r'(http://news\.xinhuanet\.com/politics/\d{4}-\d{2}/\d{2}/c_\d+?\.htm)', r.text)
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

        title = p('#title').text()
        content = p('.article').text()
        if content=='':
            content=p('#content').text()
        time_str=p('.time').text()
        if time_str=='':
            time_str=p('#pubtime').text()
        if content == '' or title=='' or time_str=='':
            self.blf.insert(url)
            return

        # time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日\s\d{2}:\d{2}:\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日 %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
        source=p('#source').text()
        if source not in self.allow_source:
            self.blf.insert(url)
            return
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
