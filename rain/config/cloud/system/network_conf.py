#!/usr/bin/env python
# -*- coding:utf-8 -*-

from oslo_config import cfg

network_info = cfg.OptGroup(name='network_info',
                            title='Network options',
                            help='network.py script configuration.')

network_info_opts = [
    cfg.ListOpt('net_list',
                default=[],
                help='Network card list.'),
    cfg.BoolOpt('conn_proc_detail',
                default=False,
                help="""
Whether to output the process information of the network connection
"""),
    cfg.BoolOpt('port_proc_detail',
                default=False,
                help="""
Whether to output the process information of the network port
"""),
]

CONF = cfg.CONF
CONF.register_group(network_info)
CONF.register_opts(network_info_opts, network_info)
CONF(default_config_files=[
    '/home/superc/file/python/rain/rain/config/rain.conf'
])
