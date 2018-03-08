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


class MIITOPINION(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://zmhd.miit.gov.cn:8080/opinion/notice.do?method=new_notice&pgSize=10',
    ]
    url_links_selector = 'a'
    content_selector = dict(
        title='',
        content='',
        date_area=''
    )

    def detail_url_hook(self, url):
        return re.sub(re.compile(r";jsessionid=.+?\?"), '?', url)


