#!/usr/bin/env python
# -*- coding:utf-8 -*-

import docker


client = docker.DockerClient(base_url='unix://var/run/docker.sock')

class DockerManage(object):
    """Management docker.

    Manage the docker container, mirror and get some information.
    """

    def get_containers_info(self, containers_name=None):
        containers_info = client.containers.list()
        if containers_name:
            for container in containers_name:
                container_info = client.containers.get(container)
                container_info_dict = {
                    'container_name': container_info.name,
                    'container_status': container_info.status,
                    'container_id': container_info.id,
                }
