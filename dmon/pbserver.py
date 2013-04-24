import errno
import functools
import socket

import tornado.ioloop

from tornado.options import options

import protocol


def handle_data(server_addr, client_addr, data):
    proto = protocol.JSON()
    event = proto.read(data)
    print(event)


def accept_handler(sock, fd, events):
    while True:
        try:
            server_addr = sock.getsockname()
            data, client_addr = sock.recvfrom(1024)
        except socket.error as e:
            if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return
            else:
                raise
        try:
            handle_data(server_addr, client_addr, data)
        except BaseException as e:
            print(e)


def setup():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((options.datagram_host, options.datagram_port))

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_handler(sock.fileno(), functools.partial(accept_handler, sock),
                       tornado.ioloop.IOLoop.READ)
