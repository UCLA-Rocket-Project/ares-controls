import socketserver
import serialHandler as sh
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
            print("got data: " + self.data.hex())
            print("first byte: " + hex(self.data[0]))

            mcuCommand = ch.handleCommand(self.data)
            print("MCU Command: {}".format(mcuCommand))

            if(mcuCommand == ch.ERROR):
                print("Error translating to MCU command")
                self.request.sendall("Error bad request!")
                continue

            addr = mcuCommand.pop(0)
            opcode = mcuCommand.pop(0)
            mcuCommandTwo = list(mcuCommand) # copy mcuCommand

            mcuResponse = sh.fcmHandler.sendDataToMCU(addr, opcode, mcuCommand)
            tcpResponse = b'-'.join(response)

            self.request.sendall(tcpResponse)
        # outside of while loop
        print("Client disconnected: {}".format(self.client_address[0]))

def getServerThread(HOST, PORT):
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), TCPServerHandler)
    t = Thread(target=server.serve_forever())
    return t
