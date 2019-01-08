#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

default_info = cfg.OptGroup(name='DEFAULT',
                            title='Default options',
                            help="""
socket_client.py script configuration.
""")

default_info_opts = [
    cfg.StrOpt('address',
               default='',
               help='Monitor node ip.'),
    cfg.IntOpt('port',
               default='',
               help='Monitor node port.'),
]

CONF = cfg.CONF
CONF.register_group(default_info)
CONF.register_opts(default_info_opts, default_info)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
