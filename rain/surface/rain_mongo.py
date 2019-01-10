#!/usr/bin/env python
# -*- coding=utf-8 -*-

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
