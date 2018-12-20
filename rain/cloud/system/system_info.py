#!/usr/bin/env python
# -*- coding:utf-8 -*-

import psutil


class SystemInfo(object):

    def _get_memcache_info(self):
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

    def _get_cpuinfo_info(self):
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_percent_info = psutil.cpu_times_percent(interval=1, percpu=True)
        cpu_info_dict = {
            'cpu_count': cpu_count,
            'cpu_percent': cpu_percent,
            'cpu_percent_info': cpu_percent_info
        }
        return cpu_info_dict
