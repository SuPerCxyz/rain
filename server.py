#!/usr/bin/env python
# -*- coding: utf-8 -*


def server():
    from rain.surface import socket_server
    socket_se = socket_server.ScoketServer()
    socket_se.socket_service()


if __name__ == "__main__":
    server()
