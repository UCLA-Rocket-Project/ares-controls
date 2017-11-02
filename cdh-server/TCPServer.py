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
                continue

            addr = mcuCommand.pop(0)
            opcode = mcuCommand.pop(0)
            response = sh.fcmHandler.sendDataToMCU(addr, opcode, mcuCommand)
            responseTwo = sh.gcmHandler.sendDataToMCU(addr, opcode, mcuCommand)
            response.extend(responseTwo)

            self.request.sendall(response)
        # outside of while loop
        print("Client disconnected: {}".format(self.client_address[0]))

def getServerThread(HOST, PORT):
    server = socketserver.TCPServer((HOST, PORT), TCPServerHandler)
    t = Thread(target=server.serve_forever())
    return t
