# TCP chat server
import socket, select

# Broadcast function
def broadcast (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close();
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
    CONNECTION_LIST = []
    BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        sock_read, sock_write, sock_error = select.select(CONNECTION_LIST, [], [])
    
        for sock in sock_read:
            if sock == server_socket: # new connection
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

                broadcast(sockfd, "[%s:%s] joined the party\n" % addr)
            else: # incoming message
                try:
                    data = sock.recv(BUFFER)
                    if data:
                        broadcast(sock, "\r" + '<' + str(sock.getpeername()) + '>' + data)
                except:
                    broadcast(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    

    server_socket.close()