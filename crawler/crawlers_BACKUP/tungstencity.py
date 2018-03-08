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


class TUNGSTENCITY(CrawlerAbstract):
    title = u'钨都网 - 每月报价'
    start_urls = [
        'http://www.tungstencity.com/index.php?m=content&c=index&a=lists&catid=16'
    ]
    url_links_selector = 'ul.liebwen li a'
    content_selector = dict(
        title='.xuqn h2',
        content='.xuqn .neir',
        date_area='.xuqn .shij'
    )






