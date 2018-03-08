#!/usr/bin/env python
# coding:utf8
"""
    code by liuyang@wallstreetcn.com
"""
from collections import Counter

from gevent import monkey
monkey.patch_all()
import json
import logging
import requests
from coloredlogs import install
from gevent.pool import Pool
import proxies

__author__ = 'liuyang@wallstreetcm.com'
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARN)
logging.basicConfig()
install()

proxy_list = proxies.proxy_list
proxy_list.extend(proxies.proxy_list_error)
proxy_list_error = []

good_proxy=[]
c=Counter()
def process_proxy(proxy_string):
    proxy_dict = {"http": proxy_string}
    try:
        r = requests.get('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json',
                         proxies=proxy_dict, timeout=5)
        res = json.loads(r.text)
        logger.info('%-20s %s %s %s' % (proxy_dict.get('http'), res['country'], res['province'], res['city']))
        good_proxy.append(proxy_string)
    except Exception as e:
        # proxy_list.remove(proxy_tuple)
        proxy_list_error.append(proxy_string)
        logger.error(proxy_string)


if __name__ == '__main__':
    p = Pool(64)

    for i in proxy_list:
        p.apply_async(process_proxy, (i,))
    p.join()
    good_proxy=list(set(good_proxy))
    proxy_list_error=list(set(proxy_list_error))
    with open('proxies.py', 'w') as f:
        f.write('proxy_list=')
        f.write(str(good_proxy))
        f.write('\r\nproxy_list_error=')
        f.write(str(proxy_list_error))
