#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time


class HKSE(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        'http://www.hkexnews.hk/listedco/listconews/mainindex/sehk_listedco_datetime_today_c.htm',
    ]
    url_links_selector = ".row0 , .row1"

    name_pool = [
                u'中國恒大', u'中國恆大', u'騰訊控股', u'吉利汽車', u'阿里健康', u'美圖公司', u'國美電器', u'復星國際', u'中國海洋石油', u'中國電信',
                u'中國聯通',u'中國移動', u'阿里影業', u'融創中國', u'萬科企業', u'碧桂園', u'蒙牛乳業', u'酷派集團', u'輝山乳業',
                u'首都機場', u'中國宏橋',  u'漢能薄膜發電', u'中國神華'
                 ]


    def get_detail_url_and_title_list(self, response):
        details = []
        if not self.url_links_selector:
            return []

        for link in response.doc(self.url_links_selector).items():
            company_name = link.find('nobr').text()
            if company_name in self.name_pool:
                details.append(dict(url=self.detail_url_hook(link.find('a').attr('href')), content=' : '.join([
                    company_name, link.find('a').text()])))
        return details

