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
    def get_datestr_and_dateint(self, datestr_area):
        time_str = re.match(ur'(\d{4})年 (\d{1,2})月 (\d{1,2})日.+?(\d{2}):(\d{2})', datestr_area).groups()
        time_str = map(int, time_str)
        src_time = Arrow.now().replace(year=time_str[0], month=time_str[1], day=time_str[2], hour=time_str[3],
                                       minute=time_str[4], second=0).timestamp
        return dict(
            datestr=datestr_area,
            dateint=src_time
        )


