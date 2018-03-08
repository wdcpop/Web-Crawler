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


class PPI100(CrawlerAbstract):
    title = u'生意社 - 钛白粉,粘胶短纤,生猪,白糖,农副,化工,涤纶POY,尿素,己二酸,PA6'
    start_urls = [
        'http://tio2.100ppi.com/news/list--1211-1.html',
        'http://nianjiao.100ppi.com/news/list--12-1.html',
        'http://pig.100ppi.com/news/list--12-1.html',
        'http://sugar.100ppi.com/news/list--12-1.html',
        'http://www.100ppi.com/forecast/list-18-11-1.html',
        'http://www.100ppi.com/forecast/list-14-11-1.html',
        'http://poly.100ppi.com/news/list--12-1.html',
        'http://urea.100ppi.com/news/list--12-1.html',
        'http://j2s.100ppi.com/news/list--1211-1.html',
        'http://pa6.100ppi.com/news/list--12-1.html',
    ]
    url_links_selector = '.list-c ul:eq(0) li a:last'
    # url_patterns = [
    #     re.compile(r'"(http://www\.100ppi\.com/\S+/detail-\d{8}-\d+?\.html)"')
    # ]
    content_selector = dict(
        title='h1',
        content='.nd-c',
        date_area='.nd-info'
    )




