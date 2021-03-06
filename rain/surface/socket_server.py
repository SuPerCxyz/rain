#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import socket
import sys
import threading
import time

from rain.common import rain_log
from rain.config import default_conf
from rain.surface import rain_mongo

CONF = default_conf.CONF
logger = rain_log.logg(__name__)


class ScoketServer(object):
    """Socket Server.

    Socket server, constantly receiving requests and sending them to the
    message queue.
    """

    def __init__(self):
        self.mongodb = rain_mongo.RainMongo()

    def socket_service(self):
        """Initialize the socket connection.
        """
        try:
            address = CONF.DEFAULT.address
            port = CONF.DEFAULT.port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((address, port))
            s.listen(100)
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

        # Verify data length.
        while True:
            recv = conn.recv(1024)
            logger.info(recv)
            if 'send_len:' in recv:
                conn.send(recv)
                lens = recv[9:]
                break
            if recv == 'error':
                conn.close()
                return

        # Verify the data and send it to mongodb if it succeeds.
        loop = CONF.DEFAULT.socket_retry
        while loop:
            data = ''
            while True:
                recv = conn.recv(1024)
                if recv == 'rain_socket_send':
                    logger.info('Received all data.')
                    break
                if not recv:
                    break
                data += recv
            if len(data) == int(lens):
                conn.send('complete')
                logger.info('Data verification completed')
                self.mongodb.rain_insert_data(data, addr[0])
                logger.info('Data insertion database completed, from {}.'
                            .format(addr))
                break
            else:
                conn.send('incomplete')
                logger.warning('Did not receive full data from {}.'
                               .format(addr))
            loop -= 1
        else:
            conn.close()
            logger.error('Failed to receive data.')
