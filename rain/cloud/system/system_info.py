#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time


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
        memcache_total = memcache_info.total/1024**2
        memcache_used = memcache_info.used/1024**2
        memcache_available = memcache_info.available/1024**2
        memcache_buff = memcache_info.cached/1024**2
        memcache_cached = memcache_info.cached/1024**2
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

    def get_disk_info(self, disk_list):
        pass

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
