# Socket client example in Python
import socket
import sys

try:
    # Create an IPv4, TCP stream
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ', '
    print 'Error message: ' + msg[1]
    sys.exit()

print 'Socket connected :D'

host = 'www.google.com'
port = 80

try:
    ip = socket.gethostbyname(host)

except socket.gaierror:
    print 'Could not resolve hostname, exiting'
    sys.exit()

print 'IP of ' + host + ' is ' + ip

# Connect to server
sock.connect((ip, port))

print 'Connected using a socket to ' + host + ' on ' + ip

request = "GET / HTTP/1.1\r\n\r\n"

try:
    sock.sendall(request)
except socket.errror:
    print 'Send failed :('
    sys.exit()

print 'Send that message succesfully!'

response = sock.recv(4096)

print response

sock.close() # close down connection once we're done