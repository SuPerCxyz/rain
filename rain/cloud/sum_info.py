#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from rain.cloud.pluginss.docker_im import DockerManage
from rain.cloud.system.disk import DiskInfo
from rain.cloud.system.network import NetworkInfo
from rain.cloud.system.process import ProcessInfo
from rain.cloud.system.system import SystemInfo
from rain.common import rain_log
from rain.common.utils import async_call
from rain.config.cloud import sum_info_conf

CONF = sum_info_conf.CONF
logger = rain_log.logg(__name__)


class SumInfo(object):
    """Summary information.

    Summarize all information in the system directory and the pluginss
    directory.
    """

    def __init__(self):
        self.server_info = {}

    @async_call
    def sum_docker(self):
        """Summary docker information.
        """
        docker_class = DockerManage()
        docker_container_info = docker_class.get_containers_info()
        docker_image_info = docker_class.get_images()
        docker_info = {
            'containers': docker_container_info,
            'images': docker_image_info,
        }
        self.server_info['docker_info'] = docker_info
        # return docker_info

    @async_call
    def sum_disk(self):
        """Summary disk information.

        Does not support nvme hard disk
        """
        disk_class = DiskInfo()
        disk_usage_info = disk_class.get_disk_info()
        disk_info = {
            'disk_usage': disk_usage_info,
        }
        self.server_info['disk_info'] = disk_info
        # return disk_info

    @async_call
    def sum_network(self):
        """Summary network information.
        """
        net_class = NetworkInfo()
        net_traffic_info = net_class.get_network_traffic_info()
        net_ip_info = net_class.get_net_if_addrs()
        net_info = {
            'network_traffic': net_traffic_info,
            'ip_address': net_ip_info,
        }
        if CONF.sum_info.network_conn_info:
            net_conn_info = net_class.get_net_connections_info()
            net_info['connections'] = net_conn_info
        if CONF.sum_info.network_port:
            net_port_info = net_class.get_net_port()
            net_info['network_port'] = net_port_info
        self.server_info['network_info'] = net_info
        # return net_info

    @async_call
    def sum_process(self):
        """Summary process information.
        """
        process_class = ProcessInfo()
        process_infos = process_class.get_process_info()
        process_info = {
            'process_info': process_infos,
        }
        self.server_info['process_info'] = process_info
        # return process_info

    @async_call
    def sum_system(self):
        """Summary system information.
        """
        system_class = SystemInfo()
        cpu_info = system_class.get_cpuinfo_info()
        mem_info = system_class.get_memcache_info()
        system_infos = system_class.get_system_info()
        system_info = {
            'cpu': cpu_info,
            'memcache': mem_info,
            'system_info': system_infos,
        }
        self.server_info['system_inf'] = system_info
        # return system_info

    def sum_info(self):
        """Summary information.
        """
        self.server_info = {}
        collect_list = CONF.sum_info.collect_list
        logger.info('Collect the following service information: {}.'
                    .format(collect_list))
        if 'docker' in collect_list:
            self.sum_docker()
        if 'disk' in collect_list:
            self.sum_disk()
        if 'network' in collect_list:
            self.sum_network()
        if 'process' in collect_list:
            self.sum_process()
        if 'system' in collect_list:
            self.sum_system()
        while True:
            if len(self.server_info.keys()) == len(collect_list):
                break
            time.sleep(0.1)
        logger.info('Successful data collection.')
        return self.server_info
