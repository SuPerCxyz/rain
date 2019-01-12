#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import socket

from rain.common import rain_log
from rain.config import default_conf

CONF = default_conf.CONF
logger = rain_log.logg(__name__)


class SocketClient(object):
    """Socket client.

    The socket client receives the request data and sends the data to the
    server.
    """

    def send_data(self, data):
        """Data is sent to the socket server.
        """
        address = CONF.DEFAULT.address
        port = CONF.DEFAULT.port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((address, port))
        data = json.dumps(data)

        # Send data length and verify that the server receives correctly,
        # preventing real data transmission errors.
        lens = 'send_len:' + str(len(data))
        loop = CONF.DEFAULT.socket_retry
        while loop:
            client.send(lens)
            if lens == client.recv(1024000):
                logger.info('The data length verification is successful and '
                            'the length is: {}.'.format(str(len(data))))
                break
            else:
                loop -= 1
                logger.warning('Data length verification failed and '
                               're-verification. remaining times: {}.'
                               .format(loop - 1))
            if loop == 0:
                client.send('error')
                logger.error('Data length check error, end sending data.')
                # client.close()
                return

        # Send data and verify that the server receives it correctly, and
        # resend it when it receives 'Retry'.
        loop = CONF.DEFAULT.socket_retry
        client.send(data)
        while loop:
            message = client.recv(1024000)
            if message == 'Retry':
                client.send(data)
                logger.warning('Data verification failed and re-verification. '
                               'remaining times: {}.'.format(loop - 1))
                loop -= 1
            if 'Successfully' in message:
                logger.info('The socket server successfully received the '
                            'data.')
                client.send('exit')
                break
        # client.close()
