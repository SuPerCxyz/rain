#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

disk_info = cfg.OptGroup(name='docker_info',
                         title='Docker information options',
                         help="""
docker_im.py script configuration.
""")

disk_info_opts = [
    cfg.BoolOpt('docker_net_info_detail',
                default=False,
                help='Whether to output more docker network information.'),
    cfg.BoolOpt('docker_usage_info_detail',
                default=False,
                help='Whether to output more docker usage information.'),
]

CONF = cfg.CONF
CONF.register_group(disk_info)
CONF.register_opts(disk_info_opts, disk_info)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
