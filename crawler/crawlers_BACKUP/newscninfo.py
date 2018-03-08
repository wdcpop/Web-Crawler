#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class NEWSCNINFO(CrawlerAbstract):
    use_link_content_as_detail_title = True
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Cookie': 'refreshedTimestamp=1486455712363; com.trs.idm.coSessionId=c0a8011030d751fb300d38ae40e7a0a1e8baf7bb60f5; JSESSIONID=c0a8011030d751fb300d38ae40e7a0a1e8baf7bb60f5.e34QaxaObhuMby0Mb390'
    }
    start_urls = [
        'http://info.xinhua.org/cn/outline.do?date=null&cid=37&ps=30&dt=0&lev=2&dm=0&pn=1',
        'http://info.xinhua.org/cn/outline.do?date=null&cid=66695&ps=30&dt=0&lev=2&dm=0&pn=1',
    ]
    url_links_selector = '.gailan:lt(20)'
    content_selector = dict(
        title='.detail_til',
        content='.detail_center',
        date_area='#detail_date'
    )