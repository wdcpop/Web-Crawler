#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import hashlib
import xmltodict
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
import dateparser


class PBC(CrawlerAbstract):
    title = u'中国人民银行 - 动态(MLF, SLF, PSL)'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Cookie': 'wzwsconfirm=00c0502487a2daf965780f2b99158640; wzwsvtime=1700000000; wzwstemplate=Mg==; wzwschallenge=-1; ccpassport=2349a47c791240d43052a0b6fdde54dc; _gscu_1042262807=816112928ligaq95; _gscs_1042262807=816112921g86ew95|pv:2; _gscbrs_1042262807=1'
    }  # wzwsvtime如果小于当前时间超过一定数值就会导致抓不到, 所以设置一个2020年的值来防止过期
    start_urls = [
        'http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125446/125873/index.html',
        'http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125443/125857/index.html',
        'http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/2161446/2161457/index.html',
    ]
    url_patterns = [
        re.compile(r'"(/zhengcehuobisi/125207/125213/\d+?/\d+?/\d+?/index.html)"')
    ]
    content_selector = CrawlerAbstract.preset_content_selector['PBC']



