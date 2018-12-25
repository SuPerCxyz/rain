#!/usr/bin/env python
# -*- coding:utf-8 -*-

from oslo_config import cfg


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
    '/home/superc/file/python/rain/rain/config/rain.conf'
])