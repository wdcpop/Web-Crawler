#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import urllib
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class HKET(CrawlerAbstract):
    start_urls = [
        'http://inews.hket.com/sran001/',
    ]
    url_links_selector = '#eti-inews-list tr:lt(5) td a'

    @staticmethod
    def extract_hostname(url):
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        return host

    def detail_page(self, response):
        if self.removing_style_and_script:
            response.doc('script').remove()
            response.doc('style').remove()

        query = response.doc

        hostname = self.extract_hostname(response.url)

        result = {}
        if hostname in ['inews.hket.com', 'paper.hket.com']:
            result = {
                'title': query('#eti-article-headline h1').text(),
                'content': query('#eti-article-content-body').html(),
                'time': query('#eti-article-functions div:eq(0)').text()
            }
        elif hostname == 'invest.hket.com':
            result = {
                'title': query('#headline').text(),
                'content': query('#content-main .content-content').html(),
                'time': query('#news-date').text()
            }
        elif hostname == 'china.hket.com':
            page_time = query('#main-left > div:eq(1)').text()
            page_time = re.sub(ur'星期.{1,3}\s', u'', page_time, flags=re.UNICODE)
            result = {
                'title': query('#main-left > div:eq(2) > div:eq(1)').text(),
                'content': query('#content-main').html(),
                'time': page_time
            }

        dt_dict = self.get_datestr_and_dateint(result.get('time'))
        datestr = dt_dict.get('datestr', '')
        dateint = dt_dict.get('dateint', 0)

        return {
            "acknowledged": True,
            "link": response.url,
            "host": "{0.netloc}".format(urlsplit(response.url)),
            "title": result.get('title'),
            "time_human": datestr,
            "time": dateint,
            "ctime": int(time.time()),
            "content": result.get('content')
        }
