#! /usr/bin/python
# coding:utf-8

import logging
from urlparse import urljoin
from datetime import datetime
import time
import re
import urllib
import hashlib

import requests
import user_agent
from pyquery import PyQuery

from bloom.bloomfilter import BloomFilter

class FakeBlf(object):
    
    def __init__(self,spider):
        self._spider=spider
    
    def insert(self,url):
        return self._spider.check_bloomfilter(url)

class Spider(object):
    start_urls = []
    url_pattern = []
    content_pattern = {}
    charset='utf-8'
    
    def __init__(self):
        self._session=requests.Session()
        self._session.headers.update({'User-Agent': user_agent.generate_user_agent(platform='win', navigator='chrome')})
        self._session.headers.update({'CacheControl': 'no-cache'})
        self._session.headers.update({'Pragma': 'no-cache'})
        self._session.headers.update({'Expires': '-1'})
        logger=logging.getLogger(self.__module__)
        handler=logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self._logger=logger
        self.result=[]
        self._accept_old_fashion()
        self._bloomfilter=BloomFilter()
        
    def get_safe_html(self, query):
        return query.text()

    def _accept_old_fashion(self):
        self.s=self._session
        self.pq=PyQuery
        self.blf=FakeBlf(self)
        self.repeat_check=self.check_bloomfilter
        self.req=self._session.get
	
    def set_proxy(self,proxy_host):
        if proxy_host:
            self._session.proxies.update({'http':proxy_host,'https':proxy_host})
    
    def run(self):
        url_details=[]
        for url in self.start_urls:
            resp=self._session.get(url)
            self._logger.info('%d length data received from url [%s]'%(len(resp.text),url))
            for pattern in self.url_pattern:
                url_details += [urljoin(url, _) for _ in pattern.findall(resp.text)]
        map(self.parse, url_details)
        return self.result

    def result_hook(self,result):
        return True
    
    def check_bloomfilter(self,url):
        #filter_checks=self._bloomfilter.check(url)
        #print(url,filter_checks)
        return False
    
    def addresult(self,name='',title='',content='',link='',**kwargs):
        if 'createdAt' in kwargs:
            kwargs['time']=kwargs['createdAt']
        result = {
            'name': name, 'title': title, 'content': content,
            'link': link, 'host': self.extract_hostname(link),
            'ctime': time.time(), 'time': self.parse_time(kwargs['time'])
            }
        if len(title) == 0:
            raise ValueError(u'标题为空{}'.format(link))
        if len(content) == 0:
            raise ValueError(u'内容为空{}'.format(link))
        self.result.append(result)
        
    def parse_time(self, ctime):
        if isinstance(ctime, unicode) or isinstance(ctime, str):
            for time_re, arrow_fmt in time_formats:
                result = time_re.search(ctime)
                if result:
                    ret = datetime.strptime(result.group(1).encode('utf8'), arrow_fmt)
                    return (ret - datetime(1970, 1, 1)).total_seconds()
            return 0
        else:
            return ctime
        
    def parse(self,url):
        if self.check_bloomfilter(url):
            return
        page = self._session.get(url)
        page.encoding = self.charset
        query = PyQuery(page.text)
        article_attrs = {}
        for key, value in self.content_pattern.iteritems():
            if isinstance(value, str) or isinstance(value, unicode):
                article_attrs[key] = query(value).remove('style').remove('script').text()
            elif isinstance(value, re.compile('')):
                article_attrs[key] = value.match(page.text).group(1)
        result=dict(
            name=self.__module__,
            link=url,
            **article_attrs
        )
        result['raw']=page.text
        if not self.result_hook(result):
            return
        result.pop('raw')
        self.addresult(**result)

    @staticmethod
    def extract_hostname(url):
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        return host
    
    def log(self,msg):
        self._logger.info(msg)
        
    def clear(self):
        self.result=[]

time_formats = [
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2})'),
        '%Y年%m月%d日%H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}:\d{2})'),
        '%Y.%m.%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})'),
        '%Y/%m/%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2})'),
        '%Y-%m-%d'
    ),
    (
        re.compile(ur'(\d{4}/\d{2}/\d{2})'),
        '%Y/%m/%d'
    ),
    (
        re.compile(ur'(\d{4}年\d{2}月\d{2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}\d{2}\d{2})'),
        '%Y%m%d'
    )
]