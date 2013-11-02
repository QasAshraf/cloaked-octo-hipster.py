import sys
from src.server.customServer import MyServer

total = len(sys.argv)
if total != 3:
    print ("Usage: python myServer.py <ip> <port>")
    sys.exit(0)


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# TODO: Expose the different types of server, we should be able to choose what type of server we are creating
# Create an echo server.
server = MyServer()

# Start server
server.start(ip, port)