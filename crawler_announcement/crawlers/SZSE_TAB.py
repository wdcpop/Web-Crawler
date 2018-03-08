#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .abstracts.crawler_abstract import CrawlerAbstract

import re


class SZSE_TAB(CrawlerAbstract):
    use_link_content_as_detail_title = True
    start_urls = [
        "http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=main_wxhj&tab1PAGENO=1&TABKEY=tab1",
        "http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=main_wxhj&tab1PAGENO=1&TABKEY=tab2",
        "http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=main_wxhj&tab1PAGENO=1&TABKEY=tab3",
        "http://www.szse.cn/main/disclosure/jgxxgk/jgcs/"
    ]

    def get_detail_url_and_title_list(self, response):
        details = []
        for link in response.doc(".cls-data-table-common tr").items():
            # 　第一栏是标题框  跳过
            if link.find('th'):
                continue

            url_PDF = "Url Not Found"
            columns = list(link.find("td").items())
            title = ' '.join([columns[1].text(), columns[2].text(), columns[3].text()])
            # print 'title', title
            patternPDF = re.compile(ur"Component\(.(.*?).\)")
            patternPath = re.compile(ur"window.open\(.(.*?).\+encode")
            searchPDF = patternPDF.search(link.__str__())
            searchPath = patternPath.search(link.__str__())
            if searchPath and searchPDF:
                url_PDF = ''.join(["http://www.szse.cn", searchPath.group(1), searchPDF.group(1)])
            details.append(dict(url=url_PDF, content=title))
        # print len(details)
        return details



