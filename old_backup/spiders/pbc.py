#!/usr/bin/env python
# coding:utf8
import re
from urlparse import urljoin, parse_qsl

from arrow import Arrow

from spider import Spider

__name__ = '中国人民银行'

from lib import PyV8 as v8


class JS(object):
    def __init__(self):
        pass


class Cookie(object):
    def __init__(self):
        self._cookie = {}

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, v):
        self._cookie.update(dict(parse_qsl(re.findall(r'(.+?);', v)[0])))


class Pbc(Spider):
    start_urls = ['http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html']
    def run(self):
        r =self.s.get('http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html')
        if u'JavaScript' in r.text:
            js = self.pq(r.text).find(
                'script').text()
            g = JS()
            g.documentElement = JS()
            g.body = JS()
            g.document = Cookie()  # type:Cookie()
            g.window = JS()
            g.window.screen = JS()
            g.window.screen.width = 1024
            g.window.innerHeight = 768
            g.window.innerWidth = 1024
            g.window.location = ''
            g.body.clientWidth = 1024
            g.body.clientHeight = 768
            g.documentElement = g.body
            with v8.JSContext(g) as ctx:
                self.s.cookies.clear()
                ctx.eval(js)
                self.s.cookies.update(g.document.cookie)
            r = self.s.get(self.start_urls[0])
            del g
        for url in self.start_urls:
            # r = self.s.get(urljoin(url, g.window.location))
            url_details = re.findall(r'"(/goutongjiaoliu/113456/113469/\d+?/index\.html)"', r.text)
            url_details = map(lambda x: urljoin(url, x), url_details)
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

        title = p('h2').text()
        content = p('#zoom').text()

        time_str = p('.hui12').text()
        # time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', time_str)[0]
        # src_time = Arrow.strptime(time_str, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
        self.addresult(
            name=__name__,
            title=title,
            content=content,
            link=url,
            time=time_str
        )
