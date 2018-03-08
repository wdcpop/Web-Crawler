#!/usr/bin/env python
# coding:utf8
import json
import re
from arrow import Arrow

from spider import Spider

__name__ = '第一财经'


class Yicai(Spider):
    def __init__(self):
        super(Yicai, self).__init__()
        self.start_urls = [
            "http://www.yicai.com/news/business/",
            "http://www.yicai.com/news/markets/",
            "http://www.yicai.com/news/technology/",
            "http://www.yicai.com/news/finance/",
            "http://www.yicai.com/news/economy/",
        ]

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            r.encoding='utf-8'
            query=self.pq(r.text)
            contents=query('#news_List dl')
            url_details=[]
            for content in contents:
                link=self.pq(content)('a:first')
                if link:
                    url_details.append(link.attr('href'))
            map(self.parse,url_details)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()

        pos=title.find(u' 相关阅读')
        if pos!=-1:
            title=title[:pos]

        #content = p('p').text()
        content = self.get_safe_html(p('p'))

        time_str=p('h2').text()
        if content=='' or time_str=='':
            self.blf.insert(url)
            return
        try:
            time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})', time_str)[0]
            src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M', tzinfo='Asia/Shanghai').timestamp
        except KeyError:
            time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日)', time_str)[0]
            src_time = Arrow.strptime(time_str, u'%Y年%m月%d年', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
