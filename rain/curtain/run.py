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


@app.route('/detail')
def detail():
    return render_template('detail.html')


def recode_time(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    time_list = []
    for i in mycol.find().sort("time", -1).limit(-count):
        tl = time.localtime(i['time'])
        format_time = time.strftime("%H:%M", tl)
        time_list.append(format_time)
    time_list.reverse()
    return time_list


def get_data(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    cpu_list = []
    mem_list = []
    time_list = recode_time(node, count)
    for i in mycol.find().sort("time", -1).limit(-count):
        x = 0
        cpu_count = i['system_info']['cpu']['cpu_count']
        for j in i['system_info']['cpu']['cpu_percent']:
            x += j
        cpu_list.append('%.2f' % (x/cpu_count))
        mem_list.append(i['system_info']['memcache']['memcache_percent'])
    cpu_list.reverse()
    mem_list.reverse()
    return cpu_list, mem_list, time_list


@app.route("/overview", methods=["POST"])
def overview():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        cpu_list, mem_list, time_list = get_data(request_json['nodes'],
                                                 request_json['count'])
        return jsonify(cpu_list=cpu_list,
                       mem_list=mem_list,
                       time_list=time_list)


def get_node_list():
    mydb = monclient['rain']
    return mydb.list_collection_names()


@app.route("/node_list", methods=["GET"])
def node_list():
    return jsonify(node_lists=get_node_list())


@app.route("/node_status", methods=["GET"])
def node_status():
    node_list = get_node_list()
    status_result = []
    for node in node_list:
        mydb = monclient['rain']
        mycol = mydb[node]
        status = mycol.find().sort('time', -1).limit(1).next()
        status.pop('_id')
        now_time = int(time.time())
        if (now_time - status['time']) > 300:
            status['status'] = 'Lost connection'
        else:
            status['status'] = 'Online'
        status_result.append(status)
    return jsonify(nodes_status=status_result)


def cpu_info(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    cpu_dict = {}
    one_result = mycol.find().limit(1).next()
    core_count = one_result['system_info']['cpu']['cpu_count']
    for i in range(1, core_count + 1):
        key_name = 'core_' + str(i)
        cpu_dict[key_name] = []
        for one_data in mycol.find().sort("time", -1).limit(-count):
            cpu_dict[key_name].append(
                one_data['system_info']['cpu']['cpu_percent'][i -1])
        cpu_dict[key_name].reverse()
    return cpu_dict


def system_load(node, count):
    mydb = monclient['rain']
    mycol = mydb[node]
    load_dict = {
        'sys_load_1': [],
        'sys_load_5': [],
        'sys_load_15': [],
    }
    for one_data in mycol.find().sort("time", -1).limit(-count):
        db_dict = one_data['system_info']['cpu']['system_load']
        load_dict['sys_load_1'].append(db_dict['sys_load_1'])
        load_dict['sys_load_5'].append(db_dict['sys_load_5'])
        load_dict['sys_load_15'].append(db_dict['sys_load_15'])
    load_dict['sys_load_1'].reverse()
    load_dict['sys_load_5'].reverse()
    load_dict['sys_load_15'].reverse()
    return load_dict


def cpu_detail_info(node):
    mydb = monclient['rain']
    mycol = mydb[node]
    one_result = mycol.find().sort("time", -1).limit(-1).next()
    cpu_detail_dict = {}
    core_count = one_result['system_info']['cpu']['cpu_count']
    details = one_result['system_info']['cpu']['cpu_percent_info']
    for i in range(1, core_count + 1):
        key_name = 'core_' + str(i)
        cpu_detail_dict[key_name] = details[i -1]
    return cpu_detail_dict

def cpu_div(node, count):
    div_dict = {}
    div_dict['system_load'] = system_load(node, count)
    div_dict['cpu_detail_info'] = cpu_detail_info(node)
    div_dict['cpu_info'] = cpu_info(node, count)
    div_dict['time'] = recode_time(node, count)
    return div_dict


@app.route("/cpu_detail", methods=["POST"])
def cpu():
    if request.method == "POST":
        request_json = request.get_json(force=True)
        result = cpu_div(request_json['nodes'], int(request_json['count']))
        return jsonify(cpu_detail=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=True)
