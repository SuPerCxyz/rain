#!/usr/bin/env python
# -*- coding: utf-8 -*

import json
import time

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import pymongo

# from rain.common import rain_log
# from rain.config import default_conf

# CONF = default_conf.CONF
# logger = rain_log.logg(__name__)

app = Flask(__name__)

# ip = CONF.DEFAULT.mongo_address
# port = CONF.DEFAULT.mongo_port
# conn_link = 'mongodb://' + ip + ':' + port + '/'
conn_link = 'mongodb://127.0.0.1:27017/'
monclient = pymongo.MongoClient(conn_link)


@app.route('/')
def index():
    return render_template('index.html')


def get_data(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    cpu_list = []
    mem_list = []
    time_list = []
    result = {}
    for i in mycol.find().sort('time', -1).limit(count):
        x = 0
        cpu_count = i['system_info']['cpu']['cpu_count']
        for j in i['system_info']['cpu']['cpu_percent']:
            x += j
        cpu_list.append('%.2f' % (x/cpu_count))
        mem_list.append(i['system_info']['memcache']['memcache_percent(%)'])
        tl = time.localtime(i['time'])
        format_time = time.strftime("%H:%M", tl)
        time_list.append(format_time)
    time_list.reverse()
    result = {
        'cpu_list': cpu_list,
        'mem_list': mem_list,
        'time_list': time_list
    }
    return result


def get_node_info(count):
    all_result = {}
    mydb = monclient['rain']
    node_list = mydb.list_collection_names()
    for node in node_list:
        all_result[node] = get_data(node, count)
    return all_result


@app.route("/overview", methods=["POST"])
def overview():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        return get_node_info(request_json['count'])


# @app.route("/node_list", methods=["GET"])
# def node_list():
#     if request.method == "GET":
#         print get_node_list()
#         return jsonify(node_lists = get_node_list())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=True)
