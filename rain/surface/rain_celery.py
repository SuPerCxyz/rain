#!/usr/bin/env python
# -*- coding=utf-8 -*-

# from rain.common import rain_log
# from rain.config import default_conf

# from __future__ import absolute_import

from celery import Celery
from celery import platforms
from kombu.common import Broadcast, Queue, Exchange

# CONF = default_conf.CONF
# logger = rain_log.logg(__name__)

# Connect to redis
# redis_passwd = CONF.DEFAULT.redis_passwd
# redis_address = CONF.DEFAULT.address
# redis_port = CONF.DEFAULT.redis_port
# redis_conn = ('redis://:' + redis_passwd + '@' + redis_address + ':' +
#               redis_port + '/1')
# print redis_conn
redis_conn = 'redis://:111122@localhost:6379/11'
app = Celery('rain', broker=redis_conn)

# Allow root execution
platforms.C_FORCE_ROOT = True

app.conf.update(
    task_queues=(
        Queue("InsData", Exchange("InsData"), route_key="rain.surface.rain_celery.InsData"),
    )
)


@app.task
def InsData(addr, recv):
    if addr and recv:
        print '666'
    else:
        print 'error'
