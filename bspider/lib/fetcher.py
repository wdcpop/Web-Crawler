#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

logger = logging.getLogger('bspider')
import requests
import time
import tornado.ioloop
import tornado.httputil
import tornado.httpclient

import six
import copy
from six.moves import queue, http_cookies
from six.moves.urllib.robotparser import RobotFileParser
from requests import cookies
from six.moves.urllib.parse import urljoin, urlsplit
from tornado import httpclient, gen, ioloop, queues
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
import pycurl

import utils
from .cookie_utils import extract_cookies_to_jar
from .url import quote_chinese


class MyCurlAsyncHTTPClient(CurlAsyncHTTPClient):

    def free_size(self):
        return len(self._free_list)

    def size(self):
        return len(self._curls) - self.free_size()


class MySimpleAsyncHTTPClient(SimpleAsyncHTTPClient):

    def free_size(self):
        return self.max_clients - self.size()

    def size(self):
        return len(self.active)


class Fetcher(object):
    user_agent = "bspider/0.1 (+http://xuangubao.cn/)"
    default_options = {
        'method': 'GET',
        'headers': {
        },
        'use_gzip': True,
        'timeout': 30,
        'connect_timeout': 10,
    }

    def __init__(self, inqueue, outqueue, poolsize=100, **kwargs):
        self.inqueue = inqueue
        self.outqueue = outqueue

        self.poolsize = poolsize
        # self.proxyer = kwargs.get('proxyer')
        self.ioloop = tornado.ioloop.IOLoop.current()

        self._quit = False
        self._running = False

        # binding io_loop to http_client here
        # self.http_client = tornado.httpclient.HTTPClient(MyCurlAsyncHTTPClient, max_clients=self.poolsize)
        self.http_client = CurlAsyncHTTPClient()

        # self.ioloop.start()

    def sync_fetch(self, task, callback=None):
        self.ioloop.add_callback(self.fetch, task, callback)

    def pack_tornado_request_parameters(self, url, task):
        fetch = copy.deepcopy(self.default_options)
        fetch['url'] = url
        fetch['headers'] = tornado.httputil.HTTPHeaders(fetch['headers'])
        fetch['headers']['User-Agent'] = self.user_agent
        task_fetch = task.get('fetch', {})
        for each in self.allowed_options:
            if each in task_fetch:
                fetch[each] = task_fetch[each]
        fetch['headers'].update(task_fetch.get('headers', {}))

        if task.get('track'):
            track_headers = tornado.httputil.HTTPHeaders(
                task.get('track', {}).get('fetch', {}).get('headers') or {})
            track_ok = task.get('track', {}).get('process', {}).get('ok', False)
        else:
            track_headers = {}
            track_ok = False
        # proxy
        proxy_string = None
        if isinstance(task_fetch.get('proxy'), six.string_types):
            proxy_string = task_fetch['proxy']

        if proxy_string:
            if '://' not in proxy_string:
                proxy_string = 'http://' + proxy_string
            if 'socks5://' in proxy_string:
                def prepare_curl_socks5(curl):
                    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
                fetch['prepare_curl_callback'] = prepare_curl_socks5

            proxy_splited = urlsplit(proxy_string)
            fetch['proxy_host'] = proxy_splited.hostname
            if proxy_splited.username:
                fetch['proxy_username'] = proxy_splited.username
            if proxy_splited.password:
                fetch['proxy_password'] = proxy_splited.password
            if six.PY2:
                for key in ('proxy_host', 'proxy_username', 'proxy_password'):
                    if key in fetch:
                        fetch[key] = fetch[key].encode('utf8')
            fetch['proxy_port'] = proxy_splited.port or 8080

        # etag
        if task_fetch.get('etag', True):
            _t = None
            if isinstance(task_fetch.get('etag'), six.string_types):
                _t = task_fetch.get('etag')
            elif track_ok:
                _t = track_headers.get('etag')
            if _t and 'If-None-Match' not in fetch['headers']:
                fetch['headers']['If-None-Match'] = _t
        # last modifed
        if task_fetch.get('last_modified', task_fetch.get('last_modifed', True)):
            last_modified = task_fetch.get('last_modified', task_fetch.get('last_modifed', True))
            _t = None
            if isinstance(last_modified, six.string_types):
                _t = last_modified
            elif track_ok:
                _t = track_headers.get('last-modified')
            if _t and 'If-Modified-Since' not in fetch['headers']:
                fetch['headers']['If-Modified-Since'] = _t
        # timeout
        if 'timeout' in fetch:
            fetch['request_timeout'] = fetch['timeout']
            del fetch['timeout']
        # data rename to body
        if 'data' in fetch:
            fetch['body'] = fetch['data']
            del fetch['data']

        return fetch

    @gen.coroutine
    def fetch(self, task, callback=None):
        handle_error = lambda x: self.handle_error('http', url, task, start_time, x)
        start_time = time.time()

        url = task.get('url')
        fetch = self.pack_tornado_request_parameters(url, task)

        # requests.Session().proxies.update({
        #     'http': 'socks5://127.0.0.1:49999',
        #     'https': 'socks5://127.0.0.1:49999'
        # })
        # print fetch
        try:
            request = tornado.httpclient.HTTPRequest(**fetch)
        except Exception as e:
            logger.exception(fetch)
            raise gen.Return(handle_error(e))

        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            logger.exception(fetch)
            raise gen.Return(handle_error(e))

        result = {}
        result['orig_url'] = url
        result['content'] = response.body or ''
        result['headers'] = dict(response.headers)
        result['status_code'] = response.code
        result['url'] = response.effective_url or url
        result['time'] = time.time() - start_time
        result['cookies'] = None
        result['save'] = task.get('fetch', {}).get('save')

        raise gen.Return(result)

    @gen.coroutine
    def async_fetch(self, task):
        '''Do one fetch'''
        start_time = time.time()
        url = task.get('url', 'data:,')

        type = 'None'
        print url
        print 'fetching3...'
        try:
            if url.startswith('data:'):
                type = 'data'
                # result = yield gen.maybe_future(self.data_fetch(url, task))
            elif task.get('fetch', {}).get('fetch_type') in ('js', 'phantomjs'):
                type = 'phantomjs'
                # result = yield self.phantomjs_fetch(url, task)
            else:
                type = 'http'
                result = yield self.http_fetch(url, task)
        except Exception as e:
            print 'fetching err...'
            print str(e)
            logger.exception(e)
            result = self.handle_error(type, url, task, start_time, e)

        print 'fetching 4...'
        raise gen.Return(result)

    @gen.coroutine
    def http_fetch(self, url, task):
        '''HTTP fetcher'''
        start_time = time.time()
        handle_error = lambda x: self.handle_error('http', url, task, start_time, x)

        # setup request parameters
        fetch = self.pack_tornado_request_parameters(url, task)
        task_fetch = task.get('fetch', {})

        session = cookies.RequestsCookieJar()
        # fix for tornado request obj
        if 'Cookie' in fetch['headers']:
            c = http_cookies.SimpleCookie()
            try:
                c.load(fetch['headers']['Cookie'])
            except AttributeError:
                c.load(utils.utf8(fetch['headers']['Cookie']))
            for key in c:
                session.set(key, c[key])
            del fetch['headers']['Cookie']
        if 'cookies' in fetch:
            session.update(fetch['cookies'])
            del fetch['cookies']

        max_redirects = task_fetch.get('max_redirects', 5)
        # we will handle redirects by hand to capture cookies
        fetch['follow_redirects'] = False

        # making requests
        while True:
            # robots.txt
            # if task_fetch.get('robots_txt', False):
            #     can_fetch = yield self.can_fetch(fetch['headers']['User-Agent'], fetch['url'])
            #     if not can_fetch:
            #         error = tornado.httpclient.HTTPError(403, 'Disallowed by robots.txt')
            #         raise gen.Return(handle_error(error))

            try:
                request = tornado.httpclient.HTTPRequest(**fetch)
                # if cookie already in header, get_cookie_header wouldn't work
                old_cookie_header = request.headers.get('Cookie')
                if old_cookie_header:
                    del request.headers['Cookie']
                cookie_header = cookies.get_cookie_header(session, request)
                if cookie_header:
                    request.headers['Cookie'] = cookie_header
                elif old_cookie_header:
                    request.headers['Cookie'] = old_cookie_header
            except Exception as e:
                logger.exception(fetch)
                raise gen.Return(handle_error(e))

            try:
                response = yield self.http_client.fetch(request)
            except tornado.httpclient.HTTPError as e:
                if e.response:
                    response = e.response
                else:
                    raise gen.Return(handle_error(e))

            extract_cookies_to_jar(session, response.request, response.headers)
            if (response.code in (301, 302, 303, 307)
                and response.headers.get('Location')
                and task_fetch.get('allow_redirects', True)):
                if max_redirects <= 0:
                    error = tornado.httpclient.HTTPError(
                        599, 'Maximum (%d) redirects followed' % task_fetch.get('max_redirects', 5),
                        response)
                    raise gen.Return(handle_error(error))
                if response.code in (302, 303):
                    fetch['method'] = 'GET'
                    if 'body' in fetch:
                        del fetch['body']
                fetch['url'] = quote_chinese(urljoin(fetch['url'], response.headers['Location']))
                fetch['request_timeout'] -= time.time() - start_time
                if fetch['request_timeout'] < 0:
                    fetch['request_timeout'] = 0.1
                max_redirects -= 1
                continue

            result = {}
            result['orig_url'] = url
            result['content'] = response.body or ''
            result['headers'] = dict(response.headers)
            result['status_code'] = response.code
            result['url'] = response.effective_url or url
            result['time'] = time.time() - start_time
            result['cookies'] = session.get_dict()
            result['save'] = task_fetch.get('save')
            if response.error:
                result['error'] = utils.text(response.error)
            if 200 <= response.code < 300:
                logger.info("[%d] %s:%s %s %.2fs", response.code,
                            task.get('project'), task.get('taskid'),
                            url, result['time'])
            else:
                logger.warning("[%d] %s:%s %s %.2fs", response.code,
                               task.get('project'), task.get('taskid'),
                               url, result['time'])

            raise gen.Return(result)

    allowed_options = ['method', 'data', 'timeout', 'cookies', 'use_gzip', 'validate_cert']


    def run(self):
        '''Run loop'''
        logger.info("fetcher starting...")

        def queue_loop():
            if not self.outqueue or not self.inqueue:
                return
            while not self._quit:
                try:
                    if self.outqueue.full():
                        break
                    if self.http_client.free_size() <= 0:
                        break
                    task = self.inqueue.get_nowait()
                    # FIXME: decode unicode_obj should used after data selete from
                    # database, it's used here for performance
                    task = utils.decode_unicode_obj(task)
                    self.fetch(task)
                except queue.Empty:
                    break
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.exception(e)
                    break

        tornado.ioloop.PeriodicCallback(queue_loop, 100, io_loop=self.ioloop).start()
        # tornado.ioloop.PeriodicCallback(self.clear_robot_txt_cache, 10000, io_loop=self.ioloop).start()
        self._running = True

        try:
            self.ioloop.start()
        except KeyboardInterrupt:
            pass

        logger.info("fetcher exiting...")

    def quit(self):
        '''Quit fetcher'''
        self._running = False
        self._quit = True
        self.ioloop.add_callback(self.ioloop.stop)

    def send_result(self, type, task, result):
        '''Send fetch result to processor'''
        if hasattr(self, 'outqueue') and self.outqueue:
            try:
                self.outqueue.put((task, result))
            except Exception as e:
                logger.exception(e)

    def on_result(self, type, task, result):
        '''Called after task fetched'''
        pass

    def handle_error(self, type, url, task, start_time, error):
        result = {
            'status_code': getattr(error, 'code', 599),
            'error': utils.text(error),
            'content': "",
            'time': time.time() - start_time,
            'orig_url': url,
            'url': url,
            "save": task.get('fetch', {}).get('save')
        }
        logger.error("[%d] %s:%s %s, %r %.2fs",
                     result['status_code'], task.get('project'), task.get('taskid'),
                     url, error, result['time'])
        return result
