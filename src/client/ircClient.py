from src.common.client import Client

class IRCClient(Client):
    def onMessage(self, socket, message):
        print message
        # *** process incoming messages here ***
        return True