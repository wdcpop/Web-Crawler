#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-9
"""
import json
import re
import trace
import traceback
from random import choice
from urlparse import parse_qsl, urljoin

import requests
from pyquery import PyQuery
from coloredlogs import install
from user_agent import generate_user_agent

import lib.PyV8 as v8


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


def jsrunner(js):
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
        ctx.enter()
        ctx.eval(js)
    return g.document.cookie, g.window.location


from settings import PROXIES


def pbc():
    install()
    url = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html'
    s = requests.Session()
    s.proxies.update({'http': '{0[0]}:{0[1]}'.format(choice(PROXIES))})
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'})
    r = s.get(url)
    js = PyQuery(r.text).find('script').text()
    print js
    cookie, href = jsrunner(js)
    s.cookies.update(cookie)
    r = s.get(urljoin(url, href))
    r.encoding = 'utf8'
    print PyQuery(r.text).find('title').text()


from xmltodict import parse
def main():
    # files=[i for i in glob.glob1(join(getcwdu(),'spiders'),'*.py') if isfile(join(getcwdu(),'spiders',i))]
    # files=set(files)
    # modules=[]
    # for filename in files:
    #     with open('spiders/'+filename,'r') as f:
    #         mat=re.findall(r'__name__\s*?=\s*?\'(.+?)\'',f.read())
    #         if mat:
    #             modules.append(mat[0])
    # return modules
    s = requests.Session()
    s.headers['User-Agent'] = generate_user_agent()
    s.proxies.update({
        'http': 'http://112.124.1.118:50000',
        'https': 'http://112.124.1.118:50000',
    })
    r=s.get('http://cn.reuters.com/rssFeed/chinaNews/')
    ret= parse(r.text)['rss']['channel']['item']
    r=s.get('http://cn.reuters.com/rssFeed/CNIntlBizNews/')
    ret+= parse(r.text)['rss']['channel']['item']
    ret=map(lambda x:x['link'],ret)
    ret={}.fromkeys(ret).keys()
    print json.dumps(ret,ensure_ascii=False,indent=4)
if __name__ == '__main__':
    main()
