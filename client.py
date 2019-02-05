#!/usr/bin/env python
# -*- coding: utf-8 -*

import functools
import signal
import sys
import time

from func_timeout import func_set_timeout

from rain.cloud import sum_info
from rain.cloud import socket_client


class TimeoutError(Exception): pass
 
 
def timeout(seconds,
            error_message="Timeout Error: the cmd 30s have not finished."):
    def decorated(func):
        result = ""
 
        def _handle_timeout(signum, frame):
            global result
            result = error_message
            raise TimeoutError(error_message)
 
        def wrapper(*args, **kwargs):
            global result
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
 
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                return result
            return result
 
        return functools.wraps(func)(wrapper)
    return decorated

def client():
    while True:
        try:
            @timeout(60)
            def get_data():
                sum_init = sum_info.SumInfo()
                socket_cl = socket_client.SocketClient()
                result = sum_init.sum_info()
                socket_cl.send_data(result)
            get_data()
            time.sleep(30)
        except Exception as e:
            print e
            pass


if __name__ == "__main__":
    client()
