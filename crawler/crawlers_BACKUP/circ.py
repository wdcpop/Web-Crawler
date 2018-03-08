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


class CIRC(CrawlerAbstract):
    title = u'保监会 - 新闻发布'
    start_urls = [
        'http://www.circ.gov.cn/web/site0/tab5207/',
    ]
    url_patterns = [
        re.compile(r'"(/web/site0/tab5207/info\d{7}.htm)"')
    ]
    content_selector = dict(
        title='#tab_content > tbody > tr:eq(0) > td',
        content='#tab_content tr:eq(3)',
        date_area='#ess_mailrightpane'
    )




