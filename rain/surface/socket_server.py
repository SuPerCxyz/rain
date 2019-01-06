#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import socket
import sys
import time
import threading

from rain.common import rain_log
from rain.config.cloud import socket_client_conf

CONF = socket_client_conf.CONF
logger = rain_log.logger


class ScoketClient(object):

    def socket_service(self):
        try:
            address = CONF.DEFAULT.address
            port = CONF.DEFAULT.port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((address, port))
            s.listen(10)
        except socket.error as msg:
            print msg
            sys.exit(1)
        logger.INFO('Waiting connection...')

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self.deal_data, args=(conn, addr))
            t.start()

    def deal_data(self, conn, addr):
        print 'Accept new connection from {0}'.format(addr)
        conn.send('Hi, Welcome to the server!')

        while True:
            recv = conn.recv(1024)
            if recv == 'exit' or not recv:
                conn.send('Goodbye')
                logger.INFO('Disconnect from {}.'.format(addr))
                conn.close()
                break
            print recv
            conn.send('Successfully received')
        conn.close()
        logger.INFO('Successfully received {} data'.format(addr))
