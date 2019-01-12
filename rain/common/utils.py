#!/usr/bin/env python
# -*- coding:utf-8 -*-

from threading import Thread
import time


def str_time(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def byteify(input, encoding='utf-8'):
    """unicode to str.
    """
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input


def unit_of_measurement(num):
    lens = len(num)
    if 0 < lens < 4:
        return num + 'B'
    elif 3 < lens < 7:
        return num / 1024 + 'KB'
    elif 6 < lens < 10:
        return num / (1024 ** 2) + 'MB'
    elif 9 < lens < 13:
        return num / (1024 ** 3) + 'GB'
    elif 12 < lens < 16:
        return num / (1024 ** 4) + 'TB'
    else:
        pass

def async_call(fn):
    def wrapper(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.start()

    return wrapper
