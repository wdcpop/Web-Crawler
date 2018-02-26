#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import signal
from arrow import Arrow
import logging

from bspider.crawlers.basic_crawler import BasicCrawler
import re
import json
import random
import requests
from lxml import etree
import lxml.html
from urlparse import urljoin
from urlparse import urlsplit
from arrow import Arrow
import time
from redis import StrictRedis, ConnectionPool
from bspider.lib.response import rebuild_response
from urlparse import urljoin
from urlparse import urlsplit
from urlparse import urlparse

import lxml.html
from lxml import etree
from lxml.etree import HTMLParser
from snownlp import SnowNLP

from lib.helper import app_config


time_formats = [
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2})'),
        '%Y年%m月%d日 %H:%M'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2})'),
        '%Y年%m月%d日%H:%M'
    ),
    (
        re.compile(ur'(\d{1,2}月\d{1,2}日\d{2}:\d{2})'),
        '%m月%d日%H:%M'
    ),
    (
        re.compile(ur'(\d{1,2}月\d{1,2}日\s\d{2}:\d{2})'),
        '%m月%d日 %H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}\.\d{1,2}\.\d{1,2}\s\d{2}:\d{2}:\d{2})'),
        '%Y.%m.%d %H:%M:%S'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2})'),
        '%Y-%m-%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}/\d{1,2}/\d{1,2}\s\d{2}:\d{2})'),
        '%Y/%m/%d %H:%M'
    ),
    (
        re.compile(ur'(\d{4}-\d{1,2}-\d{1,2})'),
        '%Y-%m-%d'
    ),
    (
        re.compile(ur'(\d{4}/\d{1,2}/\d{1,2})'),
        '%Y/%m/%d'
    ),
    (
        re.compile(ur'(\d{1,2}/\d{1,2}/\d{4})'),
        '%m/%d/%Y'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}年\d{1,2}月\d{1,2}日)'),
        '%Y年%m月%d日'
    ),
    (
        re.compile(ur'(\d{4}\d{2}\d{2})'),
        '%Y%m%d'
    ),
    (
        re.compile(ur'(\S+\s\d{1,2},\s\d{4})'),
        '%b %d, %Y'
    )

]


def get_one_proxy(proxy_type=1):
    redis = StrictRedis(host='127.0.0.1', port=6379)

    proxy_list = [
        "http://reg:noxqofb0@61.158.163.86:16816"
    ]

    if proxy_type == -1:   # No need for proxy
        return None

    if proxy_type == 1:   # Visite Chinese website
        pass
    elif proxy_type == 2:  # Visite foreign websites from China
        l = redis.get('kuaidaili_foreign_proxy_list') or '[]'
        proxy_list = json.loads(l)
    elif proxy_type == 99:  # testing
        return "http://xduotai.com/wallstreet.pac"
    else:
        pass

    if not proxy_list:
        return None

    return random.choice(proxy_list)

class CrawlerAbstract(BasicCrawler):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}
    timeout = 10

    preset_content_selector = {
        'CNR': dict(
            title='h2:first',
            content='.articleMain',
            date_area='.source'
        ),
        'MONEY163': dict(
            title='h1, .ep-h1, .con1_ltle',
            content='.post_text',
            date_area='.post_time_source, .ep-time-soure, .con1_date'
        ),
        'PBC': dict(
            title='title',
            content='.content',
            date_area='#shijian'
        ),
        'CAIXIN': dict(
            title='h1',
            content='#Main_Content_Val',
            date_area='#pubtime_baidu'
        )
    }

    def on_start(self):
        self.index_res = None
        self.index_url_list = []
        self.detail_res = []
        self.return_items = []
        self.is_backend_render = None

        single_config = self.single_config = self.to_save.get('config', {})
        self.actual_proxy = get_one_proxy(single_config.get('proxy_type', 1))
        start_urls = single_config .get('start_urls')
        if not start_urls:
            self.logger.error('URL is empty ....')
            return
        is_backend_render = single_config.get('is_backend_render', True)
        start_urls = self.start_urls_hook(start_urls)
        for url in start_urls:
            if is_backend_render:
                self.crawl(url, callback='index_page', headers=self.single_config.get('headers', self.headers), timeout=self.timeout,
                           proxy=self.actual_proxy, method=single_config.get('method', 'GET'), data=single_config.get('data', None))

            else:  # Else, Use web_kit
                # self.single_config['use_link_content_as_detail_title'] = True
                response = self.frontend_render_fetch(url, {})
                self.index_page(response)

    #headless browser to crawl JS rendered webpage
    def frontend_render_fetch(self, url, save=None):
        driver = None
        try:
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys

            driver = webdriver.PhantomJS()
            driver.set_window_size(1280, 720)
            driver.set_page_load_timeout(30)
            driver.get(url)
            content = driver.page_source
            driver.close()
            driver.service.process.send_signal(signal.SIGTERM)
            driver.quit()
        except Exception as e:
            self.logger.exception(e)
            content = 'PAGE RENDER ERROR!'
            if driver:
                driver.close()
                driver.service.process.send_signal(signal.SIGTERM)
                driver.quit()

        result = {}
        result['orig_url'] = url
        result['content'] = content
        result['headers'] = self.single_config.get('headers', self.headers)
        result['status_code'] = ''
        result['url'] = url
        result['time'] = ''
        result['cookies'] = None
        result['save'] = save if save else {}
        response = rebuild_response(result)
        return response

    def index_page(self, response):
        # print 'index page resonse', response.text
        self.index_res = response
        details = self.get_detail_url_and_title_list(response)
        for detail in details:
            url_origin = detail.get('url')
            url = urljoin(response.url, url_origin)
            self.index_url_list.append(detail.get('url'))

        details = self.details_hook(details)

        detailed_res_list = []
        for detail in details:
            url_origin = detail.get('url')
            url = urljoin(response.url, url_origin)

            self.crawl(url,
                       callback='detail_page',
                       anti_duplicate=True,
                       headers=self.single_config.get('headers', self.headers),
                       timeout=self.timeout,
                       save={'link_content': detail.get('content')},
                       proxy=self.actual_proxy)

        return detailed_res_list

    def get_detail_url_and_title_list(self, response):
        url_patterns = self.single_config.get('url_patterns', [])
        url_links_selector = self.single_config.get('url_links_selector', '')
        url_area_selector = self.single_config.get('url_area_selector', '')
        details = []
        if not url_patterns and not url_links_selector:
            return []

        if url_patterns:
            if url_area_selector:
                area_html = response.doc(url_area_selector).html()
            else:
                area_html = response.text

            if area_html:
                for url_patt_str in url_patterns:
                    url_patt = re.compile(url_patt_str)
                    for m in url_patt.finditer(area_html):
                        try:
                            found = m.group(1)
                        except IndexError as e:
                            # 有的正则匹配没有用括号
                            found = m.group(0)
                        right_part_html = area_html[m.start():]
                        content_found_all = re.match(r'.*?>(.*?)</a>', right_part_html)
                        content_found = content_found_all.group(1) if content_found_all else ''

                        details.append(dict(url=self.detail_url_hook(found), content=content_found))

        if url_links_selector:
            if url_links_selector.startswith('/'):
                parser = HTMLParser()
                doc = etree.fromstring(response.text, parser)
                elem1 = doc.xpath(url_links_selector)
                for url in elem1:
                    details.append(dict(url=self.detail_url_hook(url.attrib.get('href')), content=url.text))
            else:
                for link in response.doc(url_links_selector).items():
                    # print 'link', link
                    # print 'href', link.attr('href')
                    # print 'link content', link.text()
                    details.append(dict(url=self.detail_url_hook(link.attr('href')), content=link.text()))

        return details

    def detail_page(self, response):
        if not self.single_config.get('is_backend_render', True):
            response = self.frontend_render_fetch(response.url)

        if self.single_config.get('removing_style_and_script', True):
            response.doc('script').remove()
            response.doc('style').remove()

        title = self.get_title(response)
        content = self.get_content(response)
        date_area = self.get_date_area(response)
        dt_dict = self.get_datestr_and_dateint(date_area) if date_area else {}
        datestr = dt_dict.get('datestr')
        dateint = dt_dict.get('dateint')

        labels = self.get_labels(title, content)

        res = {
            "acknowledged": True,
            "link": response.url,
            "host": "{0.netloc}".format(urlsplit(response.url)),
            "title": title if not self.single_config.get('use_link_content_as_detail_title', False) else response.save.get('link_content'),
            "time_human": datestr,
            "time": dateint,
            "ctime": int(time.time()),
            "content": content,
            "labels": labels,
        }
        res['title'] = self.to_simplified_chinese(res['title'])
        res['content'] = self.to_simplified_chinese(res['content'])
        res['title'] = self.fullshape_to_halfshape(res['title'])
        res['content'] = self.fullshape_to_halfshape(res['content'])

        res = self.result_hook(res, response)
        self.return_items.append(res)
        return res

    def start_urls_hook(self, urls):
        return urls

    def details_hook(self, details):
        return details

    def fullshape_to_halfshape(self, input_text):
        return self.strQ2B(input_text) if input_text else ''

    def to_simplified_chinese(self, input_text):
        """繁体转简体"""
        if not input_text:
            return ''
        if u'平治' in input_text:
            return input_text
        Simplified_res = SnowNLP(u'{}'.format(input_text))
        return Simplified_res.han if Simplified_res else ''



    def strQ2B(self, ustring):
        rep = {
            u'１': u'1',
            u'２': u'2',
            u'３': u'3',
            u'４': u'4',
            u'５': u'5',
            u'６': u'6',
            u'７': u'7',
            u'８': u'8',
            u'９': u'9',
            u'０': u'0',
            u'．': u'.',
            u'Ａ': u'A',
            u'Ｂ': u'B',
            u'Ｃ': u'C',
            u'Ｄ': u'D',
            u'Ｅ': u'E',
            u'Ｆ': u'F',
            u'Ｇ': u'G',
            u'Ｈ': u'H',
            u'Ｉ': u'I',
            u'Ｊ': u'J',
            u'Ｋ': u'K',
            u'Ｌ': u'L',
            u'Ｍ': u'M',
            u'Ｎ': u'N',
            u'Ｏ': u'O',
            u'Ｐ': u'P',
            u'Ｑ': u'Q',
            u'Ｒ': u'R',
            u'Ｓ': u'S',
            u'Ｔ': u'T',
            u'Ｕ': u'U',
            u'Ｖ': u'V',
            u'Ｗ': u'W',
            u'Ｘ': u'X',
            u'Ｙ': u'Y',
            u'Ｚ': u'Z',
            u'ａ': u'a',
            u'ｂ': u'b',
            u'ｃ': u'c',
            u'ｄ': u'd',
            u'ｅ': u'e',
            u'ｆ': u'f',
            u'ｇ': u'g',
            u'ｈ': u'h',
            u'ｉ': u'i',
            u'ｊ': u'j',
            u'ｋ': u'k',
            u'ｌ': u'l',
            u'ｍ': u'm',
            u'ｎ': u'n',
            u'ｏ': u'o',
            u'ｐ': u'p',
            u'ｑ': u'q',
            u'ｒ': u'r',
            u'ｓ': u's',
            u'ｔ': u't',
            u'ｕ': u'u',
            u'ｖ': u'v',
            u'ｗ': u'w',
            u'ｘ': u'x',
            u'ｙ': u'y',
            u'ｚ': u'z',
            u'馀': u'余',
            u'％': u'%',
            u'／': u'/',
            u'＼': u'\\',
            u'复甦': u'复苏',
            u'佔比': u'占比'

        }

        rstring = ""
        for uchar in ustring:
            if uchar in rep:
                uchar = rep[uchar]

            rstring += uchar

        return rstring


    def result_hook(self, res, response):
        return res

    def detail_url_hook(self, url):
        return url

    def get_title(self, response):
        content_selector = self.single_config.get('content_selector', {})
        if not content_selector.get('title'):
            return ''
        if content_selector.get('title').startswith('/'):
            parser = HTMLParser()
            doc = etree.fromstring(response.text, parser)
            elem1 = doc.xpath(content_selector.get('title'))
            return elem1[0].text if elem1 else ''

        else:
            return response.doc(content_selector.get('title')).text()

    def get_content(self, response):
        # print 'response in the detail page', response.text
        # print ''
        content_selector = self.single_config.get('content_selector', {})
        if not content_selector.get('content'):
            return ''
        if content_selector.get('content').startswith('/'):
            parser = HTMLParser()
            doc = etree.fromstring(response.text, parser)
            elem1 = doc.xpath(content_selector.get('content'))
            return "<br>".join([_.text for _ in elem1 if _.text])

        else:
            doc = response.doc(content_selector.get('content'))

        def cleanhtml(doc):
            # self_closing_tags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta',
            #                      'param', 'source', 'track', 'wbr']

            self_closing_tags = ['area', 'base', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta',
                                 'param', 'source', 'track', 'wbr']

            text = []

            def add_text(tag, no_tail=False):
                # print ''
                # print 'tag', tag
                # print 'tag.tag', tag.tag
                # print 'tag.text', tag.text
                # print 'tag.tail', tag.tail
                # print ''
                if tag.tag in self_closing_tags:
                    text.append(lxml.etree.tostring(tag, pretty_print=True))
                else:
                    if not isinstance(tag, lxml.etree._Comment):
                        text.append(u'<%s>' % tag.tag)
                        if tag.text:
                            text.append(tag.text)
                        for child in tag.getchildren():
                            add_text(child)
                        text.append(u'</%s>' % tag.tag)
                if not no_tail and tag.tail:
                    text.append(tag.tail)

            for tag in doc:
                add_text(tag, no_tail=True)

            return ''.join([t.strip() for t in text if t.strip()])

        # for test
        # doc = PyQuery('<div>123<img src="1"/><!-- asdasd -->imgtail<p>content1</p><p>content2</p><br><br><p>content3</p><div>some adds</div></div>')

        if len(doc) > 1:
            res = u''.join([cleanhtml(d) for d in doc.items()])
        else:
            res = cleanhtml(doc)

        return res

    def get_date_area(self, response):
        content_selector = self.single_config.get('content_selector')

        if not content_selector.get('date_area'):
            return ''

        if content_selector.get('date_area').startswith('/'):
            parser = HTMLParser()
            doc = etree.fromstring(response.text, parser)
            elem1 = doc.xpath(content_selector.get('date_area'))
            return elem1[0].text if elem1 else ''

        else:
            return response.doc(content_selector.get('date_area')).text()


    def get_datestr_and_dateint(self, datestr_area):
        rt = dict(
            datestr='',
            dateint=0
        )
        if isinstance(datestr_area, unicode) or isinstance(datestr_area, str):
            for time_re, arrow_fmt in time_formats:
                findall = time_re.findall(datestr_area)
                if findall:
                    ar = Arrow.strptime(findall[0].encode('utf8'), arrow_fmt, 'Asia/Shanghai')
                    if ar.year < 2000:
                        ar = ar.replace(year=Arrow.now().datetime.year)
                    rt = dict(
                        datestr=findall[0],
                        dateint=ar.timestamp
                    )
                    break
        return rt

    def get_labels(self, title, content):
        labels = []

        if not title and not content:
            return labels

        try:
            headers = {
                'content-type': "application/json",
                'x-api-token': app_config['EDITORAI_TOKEN'],
            }

            r = requests.post(app_config['EDITORAI_API'] + '/api/v1/article_analyze',
                              headers=headers,
                              json={"title": title, "body": content},
                              timeout=5)
            result = r.json()
            labels = result.get('labels')
        except Exception as e:
            print(e)

        return labels
