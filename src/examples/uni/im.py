import sysfrom ex3 import Server# Create an echo server classclass EchoServer(Server):	def onStart(self):		print "Echo server has started"			def onMessage(self, socket, message):		# This function takes two arguments: 'socket' and 'message'.		#     'socket' can be used to send a message string back over the wire.		#     'message' holds the incoming message string (minus the line-return).			# convert the string to an upper case version		message = message.upper()		# Just echo back what we received		socket.send(message)				# Signify all is well		return True# Create an ego server classclass EgoServer(Server):	def onStart(self):		self.colour = 'red'		print 'Ego server has started'	def onMessage(self, socket, message):		# Egomaniacally deal with an incoming message.		# Ignore the message, and tell your adoring fan your favourite colour		socket.send("My favourite colour is %s\n" % self.colour)				# Disconnect!		return False

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
# Parse the IP address and port you wish to listen on.ip = sys.argv[1]port = int(sys.argv[2])# Create an echo server.server = MyServer()# If you want to be an egomaniac, comment out the above command, and uncomment the# one below...#server = EgoServer()# Start serverserver.start(ip, port)import time


class IRCClient(Client):

	def onMessage(self, socket, message):
		print message
		# *** process incoming messages here ***
		return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

# *** register your client here, e.g. ***
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
