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


class TRONOX(CrawlerAbstract):
    start_urls = [
        'http://investor.tronox.com/releases.cfm',
    ]
    url_links_selector = 'table.wsh-releases tr td:eq(2) a'
    content_selector = dict(
        title='h1',
        content='#ndq-releasebody',
        date_area='.ndq-leftcol'
    )





