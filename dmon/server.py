import errno
import eventlet
import logging
import sys

from eventlet.green import socket

import protocol


logging.basicConfig(steam=sys.stdout)
log = logging.getLogger(__file__)


def handle_data(data, address):
    proto = protocol.JSON()
    try:
        event = proto.read(data)
    except (ValueError, TypeError) as e:
        log.error(e)
        return
    print(event)
    return event


def start_datagram_server(max_connections, host, port, buf_size=4096):
    print "Listening for event datagrams on: ", host, port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    pool = eventlet.GreenPool(size=max_connections)

    while True:
        try:
            pool.spawn_n(handle_data, *sock.recvfrom(buf_size))
        except socket.error as e:
            if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return
            else:
                raise
        except (SystemExit, KeyboardInterrupt):
            break
