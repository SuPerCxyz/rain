#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

sum_info = cfg.OptGroup(name='sum_info',
                        title='Sum options',
                        help="""
sum_info.py script configuration.
""")

sum_info_opts = [
    cfg.ListOpt('collect_list',
                default=[],
                help='Select list to collect information.'),
    cfg.BoolOpt('network_conn_info',
                default=False,
                help='Network connection details output.'),
    cfg.BoolOpt('network_port',
                default=False,
                help='List ip port information'),
]

CONF = cfg.CONF
CONF.register_group(sum_info)
CONF.register_opts(sum_info_opts, sum_info)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
