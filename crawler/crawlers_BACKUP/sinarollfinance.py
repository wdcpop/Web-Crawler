#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SINAROLLFINANCE(CrawlerAbstract):
    title = u'新浪财经 - 财经滚动'
    start_urls = [
        'http://roll.finance.sina.com.cn/s/channel.php?ch=03'
    ]
    url_links_selector = '#d_list .c_tit a'
    content_selector = dict(
        title='#artibodyTitle',
        content='.article, #artibody',
        date_area='.time-source, #pub_date'
    )



