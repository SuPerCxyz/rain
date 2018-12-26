#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

process_info = cfg.OptGroup(name='process_info',
                            title='Process options',
                            help='process.py script configuration.')

process_info_opts = [
    cfg.BoolOpt('proc_detail',
                default=False,
                help="""
Whether to output more information about the process
"""),
]

CONF = cfg.CONF
CONF.register_group(process_info)
CONF.register_opts(process_info_opts, process_info)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
