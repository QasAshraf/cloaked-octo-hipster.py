import sys
from server import MyServer

# TODO: Check we only have two arguments

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# TODO: Expose the different types of server, we should be able to choose what type of server we are creatting
# Create an echo server.
server = MyServer()

# Start server
server.start(ip, port)