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


class CEROLL(CrawlerAbstract):
    title = u'中国经济网 - 滚动'
    start_urls = [
        'http://finance.ce.cn/rolling/index.shtml'
    ]
    # 页面需要抓取的链接太多导致部分代理被屏蔽, 换成url_links_selector限制抓取数量
    # url_patterns = [
    #     re.compile(r'(./\d{6}/\d{2}/t\d{8}_\d{8}.shtml)')
    # ]
    url_links_selector = '.list_left > table:eq(1) > tr:lt(7) td a'
    content_selector = dict(
        title='#articleTitle',
        content='.TRS_Editor',
        date_area='#articleTime'
    )



