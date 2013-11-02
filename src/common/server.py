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

from src.common.common import Receiver


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