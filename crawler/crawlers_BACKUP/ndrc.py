#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class NDRC(CrawlerAbstract):
    start_urls = [
        'http://www.ndrc.gov.cn/zcfb/zcfbghwb/',
        'http://bgt.ndrc.gov.cn/zcfb/',
        'http://www.ndrc.gov.cn/xwzx/xwfb/',  # same as 'http://zys.ndrc.gov.cn/xwfb/'
        'http://tzs.ndrc.gov.cn/tzgz/',
        'http://gys.ndrc.gov.cn/gyfz/index.html',

        'http://www.ndrc.gov.cn/gzdt/',
        'http://www.ndrc.gov.cn/jjxsfx/',
        'http://www.ndrc.gov.cn/zcfb/zcfbtz/',
    ]
    url_links_selector = ''
    url_patterns = [
        re.compile(r'(\./\d+?/t\d+?_\d+?\.html)'),
        re.compile(r'(\./\d+?/P\d+?\.pdf)'),
    ]
    content_selector = dict(
        title='title',
        content='.txt1',
        date_area=''
    )

    def get_date_area(self, response):
        return response.url

    def result_hook(self, res, response):
        """由于source_title无法更改, 暂时不生效"""
        categorys = [
            ('xwfb', u'新闻发布'),
            ('zcfbghwb', u'规划文本'),
            ('gyfz', u'工业发展'),
            ('tzgz', u'投资工作'),
            ('zcfb', u'政策发布'),
            ('gzdt', u'工作动态'),
            ('jjxsfx', u'经济形势分析'),
        ]

        for cate, cate_name in categorys:
            if cate in res['link']:
                res['source_title'] = u'{} - {}'.format(u'发改委', cate_name)
        return res



