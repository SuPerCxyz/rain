#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
l_client = docker.APIClient(base_url='unix://var/run/docker.sock')


class DockerManage(object):
    """Management docker.

    Manage the docker container, mirror and get some information.
    """

    def _str_time(self, timestamp):
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def _byteify(self, input, encoding='utf-8'):
        """unicode to str.
        """
        if isinstance(input, dict):
            return {self._byteify(key): self._byteify(value)
                    for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self._byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode(encoding)
        else:
            return input

    def _unit_of_measurement(self, num):
        lens = len(num)
        if 0<lens<4:
            return 'B'
        elif 3<lens<7:
            return 'KB'
        elif 6<lens<10:
            return 'MB'
        elif 9<lens<13:
            return 'GB'
        elif 12<lens<16:
            return 'TB'

    def _collect_container_info(self, container_info):
        """Organize and count container information.
        """
        container_info = self._byteify(container_info)
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
            'created': self._str_time(container_info['Created']),
            'container_name': container_info['Names'][0].lstrip('/'),
            'container_status': container_info['State'],
            'container_up_time': container_info['Status'],
            'container_id': container_info['Id'],
            'container_image': container_info['Image'],
            'container_mount_info': container_mount,
            'container_port_info': container_info['Ports'],
            'container_net_info': container_net_info
        }
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
                'image_create_time': self._str_time(image['Created']),
                'image_id': str(image['Id']).split(':')[-1],
                'image_size(MB)': image['Size'] / 1024 ** 2
            }
            image_info_list.append(image_info)
        return image_info_list

    def get_container_usage(self, container_name=None):
        container_info = l_client.stats(container_name)
        old_result = eval(container_info.next())
        new_result = eval(container_info.next())
        container_info.close()
        cpu_count = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        mem_usage = new_result['memory_stats']['usage']
        container_usage = {}
        container_usage['cpu_total_usage'] = \
            new_result['cpu_stats']['cpu_usage']['total_usage'] - \
            old_result['cpu_stats']['cpu_usage']['total_usage']
        container_usage['cpu_system_usage'] = \
            new_result['cpu_stats']['system_cpu_usage'] - \
            old_result['cpu_stats']['system_cpu_usage']
        container_usage['cpu_percent'] = round(
            float(container_usage['cpu_total_usage']) /
            float(container_usage['cpu_system_usage']) *cpu_count * 100.0, 2)
        container_usage['mem_usage'] = mem_usage + \
            self._unit_of_measurement(mem_usage)
