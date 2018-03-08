#!/usr/bin/env python
# coding:utf8


class BasicResultHandler(object):
    def on_new_result(self, result):
        '''返回一个url的抓取结果(如果成功且为新)'''
        raise NotImplementedError('on_new_result must be implemented!')

    def on_new_results(self, results, total_time):
        '''返回一整次抓取的所有结果(仅返回成功且为新的结果)'''
        raise NotImplementedError('on_new_results must be implemented!')

    def on_strong_fetch_error(self, task):
        '''返回一个url的超过5次错误后的抓取结果'''
        raise NotImplementedError('on_strong_fetch_error must be implemented!')