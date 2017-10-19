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
parser.add_argument("-e", help="echo mode", action="store_true")
parser.add_argument("-v", help="output verbosity", action="store_true")
parser.add_argument("-vv", help="increase output verbosity", action="store_true")
parser.add_argument("-vvv", help="increase output verbosity", action="store_true")
args = parser.parse_args()

servers = []
verbose3 = args.vvv
verbose2 = args.vv or args.vvv
verbose1 = args.v or args.vv or args.vvv

local = args.l
echo = args.e



class Server:

    def __init__(self, port):
        self.port = port
        self.clients = []
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error, msg:
            print >> sys.stderr, "Could not create socket. Error Code: {0} Error: {1}".format(str(msg[0]), msg[1])
            sys.exit(0)

        # Bind the socket to the port
        if local:
            server_address = ('127.0.0.1', port)
        else:
            server_address = ('0.0.0.0', port)

        if verbose2:
            print 'starting up on %s port %s' % server_address
        try:
            self.sock.bind(server_address)
        except socket.error:
            print >> sys.stderr, 'Port %s already in use' % port
            sys.exit(0)
        self.sock.listen(1)

    def server_thread(self):
        while True:
            connection, client_address = self.sock.accept()
            client = Client(self.port, connection, client_address)
            self.clients.append(client)
    def kill(self):
        for client in self.clients:
            client.kill()
            client = None


class Client:
    global servers
    connection = None
    port = 0
    client_address = None

    def __init__(self, port, connection, client_address):
        self.port = port
        self.connection = connection
        self.client_address = client_address
        thread.start_new_thread(self.client_thread, ())

    def client_thread(self):
        while True:
            # Wait for a connection
            try:

                if verbose2:
                    print 'connection from {0} on port {1}'.format(self.client_address, self.port)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = self.connection.recv(16)
                    if verbose3:
                        print 'received "{0}" on port {1} from {2}'.format(data.rstrip(), self.port, self.client_address)
                    if data:
                        for server in servers:
                            for client in server.clients:
                                if client != self or echo:
                                    client.send(data)
                    else:
                        if verbose2:
                            print 'no more data from', self.client_address
                        # break
            # except:
            #     print 'connection timeout on port {0}'.format(self.port)
            #     # break
            finally:
                if self.connection:
                    self.connection.close()
                    self.connection = None
                print 'end connection on port {0}'.format(self.port)
                break

    def send(self, data):
        try:
            self.connection.sendall(data)
        except socket.error, msg:
            print >> sys.stderr, "Data could not be send. Error Code: {0} Error: {1}".format(str(msg[0]), msg[1])

    def kill(self):
        if self.connection:
            self.connection.close()
            self.connection = None


for i in range(0, len(args.ports)):
    serv = Server(args.ports[i])
    servers.append(serv)
    thread.start_new_thread(serv.server_thread,())

try:
    while True:
        time.sleep(60)
        for serv in servers:
            if verbose2:
                print "Server on port {0} has {1} active connections.".format(serv.port, len(serv.clients))
except:
    for server in servers:
        server.kill()
        server = None

