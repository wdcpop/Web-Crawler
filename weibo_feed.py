#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-7-13
"""
import json

import requests
import pymongo
import time
import datetime
import random
from iceutils import SmartLogger
from user_agent import generate_user_agent

log=SmartLogger(10,__name__)

class WeiboSpider():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.conn = pymongo.MongoClient()
        self.db = self.conn.content

    def login(self):
        # session = requests.Session()
        url_login = r"https://passport.weibo.cn/sso/login"
        headers = {
            "User-Agent"     : generate_user_agent(),
            "Referer"        : "https://passport.weibo.cn/signin/login",
        }
        postdata = {
            "username" : self.username,
            "password" : self.password,
        }
        resp = self.session.post(
                url_login,
                data=postdata,
                headers=headers
        )
        return resp



    def get_news(self):

        result = self.session.get("http://m.weibo.cn/index/feed?format=cards").json()
        if isinstance(result, dict):
            if result['msg'] == u"请先登录":
                self.login()

        for obj_arr in result[0]['card_group']:
            item = {}

            obj = obj_arr['mblog']

            item["name"] = obj['user']['screen_name']
            item["title"] = obj['user']['screen_name']
            item["source"] = u"微博"
            item["content"] = obj['text']
            item["host"] = "m.weibo.cn"
            item["coll"] = "item_weibo"
            item["link"] = "weibo_" + str(obj['id'])
            item["insert_time"] = datetime.datetime.utcnow()
            log.debug(json.dumps(obj,ensure_ascii=False,indent=4))


def main():
    weibo = WeiboSpider("zhoujiyuan@wallstreetcn.com", "haoren123456")
    weibo.login()
    while True:
        try:
            weibo.get_news()
        except Exception:
            log.exception('getInfo Error')

        time.sleep(random.randint(30, 50))


if __name__ == '__main__':
    main()
