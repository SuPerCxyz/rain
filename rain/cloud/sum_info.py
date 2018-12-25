#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rain.cloud.pluginss.docker_im import DockerManage
from rain.cloud.system.disk import DiskInfo
from rain.cloud.system.network import NetworkInfo
from rain.cloud.system.process import ProcessInfo
from rain.cloud.system.system import SystemInfo


class SumInfo(object):
    """Summary information.

    Summarize all information in the system directory and the pluginss
    directory.
    """

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
        return docker_info

    def sum_disk(self):
        """Summary disk information.

        Does not support nvme hard disk
        """
        disk_class = DiskInfo()
        disk_usage_info = disk_class.get_disk_info()
        disk_info = {
            'disk_usage': disk_usage_info,
        }
        return disk_info

    def sum_network(self):
        """Summary network information.
        """
        net_class = NetworkInfo()
        net_traffic_info = net_class.get_network_traffic_info()
        net_conn_info = net_class.get_net_connections_info()
        net_ip_info = net_class.get_net_if_addrs()
        net_port_info = net_class.get_net_port()
        net_info = {
            'network_traffic': net_traffic_info,
            'connections': net_conn_info,
            'ip_address': net_ip_info,
            'network_port': net_port_info,
        }
        return net_info

    def sum_process(self):
        """Summary process information.
        """
        process_class = ProcessInfo()
        process_infos = process_class.get_process_info()
        process_info = {
            'process_info': process_infos,
        }
        return process_info

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
        return system_info

    def sum_info(self):
        """Summary information.
        """
        server_info = {
            'docker_info': self.sum_docker(),
            'disk_info': self.sum_disk(),
            'network_info': self.sum_network(),
            'process_info': self.sum_process(),
            'system_info': self.sum_system()
        }
        return server_info
