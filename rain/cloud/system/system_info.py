#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time

from getdevinfo import getdevinfo
import psutil


class SystemInfo(object):
    """system information.

    Collect system information, including cpu, memory, hard disk, network,
    host name, boot time, login information, process...
    """

    def _load_stat(self):
        """Collecting system load.
        """
        with open("/proc/loadavg") as f:
            con = f.read().split()
            load_1 = con[0]
            load_5 = con[1]
            load_15 = con[2]
            sys_load_1 = round(float(load_1)/cpu_count*100, 2)
            sys_load_5 = round(float(load_5)/cpu_count*100, 2)
            sys_load_15 = round(float(load_15)/cpu_count*100, 2)
            system_load = {
                'sys_load_1': sys_load_1,
                'sys_load_5': sys_load_5,
                'sys_load_15': sys_load_15
            }
            return system_load

    def get_cpuinfo_info(self):
        """Collect the number of cpu and usage information and
        return the dictionary type.
        """
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_percent_info = psutil.cpu_times_percent(interval=1, percpu=True)
        cpu_info_dict = {
            'cpu_count': cpu_count,
            'cpu_percent': cpu_percent,
            'cpu_percent_info': cpu_percent_info
        }
        system_load = self._load_stat()
        return cpu_info_dict, system_load

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
            'memcache_total': memcache_total,
            'memcache_used': memcache_used,
            'memcache_available': memcache_available,
            'memcache_buff': memcache_buff,
            'memcache_cached': memcache_cached,
            'memcache_percent': memcache_percent
        }
        return memcache_info_dict
    
    def byteify(self, input, encoding='utf-8'):
        if isinstance(input, dict):
            return {byteify(key): byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode(encoding)
        else:
            return input
    
    def _get_phy_disk(self, disk_info):
        """Return to the physical disk dictionary,
        each key corresponds to the disk Partitions.
        """
        physical_disk_dict = {}
        for dev_name in disk_info.keys():
            if disk_info[dev_name]['Type'] == 'Device' and \
                'cdrom' not in str(disk_info[dev_name]):
                physical_disk_dict[dev_name] = \
                    disk_info[dev_name]['Partitions']
        root_device = disk_info['/dev/mapper/centos-root']['HostDevice']
        root_partition = disk_info['/dev/mapper/centos-root']['HostPartition']
        index = physical_disk_dict[root_device].index(root_partition)
        physical_disk_dict[root_device][index] = '/dev/mapper/centos-root'
        physical_disk_dict = self.byteify(physical_disk_dict)
        return physical_disk_dict

def get_disk_info(self, disk_list):
    disk_info = []
    all_dev_info = getdevinfo.get_info()
    # {'/dev/sda': ['/dev/sda1', '/dev/sda2', '/dev/mapper/centos-root']}
    physical_disk_dict = self._get_phy_disk(all_dev_info)
    for physical_disk, disk_partitions in physical_disk_dict.items():
        single_disk_info = {}
        parts_info = []
        disk_used = 0
        disk_capacity = all_dev_info[physical_disk]['Capacity'].strip(' GB')
        disk_product = all_dev_info[physical_disk]['Product']
        for partitions in disk_partitions:
            for psutil_partitions in psutil.disk_partitions():
                if partitions == psutil_partitions.device and \
                    'docker' not in psutil_partitions.mountpoint:
                    part_mountpoint = psutil_partitions.mountpoint
                    part_fstype = psutil_partitions.fstype
                    part_opts = psutil_partitions.opts
                    part_usage = psutil.disk_usage(part_mountpoint)
                    part_total = part_usage.total
                    part_used = part_usage.used
                    part_free = part_usage.free
                    part_percent = part_usage.percent
                    GB = int(1024 ** 3)
                    part_info = {
                        'part_mountpoint': part_mountpoint,
                        'part_fstype': part_fstype,
                        'part_opts': part_opts,
                        'part_total': part_total / GB,
                        'part_used': part_used / GB,
                        'part_percent': part_percent / GB
                    }
                    parts_info.append(part_info)
        for part_count in parts_info:
            disk_used += part_count['part_used']
        single_disk_info['disk_capacity(GB)'] = disk_capacity
        single_disk_info['disk_used(GB)'] = disk_used
        single_disk_info['disk_percent'] = disk_used / int(disk_capacity)
        single_disk_info['disk_product'] = disk_product
        single_disk_info['disk_part_info'] = parts_info
        disk_info.append(single_disk_info)
    return disk_info

    def get_network_info(self, net_list=None):
        # Need to add multithreading
        if not net_list:
            net_list = psutil.net_io_counters(pernic=True).keys()
        net_infos = {}
        net_info_s = []
        total_recv = 0
        total_sent = 0
        for net_card in net_list:
            net_io_count_1 = psutil.net_io_counters(pernic=True)[net_card]
            r1 = net_io_count_1.bytes_recv
            s1 = net_io_count_1.bytes_sent
            # t1 = psutil.net_io_counters()
            time.sleep(1)
            net_io_count_2 = psutil.net_io_counters(pernic=True)[net_card]
            r2 = net_io_count_2.bytes_recv
            s2 = net_io_count_2.bytes_sent
            # t2 = psutil.net_io_counters()
            net_recv = (r2 - r1) / (1024 ** 2)
            net_sent = (s2 - s1) / (1024 ** 2)
            # net_total = (t2 - t1) / (1024 ** 2)
            net_info = {
                'net_card': net_card,
                'net_recv(MB)': net_recv,
                'net_sent(MB)': net_sent
            }
            total_recv += net_recv
            total_sent += net_sent
            net_info_s.append(net_info)
        net_infos['single_flow'] = net_info_s
        net_infos['total_flow'] = {
            'total_recv(MB)': total_recv,
            'total_sent(MB)': total_sent
        }
        return net_infos

    def get_boot_time(self):
        """Get system boot time and return.
        """
        timestamp = psutil.boot_time()
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt
