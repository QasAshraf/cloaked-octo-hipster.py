import sys
from customServer import CustomServer
from echoServer import EchoServer

total = len(sys.argv)
if total != 3:
    print ("Usage: python myServer.py <ip> <port>")
    sys.exit(0)


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

#server = CustomServer()
server = EchoServer()
#server = egoServer()

# Start server
server.start(ip, port)