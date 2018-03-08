#!/usr/bin/env python
# coding:utf8
import re

from spider import Spider

__name__ = '新浪科技'


class Techsina(Spider):
    url_pattern=re.compile(ur'(http://tech\.sina\.com\.cn/i/\d{4}-\d{2}-\d{2}/doc-.+?\.shtml)')
    def __init__(self):
        super(Techsina, self).__init__()
        self.start_urls = ['http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=30&spec=&type=&date=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=1']

    def run(self):
        url_details=[]
        for url in self.start_urls:
            r = self.s.get(url,headers={'Referer':'http://roll.tech.sina.com.cn/s/channel.php?ch=05'})
            url_details+=self.url_pattern.findall(r.text)
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

        content = p('.content').remove('img').text()
        if not content:
            content=p('#artibody').text()
        if not content:
            self.blf.insert(url)
            return
        time_str=p('.titer').text()
        if not time_str:
            time_str=p('#pub_date').text()
        if u'<TITLE> 页面没有找到 </TITLE>' in r_detail.text:
            self.blf.insert(url)
            return
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
