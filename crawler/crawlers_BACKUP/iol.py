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


class IOL(CrawlerAbstract):
    title = u'产业在线 - 行业资讯'
    start_urls = [
        'http://www.chinaiol.com/comm/list.aspx?no-cache=0.3383590013792066&SiteID=0&ClassID=872458136042&LoginP=CH&ListOnly=true&TemplatePath=0iunm0Ufnqmfut0ofxt%60mjtu%2fiunm&page=1&_='
    ]
    url_patterns = [
        re.compile(r'"(http://.*?\.chinaiol\.com.*?/q/\d{4}/\d+?\.html)"')
    ]
    content_selector = dict(
        title='.leftlist1_1',
        content='#newsbody',
        date_area='.leftlist1_2'
    )





