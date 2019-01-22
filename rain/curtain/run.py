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


def get_data(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    cpu_list = []
    mem_list = []
    time_list = []
    for i in mycol.find().sort('time', -1).limit(count):
        x = 0
        cpu_count = i['system_info']['cpu']['cpu_count']
        for j in i['system_info']['cpu']['cpu_percent']:
            x += j
        cpu_list.append(x / cpu_count)
        mem_list.append(i['system_info']['memcache']['memcache_percent(%)'])
        tl = time.localtime(i['time'])
        format_time = time.strftime("%H:%M", tl)
        time_list.append(format_time)
    time_list.reverse()
    return cpu_list, mem_list, time_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/overview", methods=["POST"])
def overview():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        print request_json
        cpu_list, mem_list, time_list = get_data(request_json['nodes'],
                                                 request_json['count'])
        return jsonify(cpu_list=cpu_list,
                       mem_list=mem_list,
                       time_list=time_list)


if __name__ == '__main__':
    app.run(debug=True)
