#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
import subprocess
import time

import psutil

from rain.config import default_conf

CONF = default_conf.CONF
log_path = CONF.DEFAULT.log_path

def logg(name):
    logger = logging.getLogger(name)

    fh = logging.FileHandler(log_path + '/rain.log')
    if CONF.DEFAULT.debug:
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger