import argparse
import json
import os
import random
import socket
import textwrap
import time

from event import Event
from protocol import get_protocol


__description__ = """
An interactive shell for testing dmon instances.

Sets up a datagram socket for you and adds a few helpers:

- sock: the datagram socket
- addr: a (host, port) pair to pass to sock.sendto
- event: a method for constructing an Event object with default
  parameters
- protocol: an instance of a Protocol subclass
"""

SHELLS = ["ipython", "bpython", "python"]


def event(host="55.55.55.5", service="web", state="online",
          description="Testing", time=1370887560, ttl=3600,
          metric=0.5):
    return Event(host=host,
                 service=service,
                 state=state,
                 description=description,
                 time=time,
                 ttl=ttl,
                 metric=metric)


def setup_env(args):
    env = globals()
    env['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    env['addr'] = (args.addr, args.port)
    env['event'] = event
    env['protocol'] = get_protocol(args.protocol)()


def setup_plain():
    import code
    code.interact(local=globals())


def setup_ipython():
    from IPython import embed
    embed()


def setup_bpython():
    import bpython
    bpython.embed()


def run():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__description__))
    parser.add_argument("-s", "--shell", choices=SHELLS, default="python",
                        help="Choose a shell interface {default is 'python'}")
    parser.add_argument("-a", "--addr", default="127.0.0.1",
                        help="dmon host address {default 127.0.0.1}")
    parser.add_argument("-p", "--port", default=7689, type=int,
                        help="dmon host port {default 7689}")
    parser.add_argument("--protocol", choices=["json"], default="json",
                        help="Protocol to test with {default 'json'}")
    args = parser.parse_args()

    setup_env(args)

    if args.shell == "python":
        setup_plain()
    elif args.shell == "ipython":
        setup_ipython()
    elif args.shell == "bpython":
        setup_bpython()


if __name__ == "__main__":
    run()
