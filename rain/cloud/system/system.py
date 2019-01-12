#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import platform
import time

from getdevinfo import getdevinfo
import psutil

from rain.common import rain_log
from rain.common import utils
from rain.common.utils import async_call

logger = rain_log.logg(__name__)


class SystemInfo(object):
    """system information.

    Collect system information, including cpu, memory, hostname, boot time,
    login information...
    """

    def __init__(self):
        self.thread = {}

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
            logger.info('Collect system load.')
            return system_load

    @async_call
    def _cpu_percent(self):
        tmp = psutil.cpu_percent(interval=1, percpu=True)
        self.thread['cpu_percent'] = tmp

    @async_call
    def _cpus_times_percent(self):
        tmp = psutil.cpu_times_percent(interval=1, percpu=True)
        self.thread['cpus_times_percent'] = tmp

    def get_cpuinfo_info(self):
        """Collect the number of cpu and usage information and
        return the dictionary type.
        """
        cpu_count = psutil.cpu_count()
        self._cpu_percent()
        self._cpus_times_percent()
        while True:
            if len(self.thread.keys()) == 2:
                break
            time.sleep(0.1)
        cpu_percent_info = []
        for cpu in self.thread['cpus_times_percent']:
            percent_info = {
                'user': cpu.user,
                'system': cpu.system,
                'idle': cpu.idle,
                'iowait': cpu.iowait
            }
            cpu_percent_info.append(percent_info)
        system_load = self._load_stat()
        cpu_info_dict = {
            'cpu_count': cpu_count,
            'cpu_percent': self.thread['cpu_percent'],
            'cpu_percent_info': cpu_percent_info,
            'system_load': system_load
        }
        logger.info('Collect cpu related information.')
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
        logger.info('Collect memory related information.')
        return memcache_info_dict

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
        logger.info('Collect user login information.')
        return system_info
