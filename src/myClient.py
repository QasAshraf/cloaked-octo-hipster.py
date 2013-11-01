import sys
from src.client import IRCClient

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

# *** register your client here ***
client.send('REGESTER %s' % screenName)

while client.isRunning():
    try:
        command = raw_input("> ").strip()
        client.send(command)
    # *** process input from the user in a loop here ***
    # *** use client.send(someMessage) to send messages to the server
    except:
        client.stop();

client.stop()