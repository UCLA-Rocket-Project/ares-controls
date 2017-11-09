import socketserver
import serialHandler
import opcodes
import commandHandler as ch
from threading import Thread

sh = serialHandler.getHandler()

class TCPServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("  tcp #> Connection from {}".format(self.client_address[0]))
        while(1):
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024)
            if not self.data: break # end connection
            print("  tcp #> got data: " + self.data.hex())

            #if cdhCommand:
            if ((self.data[0] & 0xc0) == 0xc0):
                success, response = self.handleCDHCommand(self.data)
                if not success:
                    print("  tcph #> Error handling CDH command")
                self.request.sendall(response)
            #if mcuCommand:
            else:
                success, response = self.handleMCUCommand(self.data)
                if not success:
                    print("  tcph #> Error handling MCU command")
                self.request.sendall(response)

        # outside of while loop
        print("  tcp #> Client disconnected: {}".format(self.client_address[0]))

    def handleCDHCommand(self, data):
        opcode = data[0]
        if opcode == opcodes.GET_CONNECTED_DEVICES:
            deviceString = ", ".join(sh.getConnectedPorts())
            return True, "Connected Devices: " + deviceString
        elif opcode == opcodes.CONNECT_DEVICE:
            try:
                portBytes = data[1:data.index('\x00')]
                port = ''.join(portBytes).decode('utf-8')
                result = serialHandler.getHandler().connect(port)
                return True, "Opening serial connection to port {}".format(port) \
                    + "succeeded" if result else "failed"
            except:
                return False, "Unknown error processing data"
        else:
            return False, "Invalid CDH Command"

    def handleMCUCommand(self, data):
        mcuCommand = ch.handleCommand(data)
        print("  tcp #> MCU Command: {}".format(mcuCommand))

        if(mcuCommand == ch.ERROR):
            return False, "Error bad request!" # success, response
        addr = mcuCommand.pop(0)
        opcode = mcuCommand.pop(0)

        mcuResponse = sh.sendDataToMCUs(addr, opcode, mcuCommand)
        tcpResponse = b'-'.join(mcuResponse)
        if(tcpResponse == b''):
            print("  tcp #> Nothing from MCU's")
            tcpResponse = b'no response from MCUs'
        return True, tcpResponse # success, response


def getServerThread(HOST, PORT):
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), TCPServerHandler)
    t = Thread(target=server.serve_forever)
    print("  tcp #> Created server thread at {}:{}".format(HOST, PORT))
    return t
