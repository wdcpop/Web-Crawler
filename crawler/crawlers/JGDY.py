#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract


class JGDY(CrawlerAbstract):
    def index_page(self, response):
        res_list = []
        detail_lists = self.get_detail_url_and_title_list(response)

        for detail in detail_lists:
            if self.deduplicator.is_url_recorded(detail.get('url')):
                continue

            labels = self.get_labels(detail.get('url'), detail.get('content'))

            res_list.append({
                "acknowledged": True,
                "link": detail.get('url'),
                "title": detail.get('content'),
                "content": detail.get('content'),
                "labels": labels
            })

            self.deduplicator.record_url_good(detail.get('url'))

        return res_list


    def get_detail_url_and_title_list(self, response):
        url_details = [dict(
            url=u''.join([u'http://www.cninfo.com.cn/', _.get("s1")]), content=_.get('s2')) for _ in response.json['list']]
        print url_details
        return url_details


