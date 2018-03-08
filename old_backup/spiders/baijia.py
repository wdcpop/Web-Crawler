#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '百度百家-财经版'


class Baijia(Spider):
    url_pattern=re.compile(r'"(http://.+?\.baijia\.baidu\.com/article/\d+?)"')
    time_pattern=re.compile(ur'(\d{2}月\d{2}日\s\d{2}:\d{2})')
    def __init__(self):
        super(Baijia, self).__init__()
        self.start_urls = ['http://baijia.baidu.com/?tn=listarticle&labelid=6']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = self.url_pattern.findall( r.text)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        if u'很抱歉，您要访问的页面不存在！' in r_detail.text:
            self.blf.insert(url)
            return
        p = self.pq(r_detail.text)
        title = p('h1').text()
        content = p('.article-detail').text()

        time_str=p('.time').text()
        time_str = self.time_pattern.findall( time_str)[0]
        if content=='':content=p('blockquote').text()
        src_time = Arrow.strptime(time_str.encode('utf8'), '%m月%d日 %H:%M', tzinfo='Asia/Shanghai').replace(year=Arrow.now().datetime.year).timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
