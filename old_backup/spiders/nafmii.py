#!/usr/bin/env python
# coding:utf8

import re
import time
from spider import Spider

__name__ = '银行间交易商协会'

class Nafmii(Spider):
    start_urls = ['http://www.nafmii.org.cn/zdgz/']
    url_pattern = [
        re.compile(r'(\.\/\d{6}\/t\d{8}_\d+.html)')
        ]
    
    def _get_query(self,url):
        page = self.s.get(url)
        page.encoding = 'utf8'
        return self.pq(page.text)
    
    def parse(self,url):
        url=url.encode('utf-8')
        date_string=url.rsplit(r'/t',1)[1][:8].decode('utf-8')
        if self.check_bloomfilter(url): return
        query=self._get_query(url)
        self.addresult(
            name=__name__,
            title=query('title').text(),
            content=query('.Section1').html(),
            time=date_string,
            link=url
        )
    
    def after_test(self):
        for node in self.result:
            print('### ===============')
            for k,v in node.items():
                if k!='content':
                    print('### %s --> %s'%(k,v))