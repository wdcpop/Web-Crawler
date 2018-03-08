#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
logger = logging.getLogger('bspider')

import hashlib
from .bloomfilter import BloomFilter


class Deduplicator(object):
    def __init__(self, redis=None, name_prefix='blf'):
        if not redis:
            logger.error(u'Deduplicator only support redis now! Please give a valid redis client instance!')
        self.redis = redis
        self.name_prefix = name_prefix
        self.good_pool_name = '%s_good' % self.name_prefix
        self.err_pool_name = '%s_err' % self.name_prefix
        self.blf = BloomFilter(redis)

    def record_url_good(self, url):
        '''记录成功抓取的url'''
        logger.debug(u'Recording url good: %s' % url)
        self.blf.insert(url, self.good_pool_name)

    def record_url_err(self, url):
        '''记录失败抓取的url'''
        logger.debug(u'Recording url err: %s' % url)
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()

        # 缓存记录错误, 超过5次录入blf
        num = self.redis.incr('%s_%s' % (self.err_pool_name, url_hash))
        if num > 5:
            self.redis.delete('%s_%s' % (self.err_pool_name, url_hash))
            self.blf.insert(url, self.err_pool_name)

    def is_url_recorded(self, url):
        return self.is_url_recorded_good_or_err_5times(url)

    def is_url_recorded_good_or_err_5times(self, url):
        '''判断url是否被成功抓取或失败抓取超过5次'''
        if self.blf.exsits(url, self.good_pool_name) or self.blf.exsits(url, self.err_pool_name):
            logger.debug(u'Url is recorded: %s' % url)
            return True
        logger.debug(u'Url is not recorded: %s' % url)
        return False

    def is_url_recorded_good(self, url):
        '''判断url是否被成功抓取'''
        if self.blf.exsits(url, self.good_pool_name):
            logger.debug(u'Url is recorded as GOOD: %s' % url)
            return True
        logger.debug(u'Url is not recorded: %s' % url)
        return False

    def is_url_recorded_err_5times(self, url):
        '''判断url是否被失败抓取超过5次'''
        if self.blf.exsits(url, self.err_pool_name):
            logger.debug(u'Url is recorded as ERROR: %s' % url)
            return True
        logger.debug(u'Url is not recorded as ERROR over 5 times: %s' % url)
        return False

