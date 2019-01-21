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

    def rain_insert_data(self, data, address, db_name='rain'):
        data = json.loads(data)
        hostname = data['system_info']['system_info']['hostname']
        mydb = self.monclient[db_name]
        mycol = mydb[str(hostname) + '_' + str(address)]
        data['ip_address'] = address
        data['hostname'] = hostname
        result = mycol.insert_one(data)
        logger.info('Successfully inserted into mongodb, id: {}.'.format(
                    result.inserted_id))
