import tornado.ioloop

from tornado.options import define, options

import pbserver


define("datagram_host", default="127.0.0.1", help="Receive host for event datagrams")
define("datagram_port", default=7890, help="Receive port for event datagrams")


def main():
    options.parse_command_line()

    print("Starting datagram listener on:", options.datagram_host, options.datagram_port)

    pbserver.setup()

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == "__main__":
    main()
