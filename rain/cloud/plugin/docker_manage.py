#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import docker

from rain.common import utils

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
l_client = docker.APIClient(base_url='unix://var/run/docker.sock')


class DockerManage(object):
    """Management docker.

    Manage the docker container, mirror and get some information.
    """

    def _collect_container_info(self, container_info):
        """Organize and count container information.
        """
        container_info = utils.byteify(container_info)
        # collect mount info.
        container_mount = []
        for mount_info in container_info['Mounts']:
            mount = {}
            mount['Destination'] = mount_info['Destination']
            mount['Source'] = mount_info['Source']
            container_mount.append(mount)
        # collect network info.
        container_net_info = {}
        simple_net_info = \
            container_info['NetworkSettings']['Networks']['bridge']
        container_net_info['ip'] = simple_net_info['IPAddress']
        container_net_info['gateway'] = simple_net_info['Gateway']
        container_net_info['netmask'] = simple_net_info['IPPrefixLen']
        container_net_info['macaddress'] = simple_net_info['MacAddress']
        container_net_info['links'] = simple_net_info['Links']
        # summary info.
        container_info_dict = {
            'created': utils.str_time(container_info['Created']),
            'container_name': container_info['Names'][0].lstrip('/'),
            'container_status': container_info['State'],
            'container_up_time': container_info['Status'],
            'container_id': container_info['Id'],
            'container_image': container_info['Image'],
            'container_mount_info': container_mount,
            'container_port_info': container_info['Ports'],
            'container_net_info': container_net_info,
            'container_usage': self.get_container_usage(
                container_info['Names'][0].lstrip('/'))
        }
        return container_info_dict

    def get_containers_info(self, containers_name=None):
        """Query container information.
        """
        # Need to add multithreading.
        container_info_list = []
        containers_info_list = l_client.containers(all=True)
        if containers_name:
            for container in containers_name:
                for containers_info in containers_info_list:
                    if container == str(
                            containers_info['Names'][0].lstrip('/')):
                        container_info = self._collect_container_info(
                            containers_info)
                        container_info_list.append(container_info)
        else:
            for containers_info in containers_info_list:
                container_info = self._collect_container_info(containers_info)
                container_info_list.append(container_info)
        return container_info_list

    def get_images(self):
        """Collect docker image info.
        """
        image_info_list = []
        image_list = l_client.images(all=True)
        for image in image_list:
            image_info = {
                'image_name':
                    str(image['RepoTags'][0]).split('/')[-1].split(':')[0],
                'image_create_time': utils.str_time(image['Created']),
                'image_id': str(image['Id']).split(':')[-1],
                'image_size(MB)': image['Size'] / 1024 ** 2
            }
            image_info_list.append(image_info)
        return image_info_list

    def get_container_usage(self, container_name=None):
        """Collect container resource usage.
        """
        container_info = l_client.stats(container_name)
        old_result = eval(container_info.next())
        new_result = eval(container_info.next())
        container_info.close()
        cpu_count = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        mem_usage = new_result['memory_stats']['usage']
        mem_limit = new_result['memory_stats']['limit']
        mem_per = round(float(mem_usage) / float(mem_limit) * 100.0, 2)
        nets_info = []
        for net in new_result['networks'].keys():
            net_info = {}
            net_rx = (new_result['networks'][net]['rx_bytes'] / 8) - \
                (old_result['networks'][net]['rx_bytes'] / 8)
            net_tx = (new_result['networks'][net]['tx_bytes'] / 8) - \
                (old_result['networks'][net]['tx_bytes'] / 8)
            net_info[net] = {
                'net_rx(B)': net_rx,
                'net_tx(B)': net_tx
            }
            nets_info.append(net_info)
        container_usage = {}
        container_usage['cpu_total_usage'] = \
            new_result['cpu_stats']['cpu_usage']['total_usage'] - \
            old_result['cpu_stats']['cpu_usage']['total_usage']
        container_usage['cpu_system_usage'] = \
            new_result['cpu_stats']['system_cpu_usage'] - \
            old_result['cpu_stats']['system_cpu_usage']
        container_usage['cpu_percent'] = round(
            float(container_usage['cpu_total_usage']) /
            float(container_usage['cpu_system_usage']) * cpu_count * 100.0, 2)
        container_usage['mem_usage(B)'] = mem_usage
        container_usage['mem_limit(B)'] = mem_limit
        container_usage['mem_per'] = mem_per
        container_usage['nets_traffic'] = nets_info
        return container_usage
