#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import psutil


class ProcessInfo(object):
    """System process information.

    Collect system process related information and return.
    """

    def _get_process_info(self):
        """Collect all process information, including 'name', 'exe', 'pid',
        'username', 'cmdline', 'memory_percent', 'status', 'create_time',
        'cpu_percent', 'cpu_num', and return the list.
        """
        process_infos = []
        processss = psutil.process_iter(attrs=['name', 'exe', 'pid',
                                               'username', 'cmdline',
                                               'memory_percent', 'status',
                                               'create_time', 'cpu_percent',
                                               'cpu_num'])
        for process in processss:
            p_info = process.info
            time_local = time.localtime(p_info['create_time'])
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            p_info['create_time'] = dt
            process_infos.append(p_info)
        return process_infos

    def get_process_info(self, process_name=None):
        """By default, all process information is returned. If the process
        name is passed in, the incoming process information is returned, and
        the type list is returned.
        """
        process_info = []
        process_infos = self._get_process_info()
        if process_name:
            for p_name in process_name:
                for p_info in process_infos:
                    if p_name.lower() in p_info['name'].lower():
                        process_info.append(p_info)
        else:
            process_info = process_infos
        return process_info
