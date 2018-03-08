#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-17
"""
from gevent.monkey import patch_all

patch_all()
import json
import os
from time import sleep
from arrow import Arrow
from bson import ObjectId
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from pymongo import MongoClient
from redis import StrictRedis, ConnectionPool
from lib.helper import app_config

db = MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'])
maindb = db[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
redis = StrictRedis(connection_pool=ConnectionPool())


class Server(object):
    def __init__(self, env, resp):
        ws = env['wsgi.websocket']  # type:WebSocket
        self.current_filter_list = []
        if os.path.exists('newsweb/filter.json'):
            with open('newsweb/filter.json', 'r')as f:
                self.current_filter_list = json.load(f)
        # else:
        #     print 'filter Not Exist'
        #     exit()
        self.is_important = 'important' in ws.receive()
        self.handle(ws)

    def handle(self, ws):
        """
        :type ws: WebSocket
        """
        self.send_init_news(ws)
        sub = redis.pubsub()
        sub.subscribe(['news_updated','crawled','ann_news_updated','weibo_news_updated'])
        self.send_real_time_news_loop(sub, ws)

    def send_real_time_news_loop(self, sub, ws):
        while 1:
            data = sub.get_message(timeout=30)
            resp = dict()
            if ws.closed: break
            if not data or data['type'] == 'subscribe':
                resp['code'] = 0
                ws.send(json.dumps(resp))
                continue
            if data['channel']=='news_updated':
                updated_news_id = data['data']
                resp['code'] = 201
                result = map(self.parse_item,
                             [dict(i, **{'id': updated_news_id}) for i in
                              maindb['items'].find({'_id': ObjectId(updated_news_id)}, {'_id': 0})])
                resp['results'] = filter(self.filter_news, result)
            if data['channel']=='crawled':
                resp['code']=202
                resp['results']=json.loads(data['data'])

            if data['channel']=='ann_news_updated':
                updated_news_id = data['data']
                resp['code'] = 211
                result = map(self.parse_item,
                             [dict(i, **{'id': updated_news_id}) for i in
                              maindb['ann_items'].find({'_id': ObjectId(updated_news_id)}, {'_id': 0})])
                resp['results'] = filter(self.filter_news, result)

            if data['channel']=='weibo_news_updated':
                updated_news_id = data['data']
                resp['code'] = 221
                result = map(self.parse_item,
                             [dict(i, **{'id': updated_news_id}) for i in
                              maindb['weibo_items'].find({'_id': ObjectId(updated_news_id)}, {'_id': 0})])
                resp['results'] = filter(self.filter_news, result)

            ws.send(json.dumps(resp))

    def filter_news(self, item):
        ret = True
        # if not self.is_important:
        #     ret = True
        # if item['name'] in self.current_filter_list:
        #     ret = True
        # print u'{}-{}-{}-'.format(ret,item['name'],self.current_filter_list).encode('utf8')
        return ret

    def send_init_news(self, ws):
        sleep(1)
        init_num = 100 if not self.is_important else 100
        resp = {'code': 200, 'results': self.getnews(init_num, 1, sort=[('ctime', -1)])}
        ws.send(json.dumps(resp))
        news = self.getnews(1, init_num, sort=[('ctime', -1)])[::-1]
        news = filter(self.filter_news, news)
        for i in news:
            resp = {'code': 201, 'results': [i]}
            ws.send(json.dumps(resp))
            # sleep(0.015)

    @staticmethod
    def parse_item(news):
        if not news.get('ctime') or not isinstance(news['ctime'], int):
            news['ctime'] = 0
        if not news.get('time') or not isinstance(news.get('time'), int):
            news['time'] = 0
        ctime_formatted = Arrow.fromtimestamp(news['ctime']).to('Asia/Shanghai')
        news['ctime_formatted'] = ctime_formatted.format(u'YYYY年MM月DD日HH:mm:ss') + '<br>'
        if news.get('time'):
            insert_time = Arrow.fromtimestamp(news['time']).to('Asia/Shanghai')
            news['time_formatted'] = insert_time.format(u'YYYY年MM月DD日HH:mm:ss') + u'    爬虫抓取时间差:' + insert_time.humanize(ctime_formatted,
                                                                                                               locale='zh_cn').replace(
                u'前', '')
        news['content_formatted'] = news.get('content', '').replace(u'。', u'。<br>')
        return news

    def getnews(self, skip, limit, sort):
        items = maindb['items'].find({}, {'_id': 0}).sort(sort).skip(skip).limit(limit)
        items=map(self.parse_item, items)
        if limit==1:print items
        return items


if __name__ == '__main__':
    WSGIServer(('', 8000), Server, handler_class=WebSocketHandler).serve_forever()
