#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class SSE(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm',
    ]
    url_links_selector = '.modal_pdf_list dd a'





