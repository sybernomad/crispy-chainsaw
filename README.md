# crispy-chainsaw
Utility that runs the equivalent of `nc -l`. Can be used as a listener for TCP connectback shells.

# Usage
```
usage: shell_listener.py [-h] [--buffer BUFFER] [--connections CONNECTIONS] [--timeout TIMEOUT] [--verbose VERBOSE] listen_ip listen_port

Utility that mimics a netcat listener.

positional arguments:
  listen_ip             IP address to listen on.
  listen_port           Port to listen on.

optional arguments:
  -h, --help            show this help message and exit
  --buffer BUFFER       The maximum amount of data to be received at once. Buffer size should be a relatively small power of 2. (default: 1024)
  --connections CONNECTIONS
                        Number of connections to accept before refusing new connections. (default: 1)
  --timeout TIMEOUT     Timeout (in seconds) to wait for a connection. (default: 10)
  --verbose VERBOSE     Displays output when listening and a connection is made. (default: True)
```

# Legal Disclaimer
This project is made for educational and ethical testing purposes only. Usage of for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.
