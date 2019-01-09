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
        address = CONF.DEFAULT.address
        port = CONF.DEFAULT.port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((address, port))
        data = json.dumps(data)
        client.send(data)
        logger.info(client.recv(1024000))
        client.send('exit')
        logger.info(client.recv(1024000))
        client.close()
