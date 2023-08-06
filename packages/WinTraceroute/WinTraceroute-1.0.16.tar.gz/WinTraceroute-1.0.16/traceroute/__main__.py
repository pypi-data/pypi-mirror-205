import argparse
from traceroute.traceroute import trace_udp, trace_icmp


def main() -> int:
    import logging
    logging.getLogger("scapy").setLevel(logging.WARNING)

    epilog = """See also RFC2151 section 3.4 for a quick
                read-up on traceroute."""
    parser = argparse.ArgumentParser(
                    prog='traceroute',
                    description="""Provides a mostly *NIX-traceroute-
                    like -- but very basic -- tracert/traceroute IPv4
                    alternative built on scapy.""",
                    epilog=epilog)
    parser.add_argument('remote_host', metavar='host', \
        help="""IP address or host name of the remote host
                which is the destination of the route.""")
    parser.add_argument('packet_length', metavar='packet_length', \
        nargs='?', default=2, \
        help="""size of the UDP packet to be sent.
                Note that this option has no effect in ICMP
                mode.""")
    parser.add_argument('-m', '--maxttl', '--max-hops', \
                        default=30, \
        help="""maximum allowable TTL value, measured as
                the number of hops allowed before the
                program terminates.
                (default = 30)""")
    parser.add_argument('-f', '--minttl', '--first', \
                        default=1, \
        help="""minimum TTL value, measured as the number
                of hops at which to start.
                (default = 1)""")
    parser.add_argument('-q', '--fleetsize', \
                        default=3, \
        help="""number of packets that will be sent
                with each time-to-live setting ("fleet size").
                (default = 3)""")
    parser.add_argument('-w', '--timeout', \
                        default=5, \
        help="""amount of time, in seconds, to wait for
                an answer from a particular router before
                giving up.
                (default = 5)""")
    parser.add_argument('-p', '-P', '--port', \
                        default=33434, \
        help="""destination port (invalid) at the remote
                host.
                Note that this option will have no effect in
                ICMP mode.
                (default = 33434)""")
    parser.add_argument('-s', '--source', \
                        default=None, \
        help="""source address of outgoing packets.
                (default is address of adapter used)""")
    parser.add_argument('-M', '--module', \
                        default='UDP', choices=['UDP', 'ICMP'], \
        help="""module (or method) for traceroute
                operations.
                (default = UDP)""")
    args = parser.parse_args()

    match args.module:
        case 'UDP':
            print()
            trace_udp(args.remote_host,
                udp_length=int(args.packet_length),
                min_ttl=int(args.minttl),
                max_ttl=int(args.maxttl),
                num_per_fleet=int(args.fleetsize),
                timeout=int(args.timeout),
                port=int(args.port),
                source=args.source)
        case 'ICMP':
            print("Note: ICMP mode is experimental.")
            print()
            trace_icmp(args.remote_host,
                min_ttl=int(args.minttl),
                max_ttl=int(args.maxttl),
                num_per_fleet=int(args.fleetsize),
                timeout=int(args.timeout),
                port=int(args.port),
                source=args.source)
        case _:
            print('Module ' + args.module + ' is not supported.')


main()
