#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import psutil

from process_info import ProcessInfo


class NetworkInfo(object):
    """System port information.

    Collect system port related information and return.
    """

    def get_network_flow_info(self, net_list=None):
        """Collect network traffic information
        """
        # Need to add multi-threaded or asynchronous.
        if not net_list:
            net_list = psutil.net_io_counters(pernic=True).keys()
        net_flow_infos = {}
        net_info_s = []
        total_recv = 0
        total_sent = 0
        time1_net = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        time1_net = psutil.net_io_counters(pernic=True)
        for net_card in net_list:
            net_io_count_1 = time1_net[net_card]
            r1 = net_io_count_1.bytes_recv
            s1 = net_io_count_1.bytes_sent
            net_io_count_2 = time1_net[net_card]
            r2 = net_io_count_2.bytes_recv
            s2 = net_io_count_2.bytes_sent
            net_recv = (r2 - r1) / (1024 ** 2)
            net_sent = (s2 - s1) / (1024 ** 2)
            net_info = {
                'net_card': net_card,
                'net_recv(MB)': net_recv,
                'net_sent(MB)': net_sent
            }
            total_recv += net_recv
            total_sent += net_sent
            net_info_s.append(net_info)
        net_flow_infos['single_flow'] = net_info_s
        net_flow_infos['total_flow'] = {
            'total_recv(MB)': total_recv,
            'total_sent(MB)': total_sent
        }
        return net_flow_infos

    def _get_net_connections_info(self):
        connect_info = psutil.net_connections()
        return connect_info

    def get_net_connections_info(self):
        """Collect network connection information.
        """
        connect_info_list = []
        connect_info_list_raw = self._get_net_connections_info()
        process_infos_list = ProcessInfo().get_process_info()
        for connect_info in connect_info_list_raw:
            for process_infos in process_infos_list:
                if connect_info.pid == process_infos['pid']:
                    process_info = process_infos
            if connect_info.raddr:
                conn_info = {
                    'local_addr': {
                        'ip': connect_info.laddr.ip,
                        'port': connect_info.laddr.port
                    },
                    'remote_addr': {
                        'ip': connect_info.raddr.ip,
                        'port': connect_info.raddr.port
                    },
                    'status': connect_info.status,
                    'pid': connect_info.pid,
                    'process_info': process_info
                }
            else:
                conn_info = {
                    'local_addr': {
                        'ip': connect_info.laddr.ip,
                        'port': connect_info.laddr.port
                    },
                    'remote_addr': {
                    },
                    'status': connect_info.status,
                    'pid': connect_info.pid,
                    'process_info': process_info
                }
            connect_info_list.append(conn_info)
        return connect_info_list

    def _get_net_if_addrs(self):
        net_if_addr = psutil.net_if_addrs()
        return net_if_addr

    def get_net_if_addrs(self):
        """Collect network card and ip information.
        """
        net_if_addrs = []
        net_if_addr_dict = self._get_net_if_addrs()
        for net_card in net_if_addr_dict.keys():
            net_card_dict = {}
            single_net_card_list = []
            net_card_infos = net_if_addr_dict[net_card]
            for net_card_info in net_card_infos:
                single_net_card = {
                    'address': net_card_info.address,
                    'netmask': net_card_info.netmask,
                    'broadcast': net_card_info.broadcast,
                    'ptp': net_card_info.ptp
                }
                single_net_card_list.append(single_net_card)
            net_card_dict['net_card'] = net_card
            net_card_dict['card_info'] = single_net_card_list
            net_if_addrs.append(net_card_dict)
        return net_if_addrs
