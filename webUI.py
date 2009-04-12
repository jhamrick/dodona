import socket
import threading
import SocketServer

socket.setdefaulttimeout(10)

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        """recieves statement from the user """
        print "handling request..."
        # self.request is the TCP socket connected to the client
        try:
            self.userspeak = self.request.recv(1024).strip()
        except socket.timeout:
            print 'socket timed out'
            return
        print "%s wrote:" % self.client_address[0]
        print self.userspeak
        dodonaspeak=self.respond(self.userspeak)
        # just send back the same data, but upper-cased
        self.request.send(dodonaspeak)

    def wordwrap(self,statement,numchars=70):
        if len(statement)>numchars:
            return statement[0:79]+'\n'+self.wordwrap(statement[79:])
        else:
            return statement

    def respond(self,statement):
        return self.wordwrap("I don't know anything about "+str(statement)+" please ask again.")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "18.111.23.79", 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    #server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    #server_thread.setDaemon(True)
    #server_thread.start()
    print "Server daemon started..."
    server.serve_forever()


