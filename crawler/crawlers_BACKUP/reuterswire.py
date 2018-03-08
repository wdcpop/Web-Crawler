#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
import xmltodict
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class REUTERSWIRE(CrawlerAbstract):
    title = u'路透中文 - 实时资讯'
    start_urls = [
        'http://cn.reuters.com/assets/jsonWireNews?limit=20',
    ]
    url_patterns = [
        re.compile(r'"(/article/\S+?)"')
    ]
    content_selector = dict(
        title='h1',
        content='#article-text',
        date_area='.timestamp'
    )
    def get_datestr_and_dateint(self, datestr_area):
        time_str = re.match(ur'(\d{4})年 (\d{1,2})月 (\d{1,2})日.+?(\d{2}):(\d{2})', datestr_area).groups()
        time_str = map(int, time_str)
        src_time = Arrow.now().replace(year=time_str[0], month=time_str[1], day=time_str[2], hour=time_str[3],
                                       minute=time_str[4], second=0).timestamp
        return dict(
            datestr=datestr_area,
            dateint=src_time
        )


