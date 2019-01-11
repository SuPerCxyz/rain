#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import time

import pymongo

from rain.common import rain_log
from rain.config import default_conf

CONF = default_conf.CONF
logger = rain_log.logg(__name__)


class RainMongo(object):

    def __init__(self):
        ip = CONF.DEFAULT.mongo_address
        port = CONF.DEFAULT.mongo_port
        conn_link = 'mongodb://' + ip + ':' + port + '/'
        self.monclient = pymongo.MongoClient(conn_link)

    def rain_insert_data(
            self, data, address, db_name='rain', tab_name='node_usage'):
        data = json.loads(data)
        mydb = self.monclient[db_name]
        mycol = mydb[tab_name]
        now_time = int(time.time())
        data['now_time'] = now_time
        data['ip_address'] = address
        result = mycol.insert_one(data)
        logger.info('Successfully inserted into mongodb, id: {}.'.format(
                    result.inserted_id))
