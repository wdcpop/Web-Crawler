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


class GMWFINANCE(CrawlerAbstract):
    title = u'光明网 - 金融滚动'
    start_urls = [
        'http://finance.gmw.cn/node_70075.htm',
    ]
    url_area_selector = '.channelLeftPart'
    url_patterns = [
        re.compile(r'"(http://finance\.gmw\.cn/\d{4}-\d{2}/\d{2}/content_\d{8}.htm)"')
    ]
    content_selector = dict(
        title='h1',
        content='#contentMain',
        date_area='#contentMsg'
    )





