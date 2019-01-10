#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import socket
import sys
import time
import threading

from rain.common import rain_log
from rain.config import default_conf
from rain.surface import rain_celery

CONF = default_conf.CONF
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

        while True:
            recv = conn.recv(1024000)
            if recv == 'exit' or not recv:
                conn.send('Bye')
                logger.info('Disconnect from {}.'.format(addr))
                conn.close()
                break
            # self._sned_to_mq(addr, recv)
            conn.send('Successfully received data.')
            logger.info('Successfully received from {}.'.format(addr))
