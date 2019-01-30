#!/usr/bin/env python
# -*- coding: utf-8 -*

import time

from func_timeout import func_set_timeout

from rain.cloud import sum_info
from rain.cloud import socket_client

sum_init=sum_info.SumInfo()
socket_cl=socket_client.SocketClient()


@func_set_timeout(3)
def get_data():
    try:
        result = sum_init.sum_info()
        return result
    except:
        return None

def client():

    while True:
        try:
            result = get_data()
            if result:
                socket_cl.send_data(result)
                time.sleep(30)
            else:
                time.sleep(3)
        except:
            pass


if __name__ == "__main__":
    client()
