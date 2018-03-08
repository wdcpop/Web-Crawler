#!/usr/bin/env python
# coding:utf8

import re
import time
from spider import Spider

__name__ = '香港经济日报'

class Hket(Spider):
    start_urls = ['http://inews.hket.com/sran001/']
    url_pattern = [
        re.compile(r'(http://[a-z]+.hket.com/article/\d+/.+?)\"')
        ]
    
    def _get_query(self,url):
        page = self.s.get(url)
        page.encoding = 'utf8'
        return self.pq(page.text)
    
    def parse(self,url):
        url=url.encode('utf-8')
        if self.check_bloomfilter(url): return
        hostname=self.extract_hostname(url)
        if hostname in ['inews.hket.com','paper.hket.com']:
            query=self._get_query(url)
            result={
                'title':query('#eti-article-headline h1').text(),
                'content':query('#eti-article-content-body').html(),
                'time':query('#eti-article-functions div:eq(0)').text()
            }
        elif hostname=='invest.hket.com':
            query=self._get_query(url)
            result={
                'title':query('#headline').text(),
                'content':query('#content-main .content-content').html(),
                'time':query('#news-date').text()
            }
        elif hostname=='china.hket.com':
            query=self._get_query(url)
            page_time=query('#main-left > div:eq(1)').text()
            page_time=re.sub(ur'星期.{1,3}\s',u'',page_time,flags=re.UNICODE)
            result={
                'title':query('#main-left > div:eq(2) > div:eq(1)').text(),
                'content':query('#content-main').html(),
                'time':page_time
            }
        else:
            result=None
        if result:
            self.addresult(
                name=__name__,
                link=url,
                **result
            )
    
    def after_test(self):
        for node in self.result:
            print('### ===============')
            for k,v in node.items():
                print('### %s --> %s'%(k,v))