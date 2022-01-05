import argparse
import socket
import sys
import threading
import time


class ShellListener(threading.Thread):

    def __init__(
        self, 
        listening_ip, 
        listening_port, 
        buffer=1024, 
        connections=1, 
        timeout=10, 
        verbose=True
        ):
        """
        Initializes the constructor for the ShellListner.
        
        :param listening_ip: IP address to listen on
        :type listening_ip: str
        :param listening_port: Port to listen on
        :type listening_port: int
        :param buffer: The maximum amount of data to be received at once
        :type buffer: int
        :param connections: Number of connections to accept before refusing new connections
        :type connections: int
        :param timeout: Timeout (in seconds) to wait for a connection
        :type timeout: int/float
        :param verbose: Print when listening and a connection is made
        :type verbose: bool
        """
        super().__init__(daemon=True)
        
        self._shutdown = False
        self.addr = None  # the address bound to the socket on the other end of the connection
        self.conn = None  # the socket object usable to send and receieve data on the connection
        self.buffer = buffer  # buffer size should be a relatively small power of 2
        self.connections = connections  # number of connections to listen before
        self.listening_ip = listening_ip
        self.listening_port = listening_port
        self.verbose = verbose

        self.sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        
        self.sock.settimeout(timeout)

    def listen(self):
        """Binds socket."""
        try:
            self.sock.bind((self.listening_ip, self.listening_port))
        except Exception as e:
            if self.verbose:
                print(e)
            self._shutdown = True
            return

        self.sock.listen(self.connections) 

        if self.verbose:
            print(f"Listening on {self.listening_ip}:{self.listening_port}")
        
        try:
            self.conn, self.addr = self.sock.accept()
        except Exception as e:
            if self.verbose:
                print(e)
            self._shutdown = True
            return

        if self.verbose:
            print(f"Connection received from {self.addr}")
    
    def stop(self):
        """Close out the socket connection."""
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        
    def run(self):
        """Run loop for the thread."""
        self.listen()
        
        # Loop starts once a connection is made.
        while True:
            if self._shutdown:
                self.stop()
                break

            if self.conn and self.addr:
                # Receive data from the target and get user input
                data_recv = self.conn.recv(self.buffer).decode()
                sys.stdout.write(data_recv)
                command = input()

                # Send a command, check if command sent is requesting the shell to close
                if command.lower() == "quit" or command.lower() == "exit" or command.lower() == "close":
                    self._shutdown = True
                    continue
                
                command += "\n"
                self.conn.send(command.encode())
                time.sleep(1)

            # Remove the output of the "input()" function
            sys.stdout.write("\033[A" + data_recv.split("\n")[-1])


def main():
    """Parse arguments and start a shell listener."""
    parser = argparse.ArgumentParser(add_help=True,
                                     description='Utility that mimics a netcat listener.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'listen_ip', 
        type=str, 
        help='IP address to listen on.'
    )

    parser.add_argument(
        'listen_port', 
        type=int,
        help="Port to listen on."
    )

    parser.add_argument(
        '--buffer', 
        type=int, 
        default=1024, 
        help="The maximum amount of data to be received at once. Buffer size should be a relatively small power of 2."
    )

    parser.add_argument(
        '--connections', 
        type=int, 
        default=1, 
        help="Number of connections to accept before refusing new connections."
    )

    parser.add_argument(
        '--timeout', 
        type=int, 
        default=10, 
        help="Timeout (in seconds) to wait for a connection."
    )

    parser.add_argument(
        '--verbose', 
        type=bool, 
        default=True, 
        help="Displays output when listening and a connection is made."
    )

    args = parser.parse_args()
    
    s = ShellListener(
        args.listen_ip, 
        args.listen_port,
        buffer=args.buffer,
        connections=args.connections,
        timeout=args.timeout,
        verbose=args.verbose
    )

    s.setDaemon(True)
    s.start()
    s.join()       


if __name__ == '__main__':
    main()
