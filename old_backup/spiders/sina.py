#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import json
import re
from arrow import Arrow

from spider import Spider

__name__ = '新浪财经'


class Sina(Spider):
    def __init__(self):
        super(Sina, self).__init__()
        self.start_urls = [
            'http://roll.finance.sina.com.cn/finance/gncj/hgjj/index.shtml'
        ]

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = re.findall(r'(http://finance\.sina\.com\.cn/[\w/]+?/\d{4}-\d{2}-\d{2}/doc-\w+?\.shtml)',r.text)
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

        title = p('#artibodyTitle').text()
        content = p('.article').text()
        time_str = p('.time-source').text()
        if time_str=='':
            content=p('#artibody').text()
            time_str=p('#pub_date').text()
            time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日\s\d{2}:\d{2})', time_str)[0]
            src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日 %H:%M', tzinfo='Asia/Shanghai').timestamp
        else:
            time_str = re.findall(ur'(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})', time_str)[0]
            src_time = Arrow.strptime(time_str.encode('utf8'), '%Y年%m月%d日%H:%M', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
