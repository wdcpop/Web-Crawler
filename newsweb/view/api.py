#!/usr/bin/env python
# coding:utf8
import json
import sys
import traceback

import os
import time
from arrow import Arrow
from flask import jsonify, request
from flask.blueprints import Blueprint
from flask import Response
from flask import current_app, send_from_directory
from bson.objectid import ObjectId
sys.path.append('/home/wdcpop/WALL/NewsCrawler/newsweb')
from util.getredis import get_collection, get_redis
from datetime import datetime
import hashlib
import re
import hashlib

from urlparse import urlsplit
from snownlp import SnowNLP

bpApi = Blueprint('api', __name__, url_prefix='/api')


def clean_id(obj):
    obj['id'] = str(obj['_id'])
    del obj['_id']
    return obj


def jsonp(ret):
    ret = json.dumps(ret)
    jsonp_callback = request.args.get('callback')
    if jsonp_callback:
        ret = '{0}({1});'.format(jsonp_callback, ret)

    return Response(ret, mimetype='application/json; charset=utf-8', headers={'Access-Control-Allow-Origin': '*'})


def filterFields(d, fields):
    return {k: v for k, v in d.items() if k in fields}


@bpApi.route('/names/', methods=['GET', 'POST'])
def names():
    items = get_collection('items')

    if request.method == 'GET':
        name_list = items.distinct('name')
        current = []
        if os.path.exists('filter.json'):
            with open('filter.json', 'r')as f:
                current = json.load(f)
        msgs = {}
        for name in name_list:
            item = [i for i in items.find({'name': name}, {'_id': 0}).sort([('ctime', -1)]).limit(1)]
            if item:
                item = item[0]
                last_time = Arrow.fromtimestamp(item['ctime']).to('Asia/Shanghai')
                msgs[name] = u'最后时间:{0}'.format(last_time.humanize(locale='zh_cn'))
                if (Arrow.utcnow() - last_time).days > 1:
                    msgs[name] = u'<span class="text-danger">{}</span>'.format(msgs[name])
        return jsonp({
            'all': name_list,
            'current': current,
            'msg': msgs
        })
    elif request.method == 'POST':
        code = 500
        if request.json:
            with open('filter.json', 'w')as f:
                f.write(json.dumps(request.json, ensure_ascii=False).encode('utf8'))
                code = 200
        return Response('', code)


@bpApi.route('/news/', methods=['GET'])
def news():
    items = get_collection('items')
    limit = request.args.get('limit', 1)
    skip = request.args.get('skip', 0)
    skip = skip if skip != 0 else request.args.get('offset', 0)  # allow another namespace 'offset'
    keyword = request.args.get('keyword', None)
    is_keyword_full = request.args.get('is_keyword_full', 0)
    startwith = request.args.get('startwith', None)
    coop = request.args.get('coop', None)

    source = request.args.get('source', None)
    source_keyword = request.args.get('source_keyword', None)
    sql_filter = {}
    if source:
        sql_filter.update({'source': source})

    if source_keyword:
        sql_filter.update({"name": {'$regex': source_keyword, '$options': 'i'}})

    if keyword:
        if int(json.loads(str(is_keyword_full))):  # is_keyword_full maybe "false" or "0"
            sql_filter.update({"title": keyword})
        else:
            sql_filter.update({"title": {'$regex': keyword, '$options': 'i'}})

    if startwith:
        sql_filter.update({'_id': {'$lte': ObjectId(startwith)}})

    if coop:
        sql_filter.update({'coops': coop})

    data = []
    data.extend([clean_id(i) for i in items
                .find(sql_filter)
                .sort([('_id', -1)])
                .skip(int(skip))
                .limit(int(limit))
                 ])
    ret = {
        'data': data,
        'total': items.find().count()
    }

    return jsonify(ret)


@bpApi.route('/stock/news/', methods=['GET'])
def stock_news():
    items = get_collection('gw_news', 'temp_spiders')
    limit = request.args.get('limit', 1)
    skip = request.args.get('skip', 0)
    skip = skip if skip != 0 else request.args.get('offset', 0)  # allow another namespace 'offset'
    keyword = request.args.get('keyword', None)
    is_keyword_full = request.args.get('is_keyword_full', 0)
    startwith = request.args.get('startwith', None)

    news_type = request.args.get('news_type', None)
    stock_id = request.args.get('stock_id', None)
    sql_filter = {}
    if news_type:
        sql_filter.update({'news_type': news_type})

    if stock_id:
        sql_filter.update({'stock_id': stock_id})

    if keyword:
        if int(json.loads(str(is_keyword_full))):  # is_keyword_full maybe "false" or "0"
            sql_filter.update({"title": keyword})
        else:
            sql_filter.update({"title": {'$regex': keyword, '$options': 'i'}})

    if startwith:
        sql_filter.update({'_id': {'$lte': ObjectId(startwith)}})

    data = []
    data.extend([clean_id(i) for i in items
                .find(sql_filter)
                .sort([('_id', -1)])
                .skip(int(skip))
                .limit(int(limit))
                 ])
    ret = {
        'data': data,
        'total': items.find().count()
    }

    return jsonify(ret)


@bpApi.route('/ann/news/', methods=['GET'])
def ann_news():
    items = get_collection('ann_items')
    limit = request.args.get('limit', 1)
    skip = request.args.get('skip', 0)
    skip = skip if skip != 0 else request.args.get('offset', 0)  # allow another namespace 'offset'
    keyword = request.args.get('keyword', None)
    is_keyword_full = request.args.get('is_keyword_full', 0)
    startwith = request.args.get('startwith', None)

    stock_id = request.args.get('stock_id', None)
    sql_filter = {}

    if stock_id:
        sql_filter.update({'stock_id': stock_id})

    if keyword:
        if int(json.loads(str(is_keyword_full))):  # is_keyword_full maybe "false" or "0"
            sql_filter.update({"title": keyword})
        else:
            sql_filter.update({"title": {'$regex': keyword, '$options': 'i'}})

    if startwith:
        sql_filter.update({'_id': {'$lte': ObjectId(startwith)}})

    data = []
    data.extend([clean_id(i) for i in items
                .find(sql_filter)
                .sort([('_id', -1)])
                .skip(int(skip))
                .limit(int(limit))
                 ])
    ret = {
        'data': data,
        'total': items.find().count()
    }

    return jsonify(ret)


@bpApi.route('/weibo/news/', methods=['GET'])
def weibo_news():
    items = get_collection('weibo_items')
    limit = request.args.get('limit', 1)
    skip = request.args.get('skip', 0)
    skip = skip if skip != 0 else request.args.get('offset', 0)  # allow another namespace 'offset'
    keyword = request.args.get('keyword', None)
    is_keyword_full = request.args.get('is_keyword_full', 0)
    startwith = request.args.get('startwith', None)

    sql_filter = {}

    if keyword:
        if int(json.loads(str(is_keyword_full))):  # is_keyword_full maybe "false" or "0"
            sql_filter.update({"title": keyword})
        else:
            sql_filter.update({"title": {'$regex': keyword, '$options': 'i'}})

    if startwith:
        sql_filter.update({'_id': {'$lte': ObjectId(startwith)}})

    data = []
    data.extend([clean_id(i) for i in items
                .find(sql_filter)
                .sort([('_id', -1)])
                .skip(int(skip))
                .limit(int(limit))
                 ])
    ret = {
        'data': data,
        'total': items.find().count()
    }

    return jsonify(ret)


@bpApi.route('/news2/', methods=['GET'])
def news2():
    items = get_collection('items')
    limit = request.args.get('limit', 1)
    skip = request.args.get('skip', 0)
    source = request.args.get('source', None)
    sql_filter = {}
    if source:
        sql_filter.update({'name': source})
    data = []
    data.extend([i for i in items.find(sql_filter, {'_id': 0}).sort([('ctime', -1)]).skip(int(skip)).limit(int(limit))])
    ret = {
        'results': data,
        'code': 0
    }
    return jsonp(ret)


# deprecated
def get_modules():
    items = get_collection('items')
    namelist = items.distinct('name')
    return namelist


# deprecated
@bpApi.route('/sourcelist/')
def sourcelist():
    keyword = request.args.get('keyword', None)
    return jsonify({'list': get_modules()})


@bpApi.route('/sources/')
def sources():
    sources = get_collection('sources')
    limit = request.args.get('limit', 50)
    skip = request.args.get('skip', 0)
    skip = skip if skip != 0 else request.args.get('offset', 0)  # allow another namespace 'offset'
    keyword = request.args.get('keyword', None)
    start_urls_keyword = request.args.get('start_urls_keyword', None)
    comment_keyword = request.args.get('comment_keyword', None)
    startwith = request.args.get('startwith', None)
    coop = request.args.get('coop', None)

    sql_filter = {}

    if keyword:
        sql_filter.update({"title": {'$regex': keyword, '$options': 'i'}})

    if start_urls_keyword:
        sql_filter.update({"start_urls": {'$regex': start_urls_keyword, '$options': 'i'}})

    if comment_keyword:
        sql_filter.update({"comments": {'$regex': comment_keyword, '$options': 'i'}})

    if startwith:
        sql_filter.update({'_id': {'$lte': ObjectId(startwith)}})

    if coop:
        sql_filter.update({'coops': coop})

    data = []
    data.extend([clean_id(i) for i in sources
                .find(sql_filter)
                .sort('machine_name', 1)
                .skip(int(skip))
                .limit(int(limit))
                 ])

    for d in data:
        if d.get('latestArticleCreated'):
            last_time = Arrow.fromtimestamp(d['latestArticleCreated']).to('Asia/Shanghai')
            d['latestArticleCreatedHuman'] = u'最后时间:{0}'.format(last_time.humanize(locale='zh_cn'))
            if (Arrow.utcnow() - last_time).days > 1:
                d['latestArticleCreatedHuman'] = u'<span class="text-danger">{}</span>'.format(d['latestArticleCreatedHuman'])

    ret = {
        'data': data,
        'total': sources.find().count()
    }
    return jsonify(ret)


@bpApi.route('/source_default/', methods=['GET'])
def sourcedefaultget():
    sources = get_collection('sourceDefaultConfigs')
    map = sources.find_one()
    clean_id(map)

    return jsonify(map)



@bpApi.route('/source_default/', methods=['PUT'])
def sourcedefaultedit():
    sources = get_collection('sourceDefaultConfigs')
    update = request.get_json(force=True)

    fieldsFilted = filterFields(update,
                                ['default_proxy', 'default_delay'])
    if not fieldsFilted:
        return jsonify({'is_success': True})

    fieldsToUpdate = fieldsFilted.copy()
    fieldsToUpdate.update({"last_modified": time.time()})

    result = sources.find_one_and_update({}, {'$set': fieldsToUpdate})
    is_success = True if result.get('_id') else False

    return jsonify({'is_success': is_success})


@bpApi.route('/source/', methods=['PUT'])
def sourceadd():

    sources = get_collection('sources')
    fieldsFromReq = request.get_json(force=True)

    fieldsFilted = filterFields(fieldsFromReq,
                                ['title', 'proxy_type', 'disabled', 'delay_sec', 'machine_name', 'comments', 'tags', 'star',
                                 'start_urls', 'is_backend_render', 'content_selector', 'removing_style_and_script',
                                 'use_link_content_as_detail_title', 'url_links_selector', 'url_area_selector',
                                 'url_patterns', 'headers', 'coops'])

    if not fieldsFilted:
        return jsonify({'json_is_success': True})

    fieldsForInsert = fieldsFilted.copy()
    fieldsForInsert.update({"first_created": time.time()})

    is_success = sources.insert_one(fieldsForInsert)

    return jsonify({'inserted_is_success': is_success.acknowledged})


@bpApi.route('/source/<sourceId>/', methods=['DELETE'])
def sourcedelete(sourceId):
    sources = get_collection('sources')
    is_success = sources.delete_one({'_id': ObjectId(sourceId)})

    return jsonify({'is_success': is_success.acknowledged})


@bpApi.route('/source/<sourceId>/', methods=['PUT'])
def sourceedit(sourceId):
    sources = get_collection('sources')
    update = request.get_json(force=True)

    fieldsFilted = filterFields(update,
                                ['title', 'proxy_type', 'disabled', 'delay_sec', 'machine_name', 'comments', 'tags', 'star',
                                 'start_urls', 'is_backend_render', 'content_selector', 'removing_style_and_script',
                                 'use_link_content_as_detail_title', 'url_links_selector', 'url_area_selector',
                                 'url_patterns', 'headers', 'coops'])
    if not fieldsFilted:
        return jsonify({'is_success': True})

    fieldsToUpdate = fieldsFilted.copy()
    fieldsToUpdate.update({"last_modified": time.time()})

    is_success = sources.update_one(
        {'_id': ObjectId(sourceId)},
        {'$set': fieldsToUpdate},
    )

    return jsonify({'is_success': is_success.acknowledged})


@bpApi.route('/news/bind_published_article/', methods=['PUT'])
def news_relate_article():
    news = get_collection('items')

    fields = request.get_json(force=True)
    newsId = fields.get('newsId', None)
    baoArticleId = fields.get('baoArticleId', None)
    publishedAt = fields.get('publishedAt', None)

    fieldsToUpdate = {
        'related_bao_article_id': baoArticleId,
        'related_bao_article_published': publishedAt,
    }
    fieldsToUpdate.update({"last_modified": time.time()})

    is_success = news.update_one(
        {'_id': ObjectId(newsId)},
        {'$set': fieldsToUpdate},
    )

    return jsonify({'is_success': is_success.acknowledged})


@bpApi.route('/source_testing/', methods=['POST'])
def source_testing():
    import requests
    from bspider.lib.response import rebuild_response
    from crawler.crawlers.abstracts.crawler_abstract import CrawlerAbstract

    input_info = request.get_json(force=True)
    try:

        class CrawlerAbstractForTesting(CrawlerAbstract):
            def crawl(self, url, **kwargs):
                callback = kwargs.get('callback')
                function = getattr(self, callback)
                is_backend_render = input_info.get('is_backend_render', True)
                if is_backend_render:
                    r = requests.get(url, proxies={"http": self.actual_proxy, "https": self.actual_proxy}, timeout=10)
                    result = {}
                    result['orig_url'] = url
                    result['content'] = r.content or ''
                    result['headers'] = dict(r.headers)
                    result['status_code'] = r.status_code
                    result['url'] = url
                    result['time'] = 0
                    result['cookies'] = None
                    result['save'] = kwargs.get('save')
                    response = rebuild_response(result)
                else:
                    response = self.frontend_render_fetch(url, kwargs.get('save'))

                self._run_func(function, response)


            def details_hook(self, details):
                return [details[0]] if details else []



        cb = CrawlerAbstractForTesting()
        cb.to_save = {'config': input_info}
        cb.on_start()
        data = {
            "index_url_list": cb.index_url_list,
            "content_dict": {
                "title": cb.return_items[0].get('title') if cb.return_items else '',
                "content": cb.return_items[0].get('content', '') if cb.return_items else '',
                'date' : cb.return_items[0].get('time', '') if cb.return_items else '',
            }
        }
        error = ''

    except Exception as e:
        traceback.print_exc()
        data = ''
        error = str(e)


    return jsonify({'data': data, 'error' : error})


@bpApi.route('/crawler/reload/', methods=['GET'])
def crawler_reload():
    r = get_redis()
    r.publish('crawler_signals', 'reload')

    return jsonify({'is_success': True})


@bpApi.route('/crawler/stop/', methods=['GET'])
def crawler_stop():
    r = get_redis()
    r.publish('crawler_signals', 'stop')

    return jsonify({'is_success': True})


@bpApi.route('/crawler/start/', methods=['GET'])
def crawler_start():
    r = get_redis()
    r.publish('crawler_signals', 'start')

    return jsonify({'is_success': True})


@bpApi.route('/crawler/restart/', methods=['GET'])
def crawler_restart():
    r = get_redis()
    r.publish('crawler_signals', 'restart')

    sub = r.pubsub()
    sub.subscribe(['crawler_signals_feedback'])

    flag = 0
    while True:
        if flag > 120:
            return jsonify({'is_success': False})

        msg = sub.get_message()
        if msg:
            if msg.get('data') == 'restarted':
                return jsonify({'is_success': True})

        time.sleep(1)
        flag += 1


@bpApi.route('/views/', methods=['PUT'])
def viewsadd():
    views = get_collection('views')
    fieldsFromReq = request.get_json(force=True)

    fieldsFilted = filterFields(fieldsFromReq, ['name'])
    if not fieldsFilted:
        return jsonify({'is_success': True})

    fieldsForInsert = fieldsFilted.copy()
    fieldsForInsert.update({"first_created": time.time()})

    is_success = views.insert_one(fieldsForInsert)

    return jsonify({'is_success': is_success.acknowledged})

@bpApi.route('/views/', methods=['GET', 'POST'])
def viewslist():
    views = get_collection('views')
    vs = get_collection('views_sources')
    data = []
    data.extend([clean_id(i) for i in views
                .find()
                .sort('_id', 1)
                .skip(int(0))
                .limit(int(100))
                 ])

    for _ in data:
        count = vs.find({'viewName': _.get('name')}).count()
        _['count'] = count

    ret = {
        'data': data,
        'total': views.find().count()
    }

    return jsonify(ret)

@bpApi.route('/views/', methods=['DELETE'])
def viewsdelete():
    views = get_collection('views')

    fields = request.get_json(force=True)
    viewName = fields.get('name', None)
    is_success = views.delete_many({'name': viewName})

    return jsonify({'is_success': is_success.acknowledged})

@bpApi.route('/views/sources/', methods=['POST'])
def viewsgetsource():
    vs = get_collection('views_sources')

    fields = request.get_json(force=True)
    viewName = fields.get('viewName', None)
    # sourceName = fields.get('sourceName', None)

    data = []
    total = 0
    if viewName:
        data.extend([clean_id(i) for i in vs.find({'viewName': viewName})])
        total = vs.find({'viewName': viewName}).count()

    ret = {
        'data': data,
        'total': total
    }

    return jsonify(ret)

@bpApi.route('/views/sources/', methods=['PUT'])
def viewsaddsource():
    vs = get_collection('views_sources')

    fields = request.get_json(force=True)
    viewName = fields.get('viewName', None)
    sourceName = fields.get('sourceName', None)
    importance = fields.get('importance', None)

    condition = {
        'viewName': viewName,
        'sourceName': sourceName
    }

    to_set = condition.copy()
    if importance != None:
        to_set['importance'] = importance

    is_success = vs.update_one(condition, {'$set': to_set}, True)

    return jsonify({'is_success': is_success.acknowledged})


@bpApi.route('/views/sources/all/', methods=['PUT'])
def viewsaddsourceall():
    vs = get_collection('views_sources')
    sources = get_collection('sources')

    fields = request.get_json(force=True)
    viewName = fields.get('viewName', None)

    is_success_pool = {}
    for n in [_.get('machine_name') for _ in sources.find().limit(1000)]:
        condition = {
            'viewName': viewName,
            'sourceName': n
        }
        to_set = condition.copy()

        is_success = vs.update_one(condition, {'$set': to_set}, True)
        is_success_pool[n] = is_success.acknowledged

    return jsonify({'is_success_pool': is_success_pool})

@bpApi.route('/views/sources/', methods=['DELETE'])
def viewsdelsource():
    vs = get_collection('views_sources')

    fields = request.get_json(force=True)
    viewName = fields.get('viewName', None)
    sourceName = fields.get('sourceName', None)

    is_success = vs.delete_many({
        'viewName': viewName,
        'sourceName': sourceName
    })

    return jsonify({'is_success': is_success.acknowledged})

@bpApi.route('/views/sources/all/', methods=['DELETE'])
def viewsdelsourceall():
    vs = get_collection('views_sources')

    fields = request.get_json(force=True)
    viewName = fields.get('viewName', None)

    is_success = vs.delete_many({
        'viewName': viewName
    })

    return jsonify({'is_success': is_success.acknowledged})

@bpApi.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, 'downloads')
    return send_from_directory(directory=uploads, filename=filename)


@bpApi.route('/news/app_push_import/', methods=['POST'])
def app_push_import():
    import_items = get_collection('app_push_items')
    items = get_collection('items')
    fields = request.get_json(force=True)

    auth_key = fields.get('auth_key')
    if not auth_key == '16b4af8':
        return jsonify({'is_success': False, 'error_msg': 'AUTH ERROR'})

    del fields['auth_key']

    if not fields:
        return jsonify({'is_success': False, 'error_msg': 'ARGS ERROR'})

    unique_title = fields.get('title', '') + fields.get('packageName', 'N') + fields.get('contentText', '')
    uid = hashlib.md5(unique_title.encode('utf-8')).hexdigest()
    fields.update({'uid': uid})

    result = import_items.update_one({'uid': uid},
                                     {'$set': fields},
                                     upsert=True)

    if result.matched_count > 0:
        return jsonify({'is_success': False, 'error_msg': 'DUPLICATED ERROR'})

    sources_map = [
        {
            'title': u'新华社',
            'packageName': "net.xinhuamm.mainclient",
            'titleField': 'contentText',
            'bodyField': '',
            'website': 'http://www.xinhuanet.com/',
        },
        {
            'title': u'人民日报',
            'packageName': "com.peopledailychina.activity",
            'titleField': 'title',
            'bodyField': 'contentText',
            'website': 'http://www.people.com.cn/',
        },
        {
            'title': u'二十一财经',
            'packageName': "com.twentyfirstcbh.epaper",
            'titleField': 'contentText',
            'bodyField': '',
            'website': 'http://www.21jingji.com/',
        },
    ]

    filtered_data = {}
    for source in sources_map:
        if fields.get('packageName') == source.get('packageName'):
            mname = 'APP_%s' % fields.get('packageName')

            inserted = items.insert_one({
                "content": fields.get(source.get('bodyField')) if source.get('bodyField') else '',
                "source": mname,
                "host": fields.get('packageName'),
                "link": source.get('website'),
                "time": fields.get('notifyTime'),
                "name": u"%s - APP推送" % source.get('title'),
                "title": fields.get(source.get('titleField')),
                "time_human": "",
                "ctime": int(time.time())
            })
            redis = get_redis()
            rt = redis.publish('news_updated', str(inserted.inserted_id))
            filtered_data = {'db_inserted_id': str(inserted.inserted_id), 'redis_published_return': rt}

            break

    return jsonify({'is_success': True, 'filtered_data': filtered_data})


@bpApi.route('/news/tmt_wechat_import/', methods=['POST'])
def tmt_wechat_import():
    items = get_collection('items')
    fields = request.get_json(force=True)

    if not fields:
        return jsonify({'is_success': False, 'error_msg': 'ARGS ERROR'})

    sources_map = [
        u'腾讯科技', u'科技每日推送', u'科技最前线', u'财新TMT', u'网易科技', u'新浪科技',
        u'凤凰科技', u'慧聪TMT', u'蓝媒TMT', u'蓝鲸TMT', u'阿玻罗金融科技', u'TMT每日观察',
        u'朱劲松-TMT观察', u'TMT观察', u'杨吉TMT', u'搜狐科技', u'雷锋网', u'36氪', u'虎嗅网',
        u'21世纪经济报道', u'创业邦杂志', u'中国经营报', u'经济观察报', u'铅笔道', u'财新网',
        u'并购汪', u'亿欧网', u'新智元', u'猎云网', u'机器之心', u'海外情报社', u'FT中文网',
        u'界面', u'雷帝触网', u'好奇心日报',u'商业周刊中文版',u'环球老虎财经',u'钛媒体',u'PingWest品玩',
        u'速途网',u'第一财经',u'秦朔朋友圈',u'IT桔子',u'DoNews',u'动点科技',u'全球企业动态',u'蓝鲸财经网',
        u'财经天下周刊',u'VRAR创投圈',u'蓝鲸财经记者工作平台',u'B楼12座',u'经纬创投',u'小道消息',u'VR时代',
        u'财经女记者部落',u'真格基金',u'峰瑞资本',u'keso怎么看',u'一见',

    ]

    filtered_data = {}

    if fields.get('wechatName') in sources_map:
        inserted = items.insert_one({
            "content": fields.get('content', ''),
            "source": u'{}__{}'.format(fields.get('wechatId', ''), fields.get('originId', '')),
            "host": 'http://mp.weixin.qq.com/',
            "link": fields.get('sourceUrl', ''),
            "time": fields.get('createdAt', ''),
            "name": u"微信 - %s" % fields.get('wechatName'),
            "title": fields.get('title', ''),
            "time_human": "",
            "ctime": int(time.time()),
            "coops": ["tmt"],
        })
        redis = get_redis()
        rt = redis.publish('news_updated', str(inserted.inserted_id))
        filtered_data = {'db_inserted_id': str(inserted.inserted_id), 'redis_published_return': rt}

    return jsonify({'is_success': True, 'filtered_data': filtered_data})