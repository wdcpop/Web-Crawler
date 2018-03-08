#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract


class TTTC(CrawlerAbstract):
    def get_detail_url_and_title_list(self, response):
        url_details = [dict(
            url=_.get("SourceUrl"), content=_.get('Title')) for _ in response.json['Datas']]

        return url_details


