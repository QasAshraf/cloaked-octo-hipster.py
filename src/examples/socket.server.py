import socket
import sys
from thread import *

HOST = ''
PORT = 8889

# IPv4 TCP stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created.'


try:
    sock.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + ', '
    print 'Message: ' + str(msg[1])
    sys.exit()

print 'Binded successfully.'

sock.listen(10) # Only allow 10 connections on the backlog
print 'Listening.'

# Function which handles the connection
def clientHandler(conn):
    conn.send('Welcome to our server, type summat and hit enter! \n')

    while True:
        data = conn.recv(1024)
        reply = 'OK... ' + data
        if not data:
            break

        conn.sendall(reply)
    conn.close()
# -- end clientHandler

# Keep talking!!
while 1:
    conn, addr = sock.accept() # Waiting to accept a connection
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientHandler, (conn,))

conn.close()
sock.close()
