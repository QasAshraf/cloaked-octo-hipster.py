import time
import socket as socketlib
import threading
import sys
from common import Receiver


class Client(Receiver):
    def start(self, ip, port):
        # Set up server socket
        try:
            self._socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
            self._socket.settimeout(1)
            self._socket.connect((ip, int(port)))
        except socketlib.timeout:
            print("Socket timed out, is the server running?")
            sys.exit(0)

        # On start!
        self.onStart()

        # Start listening for incoming messages
        self._thread = threading.Thread(target=self, args=(self._socket,))
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

