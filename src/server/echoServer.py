from src.common.server import Server

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