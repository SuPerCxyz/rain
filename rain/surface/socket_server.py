#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import socket
import sys
import time
import threading

from rain.common import rain_log
from rain.config.cloud import socket_server_conf

CONF = socket_server_conf.CONF
logger = rain_log.logg(__name__)


class ScoketServer(object):
    """Socket Server.

    Socket server, constantly receiving requests and sending them to the
    message queue.
    """

    def socket_service(self):
        """Initialize the socket connection.
        """
        try:
            address = CONF.DEFAULT.address
            port = CONF.DEFAULT.port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((address, port))
            s.listen(10)
        except socket.error as msg:
            logger.error(msg)
            sys.exit(1)
        logger.info('Waiting connection...')

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self._deal_data, args=(conn, addr))
            t.start()

    def _deal_data(self, conn, addr):
        """Receive requests and process and respond.
        """
        logger.info('Accept new connection from {0}'.format(addr))
        conn.send('Hi, Welcome to rain server!')

        while True:
            recv = conn.recv(1024)
            if recv == 'exit' or not recv:
                conn.send('Goodbye')
                logger.info('Disconnect from {}.'.format(addr))
                conn.close()
                break
            logger.info('Received data from {}: {}'.format(addr, recv))
            conn.send('Successfully received')
        conn.close()

    # def _redis(self, )
