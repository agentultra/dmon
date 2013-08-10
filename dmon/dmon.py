import argparse
import eventlet


import event
import server


parser = argparse.ArgumentParser(description="dmon distributed cluster monitor")

parser.add_argument("--udp_host", type=str, default="127.0.0.1",
                    help="The host to listen for event datagrams")
parser.add_argument("--udp_port", type=int, default="7689",
                    help="The port to listen fro event datagrams")
parser.add_argument("--max_connections", type=int, default=500,
                    help="The maximum number of socket connections.")
parser.add_argument("--threadpool_size", type=int, default=1000,
                    help="The maximum number of green threads to run.")


def main():
    args = parser.parse_args()
    eventlet.spawn(
        server.start_datagram_server(args.max_connections,
                                     args.udp_host,
                                     args.udp_port)
    )

if __name__ == "__main__":
    main()
