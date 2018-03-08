#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.4.8"
3.4 遇到一些问题，于 4.8 号解决。
这里遇到的问题是 跨域请求时候， headers 中的 Host 不断变化的问题，需要针对
不同的访问，选择合适的 Host
3.4 遇到问题，大概是忽略了更换 Host 的问题
'''
import requests
import re
import json
import base64
import time
import math
import random
from PIL import Image
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

'''
3.4
所有的请求都分析的好了
模拟请求 一直不成功
在考虑是哪里出了问题
以后学了新的知识后 再来更新
'''

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
global headers
headers = {
    "Host": "passport.weibo.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': agent
}

proxy_list = [
    "reg:noxqofb0@61.158.163.86:16816",
    "reg:noxqofb0@120.24.68.197:16816",
    "reg:noxqofb0@112.74.206.133:16816",
    "reg:noxqofb0@120.26.167.133:16816",
    "reg:noxqofb0@115.28.102.240:16816",
    "reg:noxqofb0@27.54.242.222:16816",
    "reg:noxqofb0@110.76.185.162:16816",
    "reg:noxqofb0@114.215.140.117:16816",
    "reg:noxqofb0@122.114.137.18:16816",
    "reg:noxqofb0@120.26.160.155:16816"
]

p = random.choice(proxy_list)

session = requests.session()

# 访问登录的初始页面
index_url = "https://passport.weibo.cn/signin/login"
session.get(index_url, headers=headers)


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def login_pre(username):
    # 采用构造参数的方式
    params = {
        "checkpin": "1",
        "entry": "mweibo",
        "su": get_su(username),
        "callback": "jsonpcallback" + str(int(time.time() * 1000) + math.floor(random.random() * 100000))
    }
    '''真是日了狗，下面的这个写成 session.get(login_pre_url，headers=headers) 404 错误
        这条 3.4 号的注释信息，一定是忽略了 host 的变化，真是逗比。
    '''
    pre_url = "https://login.sina.com.cn/sso/prelogin.php"
    headers["Host"] = "login.sina.com.cn"
    headers["Referer"] = index_url
    pre = session.get(pre_url, params=params, headers=headers)
    print(pre.text)
    # pa = r'\((.*?)\)'
    # res = re.findall(pa, pre.text)
    res = [pre.text]
    if res == []:
        print("好像哪里不对了哦，请检查下你的网络，或者你的账号输入是否正常")
    else:
        js = json.loads(res[0])
        if js["showpin"] == 1:
            headers["Host"] = "passport.weibo.cn"
            capt = session.get("https://passport.weibo.cn/captcha/image", headers=headers)
            capt_json = capt.json()
            capt_base64 = capt_json['data']['image'].split("base64,")[1]
            print(capt_base64)
            with open('capt.jpg', 'wb') as f:
                f.write(base64.b64decode(capt_base64))
                f.close()
            im = Image.open("capt.jpg")
            im.show()
            im.close()
            cha_code = raw_input("请输入验证码\n>")
            return cha_code, capt_json['data']['pcid']
        else:
            return ""


def login(username, password, pincode):
    postdata = {
        "username": username,
        "password": password,
        "savestate": "1",
        "ec": "0",
        "pagerefer": "http%3A%2F%2Fpassport.sina.cn%2Fsso%2Flogout%3Fentry%3Dmweibo%26r%3Dhttp%253A%252F%252Fm.weibo.cn",
        "entry": "mweibo",
        "wentry": "",
        "loginfrom": "",
        "client_id": "",
        "code": "",
        "qq": "",
        "hff": "",
        "hfp": "",
    }
    print pincode
    if pincode == "":
        pass
    else:
        postdata["pincode"] = pincode[0]
        postdata["pcid"] = pincode[1]
    headers = {
        'Host': 'passport.weibo.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Content-Length': '236',
        'Connection': 'keep-alive',
    }
    # headers["Host"] = "passport.weibo.cn"
    # headers["Reference"] = index_url
    # headers["Origin"] = "https://passport.weibo.cn"
    # headers["Content-Type"] = "application/x-www-form-urlencoded"

    post_url = "https://passport.weibo.cn/sso/login"
    login = session.post(post_url, data=postdata, headers=headers)
    # print(login.cookies)
    # print(login.status_code)
    js = login.json()
    print(js)
    uid = js["data"]["uid"]
    crossdomain = js["data"]["crossdomainlist"]
    cn = "https:" + crossdomain["sina.com.cn"]
    # 下面两个对应不同的登录 weibo.com 还是 m.weibo.cn
    # 一定要注意更改 Host
    # mcn = "https:" + crossdomain["weibo.cn"]
    # com = "https:" + crossdomain['weibo.com']
    headers["Host"] = "login.sina.com.cn"
    session.get(cn, headers=headers)
    headers["Host"] = "weibo.cn"
    ht = session.get("http://weibo.cn/%s/info" % uid, headers=headers)
    # print(ht.url)
    # print(session.cookies)
    pa = r'<title>(.*?)</title>'
    res = re.findall(pa, ht.text)
    print(u"你好%s，你正在使用 xchaoinfo 写的模拟登录" % res[0])
    # print(cn, com, mcn)
    return session


if __name__ == "__main__":

    username = "你的用户名"
    password = "你的密码"
    pincode = login_pre(username)
    login(username, password, pincode)