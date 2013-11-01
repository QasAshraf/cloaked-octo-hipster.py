"""

Network server skeleton.

This shows how you can create a server that listens on a given network socket, dealing
with incoming messages as and when they arrive. To start the server simply call its
start() method passing the IP address on which to listen (most likely 127.0.0.1) and 
the TCP port number (greater than 1024). The Server class should be subclassed here, 
implementing some or all of the following five events. 

  onStart(self)
      This is called when the server starts - i.e. shortly after the start() method is
      executed. Any server-wide variables should be created here.
      
  onStop(self)
      This is called just before the server stops, allowing you to clean up any server-
      wide variables you may still have set.
      
  onConnect(self, socket)
      This is called when a client starts a new connection with the server, with that
      connection's socket being provided as a parameter. You may store connection-
      specific variables directly in this socket object. You can do this as follows:
          socket.myNewVariableName = myNewVariableValue      
      e.g. to remember the time a specific connection was made you can store it thus:
          socket.connectionTime = time.time()
      Such connection-specific variables are then available in the following two
      events.

  onMessage(self, socket, message)
      This is called when a client sends a new-line delimited message to the server.
      The message paramater DOES NOT include the new-line character.

  onDisconnect(self, socket)
      This is called when a client's connection is terminated. As with onConnect(),
      the connection's socket is provided as a parameter. This is called regardless of
      who closed the connection.

"""

import socket as socketlib
import threading

from src.common import Receiver


class Server(Receiver):
    def start(self, ip, port):
        # Set up server socket
        serversocket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
        serversocket.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
        serversocket.bind((ip, int(port)))
        serversocket.listen(10)
        serversocket.settimeout(1)

        # On start!
        self.onStart()

        # Main connection loop
        threads = []
        while self.isRunning():
            try:
                (socket, address) = serversocket.accept()
                thread = threading.Thread(target=self, args=(socket,))
                threads.append(thread)
                thread.start()
            except socketlib.timeout:
                pass
            except:
                self.stop()

        # Wait for all threads
        while len(threads):
            threads.pop().join()

        # On stop!
        self.onStop()

    def onStart(self):
        pass

    def onStop(self):
        pass


# Create an echo server class
class EchoServer(Server):
    def onStart(self):
        print "Echo server has started"

    def onMessage(self, socket, message):
        # This function takes two arguments: 'socket' and 'message'.
        #     'socket' can be used to send a message string back over the wire.
        #     'message' holds the incoming message string (minus the line-return).

        # convert the string to an upper case version
        message = message.upper()
        # Just echo back what we received
        socket.send(message)

        # Signify all is well
        return True


# Create an ego server class
class EgoServer(Server):
    def onStart(self):
        self.colour = 'red'
        print 'Ego server has started'

    def onMessage(self, socket, message):
        # Egomaniacally deal with an incoming message.

        # Ignore the message, and tell your adoring fan your favourite colour
        socket.send("My favourite colour is %s\n" % self.colour)

        # Disconnect!
        return False


class MyServer(Server):
    def onStart(self):
        self.clients = 0
        self.names = {}
        self.sockets = []
        print "My server has started"

    def onMessage(self, socket, message):
        (command, sep, parameter) = message.strip().partition(' ')
        print "Command is " + command
        print "Message is " + parameter

        if command == "MESSAGE":
            (name, sep, message) = parameter.strip().partition(' ')
            if self.names.has_key(name):
                senderName = socket.name
                sendSocket = self.names[name]
                sendSocket.send(senderName + " says: " + message)
            else:
                socket.send("this person doesn't exist")
        elif command == "SETNAME":
            if self.names.has_key(parameter):
                socket.send("Name already exists")
            else:
                name = socket.name
                socket.name = parameter
                del self.names[name]
                self.names[parameter] = socket
                socket.send("Name changed to: " + parameter)
        elif command == "REGESTER":
            socket.name = parameter
            self.names[parameter] = socket
            for i in self.sockets:
                if i != socket:
                    name = socket.name
                    i.send(name + " has connected")
        else:
            for i in self.sockets:
                if i != socket:
                    name = socket.name
                    i.send(name + " says: " + message)
        return True

    def onConnect(self, socket):
        print "Client connected"
        self.clients = self.clients + 1
        print "There are " + str(self.clients) + " clients"
        self.sockets.append(socket)
        socket.send("Welcome!")
        socket.send("SETNAME <username> - will change your username")
        socket.send("MESSAGE <username> <message> - will send a message to a specific user")


    def onDisconnect(self, socket):
        print "Client disconnected"
        self.clients = self.clients - 1
        print "There are " + str(self.clients) + "clients"
        for i in self.sockets:
            if i != socket:
                name = socket.name
                i.send(name + " has disconnected")

    def onStop(self):
        print "Server closed"
