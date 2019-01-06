#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time

import docker

from rain.common import rain_log
from rain.common import utils
from rain.config.cloud.pluginss import docker_conf

CONF = docker_conf.CONF
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
l_client = docker.APIClient(base_url='unix://var/run/docker.sock')
logger = rain_log.logger


class DockerManage(object):
    """Management docker.

    Manage the docker container, mirror and get some information.
    """
    def __init__(self):
        self.container_all_usage = []
        for container in client.containers.list():
            container_name =  container.name
            get_usage_thread = threading.Thread(
                target=self._get_container_usage, args=(container_name,))
            get_usage_thread.start()
        get_usage_thread.join()
        while True:
            if len(client.containers.list()) == len(self.container_all_usage):
                break
            else:
                time.sleep(0.1)

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
        if CONF.docker_info.docker_net_info_detail:
            logger.debug('Get container network usage details.')
            net_name = container_info['NetworkSettings']['Networks'].keys()[0]
            simple_net_info = \
                container_info['NetworkSettings']['Networks'].get(net_name)
            container_net_info = {
                'ip': simple_net_info['IPAddress'],
                'gateway': simple_net_info['Gateway'],
                'netmask': simple_net_info['IPPrefixLen'],
                'macaddress': simple_net_info['MacAddress'],
                'links': simple_net_info['Links'],
            }
        else:
            container_net_info = {}
        # summary info.
        if CONF.docker_info.docker_usage_info_detail:
            if container_info['State'] == 'running':
                logger.debug('Get container resource usage details.')
                for usages in self.container_all_usage:
                    if container_info['Names'][0].lstrip('/') == \
                        usages['container_name']:
                        usages.pop('container_name')
                        self.container_all_usage.remove(usages)
                container_usage = usages
            else:
                container_usage = {}
        else:
            container_usage = {}
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
            'container_usage': container_usage,
        }
        logger.info('Collect container info, container name: {}.'
                    .format(container_info['Names'][0].lstrip('/')))
        return container_info_dict

    def get_containers_info(self, containers_name=None):
        """Query container information.
        """
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
        logger.info('Collect container information.')
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

    def _get_container_usage(self, container_name):
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
        cpu_total_usage = \
            new_result['cpu_stats']['cpu_usage']['total_usage'] - \
            old_result['cpu_stats']['cpu_usage']['total_usage']
        cpu_system_usage = \
            new_result['cpu_stats']['system_cpu_usage'] - \
            old_result['cpu_stats']['system_cpu_usage']
        container_usage = {
            'container_name': container_name,
            'cpu_total_usage':
                new_result['cpu_stats']['cpu_usage']['total_usage'] -
                old_result['cpu_stats']['cpu_usage']['total_usage'],
            'cpu_system_usage':
                new_result['cpu_stats']['system_cpu_usage'] -
                old_result['cpu_stats']['system_cpu_usage'],
            'cpu_percent': round(
                float(cpu_total_usage) / float(cpu_system_usage) *
                cpu_count * 100.0, 2),
            'mem_usage(B)': mem_usage,
            'mem_limit(B)': mem_limit,
            'mem_per': mem_per,
            'nets_traffic': nets_info,
        }
        logger.info('Collect container resource usage information.')
        self.container_all_usage.append(container_usage)
