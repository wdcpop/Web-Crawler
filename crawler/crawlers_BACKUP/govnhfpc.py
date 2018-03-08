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


class GOVNHFPC(CrawlerAbstract):
    title = u'卫计委 - 工作动态'
    start_urls = [
        'http://www.nhfpc.gov.cn/zhuzhan/wnsj/lists.shtml',
    ]
    url_links_selector = '.contents ul li a'
    content_selector = dict(
        title='.content_title',
        content='.content',
        date_area='.content_subtitle'
    )



