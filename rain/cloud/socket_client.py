#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import socket
import sys
import time
import threading

# from rain.common import rain_log
# from rain.config.cloud import socket_client_conf

# CONF = socket_client_conf.CONF
# logger = rain_log.logger

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('10.0.0.12', 2333))
# 接收欢迎消息:
print s.recv(1024)
for data in ['Michael', 'Tracy', 'Sarah']:
    # 发送数据:
    s.send(data)
    print s.recv(1024)
s.send('exit')
s.close()
