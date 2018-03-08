# coding=utf-8

import requests

global_config={
    'order_id':'936588863967175',
    'auth_name':'reg',
    'auth_passwd':'noxqofb0'
}

def get_proxy_urls(config=None):
    if config is None:
        config=global_config
    proxy_api = 'http://ent.kuaidaili.com/api/getproxy?orderid=%s&num=100&kps=1&format=json'%(config['order_id'])
    data = requests.get(proxy_api).json()
    proxy_list = data['data']['proxy_list']
    healthy_proxy_list=[]
    for proxy_item in proxy_list:
        proxy_url='http://%s:%s@%s'%(config['auth_name'],config['auth_passwd'],proxy_item)
        params={
            'proxies':{'http':proxy_url},
            'headers':{'User-Agent': 'curl/'}
        }
        resp = requests.get('http://www.ip.cn',**params)
        if resp.status_code==200:
            healthy_proxy_list.append(proxy_url)
    return healthy_proxy_list


proxy_list=get_proxy_urls()