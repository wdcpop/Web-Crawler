#!/usr/bin/env python
#coding:utf8
from flask import current_app
from redis import StrictRedis


def get_redis():
    """

    :rtype: StrictRedis
    """
    return current_app.redis
def get_collection(name, db=None):
    """
    :rtype: pymongo.collection.Collection
    """
    if not db:
        return current_app.maindb[name]
    else:
        return current_app.db[db][name]




def get_message(sub,timeout=1):
    """

    :rtype: dict
    """
    msg=None
    while True:
        msg = sub.get_message(timeout=timeout)
        if msg is None or msg.get('type') == 'message':
            break
        else:
            continue
    return msg