#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 * User: liuyang
 * Email:sleshep@gmail.com 
 * Date: 16-3-17 
 * Time: 上午10:42 
"""
import pymongo
from redis import StrictRedis,ConnectionPool
from werkzeug.contrib.fixers import ProxyFix
from view.api import bpApi
def config_app(app):
    """
    :type app: flask.Flask
    """
    # if socket.gethostname() != 'Ubuntu':
    #     app.config.from_pyfile('config/config.pub.py')
    # else:
    app.config.from_pyfile('config/config.dev.py')
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.register_blueprint(bpApi)


def init_redis(app):
    # type: (Flask) -> sqlalchemy.orm
    # engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # db = scoped_session(sessionmaker(autocommit=True,
    #                                  autoflush=False,
    #                                  bind=engine))
    from lib.helper import app_config
    redis = StrictRedis(connection_pool=ConnectionPool())
    db = pymongo.MongoClient(app_config['MONGODB_TO_STORE_RESULT']['HOST'])
    maindb = db[app_config['MONGODB_TO_STORE_RESULT']['MAINDB']]
    app.redis = redis
    app.db = db
    app.maindb = maindb
    return redis

