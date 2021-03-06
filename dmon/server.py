import errno
import eventlet
import functools
import logging
import sys

from eventlet.green import socket

import protocol as _protocol
import pubsub


logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__file__)


def handle_data(protocol, data, address):
    proto = protocol()
    try:
        event = proto.read(data)
    except (ValueError, TypeError):
        log.exception("Error decoding event from %s", address)
        return
    else:
        pubsub.publish("events", event)


def start_datagram_server(max_connections, host, port, buf_size=4096, protocol="json"):
    print "Listening for event datagrams on: ", host, port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    conn_pool = eventlet.GreenPool(size=max_connections)

    while True:
        try:
            handler = functools.partial(handle_data,
                                        _protocol.get_protocol(protocol))
            conn_pool.spawn_n(handler, *sock.recvfrom(buf_size))
        except socket.error as e:
            if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return
            else:
                raise
        except (SystemExit, KeyboardInterrupt):
            break
