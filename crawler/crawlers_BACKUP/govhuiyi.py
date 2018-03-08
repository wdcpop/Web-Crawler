#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class GOVHUIYI(CrawlerAbstract):
    title = u'中国政府 - 国务院会议'
    start_urls = [
        'http://www.gov.cn/guowuyuan/gwy_cwh.htm',
    ]
    url_patterns = [
        re.compile('"(http://www\.gov\.cn/guowuyuan/gwycwhy/\S+?/.*?)"'),
    ]
    content_selector = dict(
        title='h2:eq(0)',
        content='h3',
        date_area='.top_date'
    )



