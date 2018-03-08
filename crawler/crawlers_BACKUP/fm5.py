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


class FM5(CrawlerAbstract):
    title = u'FM5科技 - 内存,IC,SSD,手机芯片'
    start_urls = [
        'http://www.fm5.cn/?action-category-catid-8',
        'http://www.fm5.cn/?action-category-catid-99',
        'http://www.fm5.cn/?action-category-catid-135',
        'http://www.fm5.cn/?action-category-catid-142',
    ]
    url_links_selector = '.global_tx_list4 > li > a'
    content_selector = dict(
        title='h1',
        content='#article_body',
        date_area='#article_extinfo'
    )






