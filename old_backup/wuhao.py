#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-8-5
"""

from gevent.monkey import patch_all

patch_all()
import json,gevent,requests
from bson import ObjectId
from redis import StrictRedis
from pymongo import MongoClient
wuhao_redis_conf = dict(
    host='dac323f856954562.m.cnhza.kvstore.aliyuncs.com',
    password='Baofeed0314',
    db=0
)
wuhao_redis_conf2 = dict(
    host='121.41.77.236',
    password='baoer1234',
    db=0
)
print 'started'
redis = StrictRedis()
redis1 = StrictRedis(**wuhao_redis_conf)
redis2 = StrictRedis(**wuhao_redis_conf2)
db=MongoClient()
items=db['content']['items']
print 'init finished'

def send_new(data):
    """

    :type data: pymongo.cursor.Cursor
    """
    code1=redis1.lpush('mq:news',json.dumps(data))
    code2=redis2.lpush('mq:news',json.dumps(data))
    print 'success ',code1,code2

def main():
    sub=redis.pubsub()
    sub.subscribe(['news_updated'])
    for data in sub.listen():
        if not data or data['type'] == 'subscribe':
            continue
        let=gevent.spawn(send_new,items.find_one({'_id': ObjectId(data['data'])}, {'_id': 0}))
        gevent.wait([let],5)
        if not let.dead:
            requests.post('http://120.26.69.90/api/wx/msg',
                          data=dict(
                              source='news redis push -xuan gu bao',
                              msg='Send to Wuhao Time spend more than 5s'
                          ))
if __name__ == '__main__':

    main()
