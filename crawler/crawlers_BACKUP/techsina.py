#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class TECHSINA(CrawlerAbstract):
    # fetch_configs = dict(
    #     headers={'Referer': 'http://roll.tech.sina.com.cn/s/channel.php?ch=05'}
    # )
    start_urls = [
        'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=30&spec=&type=&date=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=1',
    ]
    url_patterns = [
        re.compile(ur'(http://tech\.sina\.com\.cn/i/\d{4}-\d{2}-\d{2}/doc-.+?\.shtml)')
    ]
    content_selector = dict(
        title='h1',
        content='.content, #artibody',
        date_area='.titer, #pub_date'
    )




