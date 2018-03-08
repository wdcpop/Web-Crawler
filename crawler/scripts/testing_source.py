#!/usr/bin/env python
# coding:utf8
import sys, os
import _json
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), os.pardir))

import requests
from bspider.lib.response import rebuild_response
from crawler.crawlers.abstracts.crawler_abstract import CrawlerAbstract
import dateparser
from datetime import datetime
import re
from snownlp import SnowNLP
import time

import urllib
from urlparse import urljoin
from urlparse import urlsplit

input_info = {

    "title" : "BEIJING_PNC",
    "is_backend_render" : False,
    "machine_name" : "PBC_BJ",
    "start_urls" : [
        "http://beijing.pbc.gov.cn/beijing/132005/index.html"
    ],

    "content_selector": {
        "content": "//p",
        "date_area": "#shijian",
        "title": "//h2"
    },

    #"\"(/zhengcehuobisi/125207/125213/\\d+?/\\d+?/\\d+?/index.html)\""
    "url_patterns": [
        "\"(/beijing/132005/\\d+?/index.html)\""
    ],

    "use_link_content_as_detail_title" : True
}


# input_info = {
#
#
#     "start_urls : [
#         "http://disclosure.szse.cn//disclosure/fulltext/plate/szlatest_24h.js"
#     ],
#
# "use_link_content_as_detail_title": True,
# }

class CrawlerAbstractForTesting(CrawlerAbstract):
    def crawl(self, url, **kwargs):
        callback = kwargs.get('callback')
        function = getattr(self, callback)
        is_backend_render = input_info.get('is_backend_render', True)
        if is_backend_render:
            r = requests.get(url, proxies={"http" : self.actual_proxy, "https" : self.actual_proxy }, timeout=10)
            result = {}
            result['orig_url'] = url
            result['content'] = r.content or ''
            result['headers'] = dict(r.headers)
            result['status_code'] = r.status_code
            result['url'] = url
            result['time'] = 0
            result['cookies'] = None
            result['save'] = kwargs.get('save')
            response = rebuild_response(result)
        else:
            response = self.frontend_render_fetch(url, kwargs.get('save'))

        self._run_func(function, response)

    # def details_hook(self, details):
    #     return [details[0]] if details else []
    #


cb = CrawlerAbstractForTesting()
cb.to_save = {'config': input_info}
cb.on_start()



for _ in cb.return_items:
    title = _.get('title')
    content = _.get('content')
    print 'content..', content

output_info = {
    "index_url_list" : cb.index_url_list,
    "content_dict" : {
        "title" : title,
        "content" : content[:20]
    }
}

# print output_info

