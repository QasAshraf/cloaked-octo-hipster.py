from server import Server

class CustomServer(Server):
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
        elif command == "REGISTER":
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
