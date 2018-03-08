#!/usr/bin/env python
# coding:utf8
import sys
import inspect

import logging

import re
import six
from arrow import Arrow
from requests.models import RequestEncodingMixin
from six import iteritems

_encode_params = RequestEncodingMixin._encode_params

from bspider.lib.url import _build_url, quote_chinese
from bspider.lib.response import rebuild_response
from bspider.lib.utils import md5string


class BasicCrawler(object):
    fetch_fields = ('method', 'headers', 'data', 'connect_timeout', 'timeout', 'allow_redirects', 'cookies',
                    'proxy', 'etag', 'last_modifed', 'last_modified', 'save', 'js_run_at', 'js_script',
                    'js_viewport_width', 'js_viewport_height', 'load_images', 'fetch_type', 'use_gzip', 'validate_cert',
                    'max_redirects', 'robots_txt', 'anti_duplicate')

    def __init__(self, deduplicator=None, to_save=None):
        self.deduplicator = deduplicator
        self.to_save = to_save if to_save else {}
        self.setLogger()
        self.project_name = None
        self._follows = []
        self._follows_keys = set()

    def cleanup(self):
        self.project_name = None
        self._follows = []
        self._follows_keys = set()

    def setLogger(self, name='bspider'):
        self.logger = logging.getLogger(name)

    def _run_func(self, function, *arguments):
        """
        Running callback function with requested number of arguments
        """
        args, varargs, keywords, defaults = inspect.getargspec(function)
        return function(*arguments[:len(args) - 1])

    def _run_task(self, task, response):
        """
        Finding callback specified by `task['callback']`
        raising status error for it if needed.
        """
        callback = task.get('next_func', '__call__')
        if not hasattr(self, callback):
            raise NotImplementedError("self.%s() not implemented!" % callback)

        function = getattr(self, callback)
        if response and response.status_code == 304:  # do not run_func when 304
            return None

        return self._run_func(function, response, task)

    def run_task(self, task, response=None):
        """
        Processing the task, catching exceptions and logs, return a `ProcessorResult` object
        """
        if isinstance(response, dict):
            response = rebuild_response(response)

        returned_results = None
        self._follows = []

        error_info = ''
        try:
            returned_results = self._run_task(task, response)
            if returned_results:
                if inspect.isgenerator(returned_results):
                    for r in returned_results:
                        self._run_func(self.on_result, r, response, task)
                else:
                    self._run_func(self.on_result, returned_results, response, task)
        except Exception as e:
            self.logger.exception(e)
            error_info = str(e)
        finally:
            following_tasks = self._follows

        return following_tasks, returned_results, error_info

    def _crawl(self, url, **kwargs):
        """
        real crawl API
        """
        task = {}

        assert len(url) < 1024, "Maximum (1024) URL length error."

        # func = None
        # callback = None
        # if kwargs.get('callback'):
        #     callback = kwargs['callback']
        #     if isinstance(callback, six.string_types) and hasattr(self, callback):
        #         func = getattr(self, callback)
        #     elif six.callable(callback) and six.get_method_self(callback) is self:
        #         func = callback
        #     else:
        #         raise NotImplementedError("self.%s() not implemented!" % callback)

        task['url'] = url
        task['next_func'] = kwargs.get('callback')

        if kwargs.get('anti_duplicate'):
            task['anti_duplicate'] = True
        else:
            task['anti_duplicate'] = False

        task['project'] = self.project_name
        task['taskid'] = self.get_taskid(task)

        fetch = {}
        for key in self.fetch_fields:
            if key in kwargs:
                fetch[key] = kwargs.pop(key)
        task['fetch'] = fetch

        cache_key = "%(project)s:%(taskid)s" % task
        if cache_key not in self._follows_keys:
            self._follows_keys.add(cache_key)
            self._follows.append(task)

        return

    def get_taskid(self, task):
        '''Generate taskid by information of task md5(url) by default, override me'''
        return md5string(task['url'])

    def crawl(self, url, **kwargs):
        '''
        available params:
          url
          callback

          method
          params
          data
          files
          headers
          timeout

          proxy
        '''
        if isinstance(url, six.string_types):
            return self._crawl(url, **kwargs)
        elif hasattr(url, "__iter__"):
            result = []
            for each in url:
                result.append(self._crawl(each, **kwargs))
            return result

    def on_start(self):
        raise NotImplementedError("on_start not implemented!")

    def on_result(self, result, response, task):
        """Receiving returns from other callback, override me."""
        if not result:
            return
