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

def get_data():
    mydb = monclient['rain']
    mycol = mydb['dev_127.0.0.1']
    cpu = []
    mem = []
    result = mycol.find()
    for i in result:
        cpu.append(i['system_info']['cpu']['cpu_percent'][0])
        mem.append(i['system_info']['memcache']['memcache_percent'])
    lens = len(result)
    return cpu, mem, lens


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/overview", methods=["GET"])
def weather():
    if request.method == "GET":
        cpu, mem, lens = get_data()
    
    return jsonify(cpu_list = cpu, mem_list = mem, x_len = lens)




if __name__ == '__main__':
    app.run()
