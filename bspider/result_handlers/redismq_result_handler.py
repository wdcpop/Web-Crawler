#!/usr/bin/env python
# coding:utf8

from .basic_result_handler import BasicResultHandler


class RedisMQResultHandler(BasicResultHandler):
    def on_new_result(self, result):
        pass