#!/usr/bin/env python
# -*- coding: utf-8 -*

import time

from func_timeout import func_set_timeout

from rain.cloud import sum_info
from rain.cloud import socket_client


def client():
    while True:
        try:
            @func_set_timeout(60)
            def get_data():
                try:
                    sum_init = sum_info.SumInfo()
                    socket_cl = socket_client.SocketClient()
                    result = sum_init.sum_info()
                    socket_cl.send_data(result)
                except Exception as e:
                    print e
            get_data()
            time.sleep(30)
        except Exception as e:
            print e
            pass


if __name__ == "__main__":
    client()
