#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

default_opt = cfg.OptGroup(name='DEFAULT',
                           title='default options',
                           help='rain project default options.')
default_opt_opts = [
    cfg.StrOpt('log_path',
               default='/var/log/rain',
               help='Rain project log path.'),
    cfg.BoolOpt('debug',
                default=False,
                help='Open debug to collect more information.'),
    cfg.StrOpt('address',
               default='',
               help='Monitor node ip.'),
    cfg.IntOpt('port',
               default='',
               help='Monitor node port.'),
    cfg.StrOpt('mongo_address',
               default='localhost',
               help='Mongodb address.'),
    cfg.StrOpt('mongo_port',
               default='27017',
               help='Mongodb port'),
]

CONF = cfg.CONF
CONF.register_group(default_opt)
CONF.register_opts(default_opt_opts, default_opt)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
