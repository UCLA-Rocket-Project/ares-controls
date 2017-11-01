import socketserver
import commandHandler as ch
from threading import Thread

class TCPServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Connection from {}".format(self.client_address[0]))
        while(1):
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024)
            if not self.data:
                break
            print("got data: " + self.data)
            print("first byte: " + hex(ord(self.data[0])))
            response = ch.handleCommand(self.data)
            self.request.sendall(response)
        print("Client disconnected: {}".format(self.client_address[0]))

def getServerThread(HOST, PORT):
    server = socketserver.TCPServer((HOST, PORT), TCPServerHandler)
    t = Thread(target=server.serve_forever())
    return t
