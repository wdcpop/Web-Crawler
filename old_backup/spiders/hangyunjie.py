#!/usr/bin/env python
# coding:utf8
import re
from arrow import Arrow

from spider import Spider

__name__ = '航运界'


class Hangyunjie(Spider):
    def __init__(self):
        super(Hangyunjie, self).__init__()
        self.start_urls = ['http://www.ship.sh/info.php']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'\./(news_detail\.php\?nid=\d{5,}?)', r.text)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            url_details=map(lambda x:'http://www.ship.sh/'+x,url_details)
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        if 'not found article' in r_detail.text:
            self.blf.insert(url)
            return
        p = self.pq(r_detail.text)
        title = p('h1').text()
        content = p('.content').text()
        time_str = p('.f12_hui').text()
        time_str = re.findall(ur'(\d{2}月\d{2}日 \d{2}时)', time_str)[0]
        src_time = Arrow.strptime(time_str.encode('utf8'), '%m月%d日 %H时', tzinfo='Asia/Shanghai').replace(year=Arrow.now().datetime.year).timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
