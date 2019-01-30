#!/usr/bin/env python
# -*- coding: utf-8 -*

import time


def client():
    from rain.cloud import sum_info
    from rain.cloud import socket_client

    sum_init=sum_info.SumInfo()
    socket_cl=socket_client.SocketClient()

    while True:
        try:
            result=sum_init.sum_info()
            socket_cl.send_data(result)
            time.sleep(30)
        except:
            pass


def server():
    from rain.surface import socket_server
    socket_se=socket_server.ScoketServer()
    socket_se.socket_service()


if __name__ == "__main__":
    client()
