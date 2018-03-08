# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract
import re
import json
import time


class KRNEWS(CrawlerAbstract):

    def index_page(self, response):
        res_list = []
        detail_lists = self.get_detail_url_and_title_list(response)

        for detail in detail_lists:
            if self.deduplicator.is_url_recorded(detail.get('title')):
                continue

            labels = self.get_labels(detail.get('title'), detail.get('content'))

            date = self.get_datestr_and_dateint(detail.get('time')) or ''

            res_list.append({
                "acknowledged": True,
                "link": detail.get('url'),
                "title": detail.get('title'),
                "time_human": date.get('dateint'),
                "time": date.get('datestr'),
                "ctime": int(time.time()),
                "content": detail.get('content'),
                "labels": labels
            })

            self.deduplicator.record_url_good(detail.get('title'))

        return res_list


    def get_detail_url_and_title_list(self, response):
        details = []
        pattern = re.compile(ur"newsflashList\|newsflash.:(.*?),.hotPosts\|hotPost")
        search = pattern.search(response.text)
        if search:
            # print "search.group(1)", search.group(1)
            news_list = json.loads(search.group(1))
            for news in news_list:
                # print "news['description']", news['description']
                details.append(dict(
                    url=news['news_url'] if news['news_url'] else u'简讯不带有详情页链接',
                    title=news['title'],
                    content=news['description'],
                    time=news['published_at']
                ))
        return details

