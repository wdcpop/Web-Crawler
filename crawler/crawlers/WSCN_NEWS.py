# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

from .abstracts.crawler_abstract import CrawlerAbstract

class WSCN_NEWS(CrawlerAbstract):

    def index_page(self, response):
        res_list = []
        detail_lists = self.get_detail_url_and_title_list(response)

        for detail in detail_lists:
            if self.deduplicator.is_url_recorded(detail.get('content')):
                continue

            labels = self.get_labels(detail.get('title'), detail.get('content'))

            res_list.append({
                "acknowledged": True,
                "link": detail.get('url'),
                "title": detail.get('content'),
                "content": detail.get('content'),
                "labels": labels
            })

            self.deduplicator.record_url_good(detail.get('content'))

        return res_list

    def get_detail_url_and_title_list(self, response):
        details = []
        url_links_selector = self.single_config.get('url_links_selector', '')
        if url_links_selector:
            for link in response.doc(url_links_selector).items():
                details.append(dict(url=u"qucik_news_does_not_have_url", content=link.text(), title=u'华尔街见闻快讯'))
        return details


