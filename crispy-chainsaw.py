from crispy_chainsaw.nc import ShellListener

import argparse


def main():
    """Parse arguments and start a shell listener."""
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Utility that mimics a netcat listener.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("listen_ip", type=str, help="IP address to listen on.")

    parser.add_argument("listen_port", type=int, help="Port to listen on.")

    parser.add_argument(
        "--buffer",
        type=int,
        default=1024,
        help="The maximum amount of data to be received at once. Buffer size should be a relatively small power of 2.",
    )

    parser.add_argument(
        "--connections", type=int, default=1, help="Number of connections to accept before refusing new connections."
    )

    parser.add_argument("--timeout", type=int, default=10, help="Timeout (in seconds) to wait for a connection.")

    parser.add_argument(
        "--verbose", type=bool, default=True, help="Displays output when listening and a connection is made."
    )

    args = parser.parse_args()

    s = ShellListener(
        args.listen_ip,
        args.listen_port,
        buffer=args.buffer,
        connections=args.connections,
        timeout=args.timeout,
        verbose=args.verbose,
    )

    s.daemon = True
    s.start()
    s.join()


if __name__ == "__main__":
    main()
