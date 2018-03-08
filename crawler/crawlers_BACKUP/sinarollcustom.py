#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SINAROLLCUSTOM(CrawlerAbstract):
    title = u'新浪财经 - 滚动自选'
    start_urls = [
        'http://roll.news.sina.com.cn/s/channel.php?ch=01#col=96,97,98&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=4'
    ]
    url_patterns = [
        re.compile(r'(http://.*?\.sina\.com\.cn/[\w/]+?/\d{4}-\d{2}-\d{2}/doc-\w+?\.shtml)')
    ]
    content_selector = dict(
        title='#artibodyTitle',
        content='.article, #artibody',
        date_area='.time-source, #pub_date'
    )



