#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""

import sys
import hashlib

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret
        
class BloomFilter(object):

    def __init__(self):
        self.bit_size = 2**25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.hashFunc = []
        for i in range(self.seeds.__len__()):
            self.hashFunc.append(SimpleHash(self.bit_size, self.seeds[i]))

    def check(self, value, name='bloomfilter_url'):
        if value is None:
            return False
        if value.__len__() == 0:
            return False
        ret = True
        hashs=hashlib.md5(value).hexdigest()
        locations=[]
        for f in self.hashFunc:
            locations.append(f.hash(hashs))
        return locations

if __name__=='__main__':
    filter=BloomFilter()
    result=filter.check('http://finance.caixin.com/2016-08-31/100983772.html')
    print(result)
