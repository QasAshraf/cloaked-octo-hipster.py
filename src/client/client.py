import threading
import time
import socket as socketlib

class Socket():
	"""
	Mutable wrapper class for sockets.
	"""

	def __init__(self, socket):
		# Store internal socket pointer
		self._socket = socket
	
	def send(self, msg):
		# Ensure a single new-line after the message
		self._socket.send("%s\n" % msg.strip())
		
	def close(self):
		self._socket.close()
		
class Receiver():
	"""
	A class for receiving newline delimited text commands on a socket.
	"""

	def __init__(self):
		# Protect access
		self._lock = threading.RLock()
		self._running = True

	def __call__(self, socket):
		"""Called for a connection."""
		# Set timeout on socket operations
		socket.settimeout(1)

		# Wrap socket for events
		wrappedSocket = Socket(socket)
		
		# Store the unprocessed data
		stored = ''
		chunk = ''
		
		# On connect!
		self._lock.acquire()
		self.onConnect(wrappedSocket)
		self._lock.release()
		
		# Loop so long as the receiver is still running
		while self.isRunning():
		
			# Take everything up to the first newline of the stored data
			(message, sep, rest) = stored.partition('\n')
			if sep == '': # If no newline is found, store more data...
				while self.isRunning():
					try:
						chunk = ''
						chunk = socket.recv(1024)
						stored += chunk
						break
					except socketlib.timeout:
						pass
					except:
						print 'EXCEPTION'
				
				# Empty chunk means disconnect
				if chunk == '':
					break;

				continue
			else: # ...otherwise store the rest
				stored = rest			
				
			# Process the command
			self._lock.acquire()
			success = self.onMessage(wrappedSocket, message)
			self._lock.release()
			
			if not success:
				break;

		# On disconnect!
		self._lock.acquire()
		self.onDisconnect(wrappedSocket)		
		self._lock.release()
		socket.close()
		del socket
		
		# On join!
		self.onJoin()
			
	def stop(self):
		"""Stop this receiver."""
		self._lock.acquire()
		self._running = False
		self._lock.release()
		
	def isRunning(self):
		"""Is this receiver still running?"""
		self._lock.acquire()
		running = self._running
		self._lock.release()
		return running
		
	def onConnect(self, socket):
		pass

	def onMessage(self, socket, message):
		pass

	def onDisconnect(self, socket):
		pass

	def onJoin(self):
		pass
		
class Client(Receiver):
	
	def start(self, ip, port):
		# Set up server socket
		self._socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
		self._socket.settimeout(1)
		self._socket.connect((ip, int(port)))

		# On start!
		self.onStart()

		# Start listening for incoming messages
		self._thread = threading.Thread(target = self, args = (self._socket,))
		self._thread.start()
		
	def send(self, message):
		# Send message to server
		self._lock.acquire()
		self._socket.send("%s\n" % message.strip())
		self._lock.release()
		time.sleep(0.5)

	def stop(self):
		# Stop event loop
		Receiver.stop(self)
		
		# Join thread
		if self._thread != threading.currentThread():
			self._thread.join()
		
		# On stop!
		self.onStop()		

	def onStart(self):
		pass

	def onStop(self):
		pass
		
	def onJoin(self):
		self.stop()

		
class IRCClient(Client):

	def onMessage(self, socket, message):
		print message
		# *** process incoming messages here ***
		return True
