#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from oslo_config import cfg

path = os.getcwd()

disk_info = cfg.OptGroup(name='disk_info',
                         title='Disk information options',
                         help="""
disk.py script configuration.
""")

disk_info_opts = [
    cfg.BoolOpt('disk_info_detail',
                default=False,
                help='Whether to output more disk information.'),
]

CONF = cfg.CONF
CONF.register_group(disk_info)
CONF.register_opts(disk_info_opts, disk_info)
CONF(default_config_files=[
    path + '/rain/config/rain.conf'
])
