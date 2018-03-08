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


class XBXGX(CrawlerAbstract):
    title = u'西本新干线 - 炉料点评,钢厂调价'
    start_urls = [
        'http://www.96369.net/news/list/15/18',
        'http://www.96369.net/news/list/14/13'
    ]
    url_patterns = [
        re.compile(r'"(/news/\d{3}/\d{6}\.html)"')
    ]
    content_selector = dict(
        title='.wll-new-detail > h2',
        content='.wll-new-detail .cont-msg',
        date_area='.wll-new-detail > h6'
    )




