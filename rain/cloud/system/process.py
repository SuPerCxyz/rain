#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import psutil

from rain.common import utils
from rain.config.cloud.system import process_conf

CONF = process_conf.CONF


class ProcessInfo(object):
    """System process information.

    Collect system process related information and return.
    """

    def _get_process_info(self, detail):
        """Collect all process information, including 'name', 'exe', 'pid',
        'username', 'cmdline', 'memory_percent', 'status', 'create_time',
        'cpu_percent', 'cpu_num', and return the list.
        """
        process_infos = []
        if detail:
            processss = psutil.process_iter(attrs=['name', 'exe', 'pid',
                                                   'username', 'cmdline',
                                                   'memory_percent', 'status',
                                                   'create_time',
                                                   'cpu_percent', 'cpu_num'])
        else:
            processss = psutil.process_iter(attrs=[
                'name', 'exe', 'pid', 'status'])
        for process in processss:
            p_info = process.info
            if p_info.get('create_time', None):
                p_info['create_time'] = utils.str_time(p_info['create_time'])
            else:
                pass
            process_infos.append(p_info)
        return process_infos

    def get_process_info(self, process_name=None, process_id=None):
        """By default, all process information is returned. If the process
        name is passed in, the incoming process information is returned, and
        the type list is returned.
        """
        proc_detail = CONF.process_info.proc_detail
        process_info = []
        process_infos = self._get_process_info(proc_detail)
        if process_name:
            for p_name in process_name:
                for p_info in process_infos:
                    if p_name.lower() in p_info['name'].lower():
                        process_info.append(p_info)
        if process_id:
            for p_id in process_id:
                for p_info in process_infos:
                    if p_id == p_info['pid']:
                        process_info.append(p_info)
        if not process_name and not process_id:
            process_info = process_infos
            return process_info
        return process_info
