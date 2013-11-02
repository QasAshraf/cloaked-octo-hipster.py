from src.common.server import Server

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