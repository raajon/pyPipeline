#-------------------------------------------#
# File name: pyPipeline.py
# copyright 2017 Ignacy Niwald
# license LGPL
#-------------------------------------------#


import socket
import sys
import thread
import time
import argparse

parser = argparse.ArgumentParser(description='Open any number of sockets on declared ports and create pipe between them.')
parser.add_argument('ports', metavar='N', type=int, nargs='+', help='Ports to open')
parser.add_argument("-l", help="just localports", action="store_true")
parser.add_argument("-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()

print args

connections = [None] * len(args.ports)
verbose = args.v
local = args.l

def connection(i, port):
    global connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    if local:
        server_address = ('127.0.0.1', port)
    else:
        server_address = ('0.0.0.0', port)

    if verbose:
        print 'starting up on %s port %s' % server_address
    try:
        sock.bind(server_address)
    except socket.error:
        print >> sys.stderr, 'Port %s already in use' % port

    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        connections[i], client_address = sock.accept()

        try:
            if verbose:
                print 'connection from {0} on port {1}'.format(client_address, port)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connections[i].recv(16)
                if verbose:
                    print 'received "{0}" on port {1} from {2}'.format(data.rstrip(), port, client_address)
                if data:
                    for j in range(0, len(connections)):
                        if i!=j and connections[j]:
                            connections[j].sendall(data)
                else:
                    if verbose:
                        print 'no more data from', client_address
                    break

        finally:
            # Clean up the connection
            connections[i].close()
            connections[i] = None
            print 'end connection from {0} on port {1}'.format(client_address, port)


for i in range(0, len(args.ports)):
    thread.start_new_thread(connection,(i, args.ports[i]))

try:
    while True:
            time.sleep(5)
except:
    for i in range(0, len(args.ports)):
        if connections[i]:
            connections[i].close()
            connections[i]=None

