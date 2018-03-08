#!/usr/bin/env python
# coding:utf8
"""
作者:刘洋
邮箱:liuyang@wallscreetcn.com
微信:475090118
时间:16-5-8
"""
import hashlib

import sys


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


def to_unicode(string, encoding='utf-8'):
    """
    将字符串转换为Unicode
    :param string: 待转换字符串
    :param encoding: 字符串解码方式
    :return: 转换后的Unicode字符串
    """
    if isinstance(string, str):
        return string.decode(encoding)
    elif isinstance(string, unicode):
        return string
    else:
        raise Exception('Unknown Type')


class BloomFilter(object):
    def __init__(self, redis):
        self.bit_size = 2 ** 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.r = redis
        self.hashFunc = []
        for i in range(self.seeds.__len__()):
            self.hashFunc.append(SimpleHash(self.bit_size, self.seeds[i]))

    def exsits(self, value, name):
        if value is None:
            return False
        if value.__len__() == 0:
            return False
        ret = True
        hashs = hashlib.md5(value.encode('utf-8')).hexdigest()
        for f in self.hashFunc:
            loc = f.hash(hashs)
            ret = ret & self.r.getbit(name, loc)
        return ret

    def insert(self, value, name):
        if 'test' in sys.argv:
            return
        hashs = hashlib.md5(value.encode('utf-8')).hexdigest()
        for f in self.hashFunc:
            loc = f.hash(hashs)
            self.r.setbit(name, loc, 1)


if __name__ == '__main__':
    from redis import StrictRedis, ConnectionPool

    bf = BloomFilter(StrictRedis(connection_pool=ConnectionPool()))
    # for i in xrange(0,1000000,100):
    #     bf.insert(str(i),'test')
    for i in xrange(0, 10000, 100):
        if not bf.exsits(str(i), 'test'):
            print i
