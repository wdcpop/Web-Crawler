#!/usr/bin/env python
# coding:utf8
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import arrow
from gevent import monkey

monkey.patch_all()
from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_cors import CORS, cross_origin

from util.getredis import get_collection
from util.config_app import config_app, init_redis

app = Flask(__name__)
CORS(app)
config_app(app)
init_redis(app)
application = app
PWD = 'wscnnews'

msg = [u'请点击左侧列表开始阅读',
       u'WebSocket实现,不会卡',
       u'如果有啥问题可以找刘洋,微信号13229607552</p>']


@app.route('/')
def index():
    return render_template(
            'index.html',
            title=u'光速小分队V0.1',
            msg=msg,
            active=0

    )


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.form.get('p') == PWD:
        resp = make_response(index())
        resp.set_cookie('pwd', PWD,None,arrow.utcnow().replace(months=1).datetime)
        return resp
    return render_template('login.html')


@app.before_request
def before():
    if request.cookies.get('pwd') != PWD and request.path != '/login/' and 'api' not in request.path:
        return redirect(url_for('login'))


@app.route('/news_important')
def news_important():
    return render_template('news_important.html',
                           title=u'光速小分队(重要版)V0.1',
                           msg=msg,
                           active=1,
                           )


@app.route('/wechat/')
def wechat():
    return render_template('wechat.html', title=u'微信新闻')


if __name__ == '__main__':
    app.run(port=8888)
