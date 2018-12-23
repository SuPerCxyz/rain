#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import platform
import time

import psutil
from getdevinfo import getdevinfo

from rain.common import utils


class SystemInfo(object):
    """system information.

    Collect system information, including cpu, memory, hostname, boot time,
    login information...
    """

    def _load_stat(self):
        """Collecting system load.
        """
        cpu_count = psutil.cpu_count()
        with open("/proc/loadavg") as f:
            con = f.read().split()
            load_1 = con[0]
            load_5 = con[1]
            load_15 = con[2]
            sys_load_1 = round(float(load_1)/cpu_count * 100, 2)
            sys_load_5 = round(float(load_5)/cpu_count * 100, 2)
            sys_load_15 = round(float(load_15)/cpu_count * 100, 2)
            system_load = {
                'sys_load_1(%)': sys_load_1,
                'sys_load_5(%)': sys_load_5,
                'sys_load_15(%)': sys_load_15,
                'load_1': load_1,
                'load_5': load_5,
                'load_15': load_15
            }
            return system_load

    def get_cpuinfo_info(self):
        """Collect the number of cpu and usage information and
        return the dictionary type.
        """
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_percent_info = psutil.cpu_times_percent(interval=1, percpu=True)
        system_load = self._load_stat()
        cpu_info_dict = {
            'cpu_count': cpu_count,
            'cpu_percent': cpu_percent,
            'cpu_percent_info': cpu_percent_info,
            'system_load': system_load
        }
        return cpu_info_dict

    def get_memcache_info(self):
        """Collect memory and swap information and return dictionary type.
        """
        memcache_info = psutil.virtual_memory()
        memcache_total = memcache_info.total / 1024 ** 2
        memcache_used = memcache_info.used / 1024 ** 2
        memcache_available = memcache_info.available / 1024 ** 2
        memcache_buff = memcache_info.cached / 1024 ** 2
        memcache_cached = memcache_info.cached / 1024 ** 2
        memcache_percent = memcache_info.percent
        memcache_info_dict = {
            'memcache_total(MB)': memcache_total,
            'memcache_used(MB)': memcache_used,
            'memcache_available(MB)': memcache_available,
            'memcache_buff(MB)': memcache_buff,
            'memcache_cached(MB)': memcache_cached,
            'memcache_percent(%)': memcache_percent
        }
        return memcache_info_dict

    # def _get_phy_disk(self, disk_info):
    #     """Return to the physical disk dictionary,
    #     each key corresponds to the disk Partitions.
    #     """
    #     physical_disk_dict = {}
    #     for dev_name in disk_info.keys():
    #         if disk_info[dev_name]['Type'] == 'Device' \
    #                 and 'cdrom' not in str(disk_info[dev_name]):
    #             physical_disk_dict[dev_name] = \
    #                 disk_info[dev_name]['Partitions']
    #     try:
    #         root_device = \
    #             disk_info['/dev/mapper/centos-root']['HostDevice']
    #         root_partition = \
    #             disk_info['/dev/mapper/centos-root']['HostPartition']
    #         index = physical_disk_dict[root_device].index(root_partition)
    #         physical_disk_dict[root_device][index] = \
    #             '/dev/mapper/centos-root'
    #         physical_disk_dict = utils.byteify(physical_disk_dict)
    #     except KeyError:
    #         pass
    #     return physical_disk_dict

    # def get_disk_info(self):
    #     """Get the physical hard disk information, The return dictionary
    #     contains hard disk usage information and partition information.
    #     """
    #     # Need to add multi-threaded or asynchronous.
    #     disk_info = []
    #     # Get all device information.
    #     all_dev_info = getdevinfo.get_info()
    #     # Return to the list of physical disks.
    #     # {'/dev/sda': ['/dev/sda1', '/dev/sda2', '/dev/mapper/centos-root']}
    #     physical_disk_dict = self._get_phy_disk(all_dev_info)
    #     for physical_disk, disk_partitions in physical_disk_dict.items():
    #         single_disk_info = {}
    #         parts_info = []
    #         disk_used = 0
    #         GB = int(1024 ** 3)
    #         disk_capacity = \
    #             all_dev_info[physical_disk]['Capacity'].strip(' GB')
    #         disk_product = all_dev_info[physical_disk]['Product']
    #         # Get each disk partition information.
    #         for partitions in disk_partitions:
    #             for psutil_partitions in psutil.disk_partitions():
    #                 if partitions == psutil_partitions.device and \
    #                         'docker' not in psutil_partitions.mountpoint:
    #                     part_mountpoint = psutil_partitions.mountpoint
    #                     part_usage = psutil.disk_usage(part_mountpoint)
    #                     part_info = {
    #                         'part_mountpoint': psutil_partitions.mountpoint,
    #                         'part_fstype': psutil_partitions.fstype,
    #                         'part_opts': psutil_partitions.opts,
    #                         'part_total': part_usage.total / GB,
    #                         'part_used': part_usage.used / GB,
    #                         'part_free': part_usage.free / GB,
    #                         'part_percent': part_usage.percent / GB
    #                     }
    #                     parts_info.append(part_info)
    #         # Count the space used by a single disk.
    #         for part_count in parts_info:
    #             disk_used += part_count['part_used']
    #         single_disk_info['disk_capacity(GB)'] = disk_capacity
    #         single_disk_info['disk_used(GB)'] = disk_used
    #         disk_percent = format(float(disk_used)/float(
    #             disk_capacity), '.2f')
    #         single_disk_info['disk_percent'] = disk_percent
    #         single_disk_info['disk_product'] = disk_product
    #         single_disk_info['disk_part_info'] = parts_info
    #         disk_info.append(single_disk_info)
    #         disk_info = utils.byteify(disk_info)
    #     return disk_info

    def _get_user(self):
        """Collect login user information.
        """
        user_info_list = []
        user_list = psutil.users()
        for user in user_list:
            user_dict = {}
            user_dict['name'] = user.name
            user_dict['host'] = user.host
            user_dict['conn_time'] = utils.str_time(user.started)
            user_info_list.append(user_dict)
        return user_info_list

    def get_system_info(self):
        """Collect system information.
        """
        system_info = {}
        system_info['python_version'] = platform.python_version()
        system_info['hostname'] = platform.node()
        system_info['system_info'] = platform.platform()
        system_info['boot_time'] = utils.str_time(psutil.boot_time())
        system_info['time'] = time.asctime(time.localtime(time.time()))
        system_info['user'] = self._get_user()
        return system_info
