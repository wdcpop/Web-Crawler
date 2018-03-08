# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/24 17:35


import re
from arrow import Arrow
from spider import Spider

__name__ = '财新网'


class Caixin(Spider):
    def __init__(self):
        super(Caixin, self).__init__()
        self.start_urls = [
            "http://mappv4.caixin.com/channel/list_lastnew_20_1.json"
        ]
        self.category = ['companies', 'economy', 'finance', 'china', 'international']

    def run(self):
        for url in self.start_urls:
            r = self.s.get(url)
            url_details = []
            for item in r.json().get('data'):
                url = item.get('web_article_url')
                if url is None:
                    url = item.get('web_url')
                    if url is None:
                        url = item.get('from_web_url')
                for name in self.category:
                    if name in url:
                        url_details.append(url)
            if not url_details:
                raise Exception('{0} 找不到详情页链接!'.format(__name__))
            for url_detail in url_details:
                self.parse(url_detail)
        return self.result

    def parse(self, url):
        if self.check_bloomfilter(url): return
        r_detail = self.s.get(url)
        r_detail.encoding = 'utf8'
        p = self.pq(r_detail.text)

        title = p('h1').text()
        content = p('#Main_Content_Val').text()
        src_time = 0
        if content=='':
            self.blf.insert(url)
            return
        try:
            time_str = p('#pubtime_baidu').text()
            time_str = re.findall(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', time_str)[0]
            src_time = Arrow.strptime(time_str.encode('utf8'), '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
        except IndexError:
            pass
        name=__name__
        if 'companies' in url:
            name+='-公司频道'
        elif 'pmi' in url:
            name += '-财新PMI频道'
        elif 'finance' in url:
            name += '-金融频道'
        elif 'international' in url:
            name += '-世界频道'
        elif 'china' in url:
            name += '-政经频道'
        elif 'economy' in url:
            name += '-经济频道'
        self.addresult(
            name=name,
            title=title,
            content=content,
            link=url,
            time=src_time
        )
