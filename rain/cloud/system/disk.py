#!/usr/bin/env python
# -*- coding:utf-8 -*-

from getdevinfo import getdevinfo
import psutil

from rain.common import utils
from rain.config.cloud.system import disk_conf

CONF = disk_conf.CONF


class DiskInfo(object):
    """Collect hard drive information and usage.
    """

    def _get_phy_disk(self, disk_info):
        """Return to the physical disk dictionary,
        each key corresponds to the disk Partitions.
        """
        physical_disk_dict = {}
        for dev_name in disk_info.keys():
            if disk_info[dev_name]['Type'] == 'Device' \
                    and 'cdrom' not in str(disk_info[dev_name]):
                physical_disk_dict[dev_name] = \
                    disk_info[dev_name]['Partitions']
        try:
            root_device = \
                disk_info['/dev/mapper/centos-root']['HostDevice']
            root_partition = \
                disk_info['/dev/mapper/centos-root']['HostPartition']
            index = physical_disk_dict[root_device].index(root_partition)
            physical_disk_dict[root_device][index] = \
                '/dev/mapper/centos-root'
            physical_disk_dict = utils.byteify(physical_disk_dict)
        except KeyError:
            pass
        return physical_disk_dict

    def get_disk_info(self):
        """Get the physical hard disk information, The return dictionary
        contains hard disk usage information and partition information.
        """
        # Need to add multi-threaded or asynchronous.
        disk_info = []
        # Get all device information.
        all_dev_info = getdevinfo.get_info()
        # Return to the list of physical disks.
        # {'/dev/sda': ['/dev/sda1', '/dev/sda2', '/dev/mapper/centos-root']}
        physical_disk_dict = self._get_phy_disk(all_dev_info)
        for physical_disk, disk_partitions in physical_disk_dict.items():
            single_disk_info = {}
            parts_info = []
            disk_used = 0
            GB = int(1024 ** 3)
            disk_capacity = \
                all_dev_info[physical_disk]['Capacity'].strip(' GB')
            disk_product = all_dev_info[physical_disk]['Product']
            # Get each disk partition information.
            for partitions in disk_partitions:
                for psutil_partitions in psutil.disk_partitions():
                    if partitions == psutil_partitions.device and \
                            'docker' not in psutil_partitions.mountpoint:
                        part_mountpoint = psutil_partitions.mountpoint
                        part_usage = psutil.disk_usage(part_mountpoint)
                        part_info = {
                            'part_mountpoint': psutil_partitions.mountpoint,
                            'part_fstype': psutil_partitions.fstype,
                            'part_opts': psutil_partitions.opts,
                            'part_total(GB)': part_usage.total / GB,
                            'part_used(GB)': part_usage.used / GB,
                            'part_free(GB)': part_usage.free / GB,
                            'part_percent(%)': part_usage.percent,
                        }
                        parts_info.append(part_info)
            # Count the space used by a single disk.
            for part_count in parts_info:
                disk_used += part_count['part_used(GB)']
            disk_percent = format(float(disk_used)/float(
                disk_capacity), '.2f')
            single_disk_info = {
                'disk_capacity(GB)': disk_capacity,
                'disk_used(GB)': disk_used,
                'disk_percent(%)': float(disk_percent) * 100,
                'disk_product': disk_product,
            }
            if CONF.disk_info.disk_info_detail:
                single_disk_info['disk_part_info'] = parts_info
            disk_info.append(single_disk_info)
            disk_info = utils.byteify(disk_info)
        return disk_info
