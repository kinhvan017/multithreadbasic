import threading
import shlex
import socket
import struct
import subprocess
import sys
from Queue import Queue


PORTS = {
    22: 'Linux',
    139: 'Windows',
}

CHECK_CMD = 'ping -n 1 -t 100 ' if sys.platform.startswith('win') \
                    else 'ping -c 1 -W 1 '


def usage():
    print 'Usage: ' + sys.argv[0] + ' subnet'
    print 'Example:' + sys.argv[0] + ' 192.168.1.0/24'
    sys.exit(1)


def ip2int(ip_string):
    """Convert string repesent an IP to 32-bit integer

    Args:
        ip_string: The string represent an IP
    Returns:
        Int -- The integer represent IP
    """
    return struct.unpack('!I', socket.inet_aton(ip_string))[0]

def int2ip(ip_int):
    """Convert an integer represent an IP to string IP

    Args:
        ip_int: The string represent
    Returns:
        Str -- The string represent IP
    """
    return socket.inet_ntoa(struct.pack('!I', ip_int))

def subnet2ips(subnet):
    """Generator to get all IPs in a subnet

    Args:
        subnet: The subnet with prefix, eg: 192.168.1.0/24
    Returns:
        A generator object, yield IP in subnet
    """
    net_addr, net_mask = subnet.split('/')
    inverse_mask = 1 << (32 - int(net_mask))

    net_addr = ip2int(net_addr)
    for i_mask in range(1, inverse_mask-1):
        yield int2ip(net_addr | i_mask)

def is_tcp_port_open(host, port):
    """Check if a TCP port is open

    Args:
        host: Host to check
        port: Port to check
    Returns:
        Boolean -- True if port open, else False
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False


def is_host_alive(host):
    """Check if host if up, using ping utility

    Args:
        host: Host to check
    Returns:
        Boolean -- True if host is up, else False
    """
    cmd = CHECK_CMD + host
    ret_code = subprocess.call(shlex.split(cmd), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if ret_code:
        return False
    else:
        return True


def print_msg(host, os):
    """Print message with host and OS type"""
    print 'Host {0} is {1}'.format(host, os)


def worker(q):
    """A worker for checking host type"""
    while 1:
        host = q.get()
        for port in PORTS:
            if is_tcp_port_open(host, port):
                print_msg(host, PORTS[port])
                break
        else:
            if is_host_alive(host):
                print_msg(host, 'unknow')
        q.task_done()

def main():
    try:
        subnet = sys.argv[1]
    except IndexError:
        usage()

    q = Queue(maxsize=0)
    num_threads = 500
    for _ in range(num_threads):
        w = threading.Thread(target=worker, args=(q,))
        w.setDaemon(True)
        w.start()

    for host in subnet2ips(subnet):
        q.put(host)

    q.join()


if __name__ == '__main__':
    main()
