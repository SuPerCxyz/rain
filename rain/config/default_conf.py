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
]

CONF = cfg.CONF
CONF.register_group(default_opt)
CONF.register_opts(default_opt_opts, default_opt)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
