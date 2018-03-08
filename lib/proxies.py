# coding=utf-8

import requests

global_config = {
    'order_id': '936588863967175',
    'auth_name': 'reg',
    'auth_passwd': 'noxqofb0'
}

proxy_list_cache = [
    "61.158.163.86:16816",
    "120.24.68.197:16816",
    "112.74.206.133:16816",
    "120.26.167.133:16816",
    "115.28.102.240:16816",
    "27.54.242.222:16816",
    "110.76.185.162:16816",
    "114.215.140.117:16816",
    "122.114.137.18:16816",
    "120.26.160.155:16816"
]


def get_proxy_urls(config=None):
    if config is None:
        config = global_config
    # try:
    #     proxy_api = 'http://ent.kuaidaili.com/api/getproxy?orderid=%s&num=100&kps=1&format=json' % (config['order_id'])
    #     data = requests.get(proxy_api, timeout=5).json()
    #     proxy_list = data['data']['proxy_list']
    # except:
    proxy_list = proxy_list_cache

    healthy_proxy_list = []
    for proxy_item in proxy_list:
        proxy_url = 'http://%s:%s@%s' % (config['auth_name'], config['auth_passwd'], proxy_item)
        # params = {
        #     'proxies': {'http': proxy_url},
        #     'headers': {'User-Agent': 'curl/'}
        # }
        # resp = requests.get('http://www.ip.cn', **params)
        if True:  # resp.status_code == 200
            healthy_proxy_list.append(proxy_url)
    return healthy_proxy_list


proxy_list = get_proxy_urls()
