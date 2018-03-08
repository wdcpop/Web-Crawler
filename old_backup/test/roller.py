#! /usr/bin/python
# coding:utf-8

import imp
import arrow
import time
import traceback

class SpiderRoller(object):

    def __init__(self):
        self._spiders=[]
    
    def _hook_parse(self,old_parse,url,urls):
        if url in urls:
            return
        old_parse(url)
        urls.add(url)
    
    def _setup_spider(self,spider):
        urls=set()
        old_parse=spider.parse
        spider.parse=lambda url:self._hook_parse(old_parse,url,urls)
    
    def add(self,spider):
        self._setup_spider(spider)
        self._spiders.append(spider)

    def run(self,run_once=False):
        while True:
            for spider in self._spiders:
                start_time=arrow.utcnow().to('+0800')
                try:
                    items=spider.run()
                except:
                    traceback.print_exc()
                    items=spider.result
                if hasattr(spider,'after_test'):
                    spider.after_test()
                if items:
                    spider.log('start spider at [%s]'%(start_time.format('YYYY-MM-DD HH:mm:ss')))
                    for item in items:
                        name=item['name']
                        title=item['title']
                        spider.log('get page with type [%s] and title [%s]'%(name.decode('utf-8'),title))
                    end_time=arrow.utcnow().to('+0800')
                    spider.log('end spider at [%s]'%(end_time.format('YYYY-MM-DD HH:mm:ss')))
                    spider.clear()
            if run_once:
                break
            time.sleep(20)

def check_spider(spider_name):
    if not spider_name:
        return None
    try:
        imp_info=imp.find_module(spider_name,['spiders'])
    except:
        imp_info=None
    if not imp_info:
        imp_info=imp.find_module(spider_name,['/root/gitwork/NewsCrawler/spiders'])
        if not imp_info:
            return None
        print('### Spider from NewsCrawler ###')
    else:
        print('### Spider from Kitchen ###')
    module=imp.load_module('',*imp_info)
    #print(module)
    symbols=dir(module)
    spider_cls=None
    for symbol in symbols:
        #print(spider_name,symbol)
        if symbol.lower()==spider_name.lower():
            spider_cls=getattr(module,symbol)
            break
    return spider_cls
            
if __name__=='__main__':
    import sys,getopt
    loop_run=False
    proxy_enabled=False
    spider_name=''
    opts,args=getopt.getopt(sys.argv[1:],'s:lp')
    for key,val in opts:
        if key=='-l':
            loop_run=True
        elif key=='-p':
            proxy_enabled=True
        elif key=='-s':
            spider_name=val
    spider_cls=check_spider(spider_name)
    if not spider_cls:
        print('spider not found or empty spider name')
        sys.exit(0)
    #print(spider)
    roller=SpiderRoller()
    spider=spider_cls()
    if proxy_enabled:
        spider.set_proxy('socks5://192.168.11.55:1234')
    roller.add(spider)
    roller.run(not loop_run)
            
            
            
    