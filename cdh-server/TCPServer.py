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
            deviceString = ', '.join(sh.getConnectedPorts())
            return True, str.encode('[' + deviceString + ']')

        elif opcode == opcodes.CONNECT_DEVICE:
            try:
                port = data[1:data.index(b'\x00')].decode('ascii')
                print('   cdh-command #> attempting serial connection to {}'.format(port))
                result = serialHandler.getHandler().connect(port)
                print('   cdh-command #> connection attempt success? -> {}'.format(result))
                return True, str.encode('Opening serial connection to port {} success? {}' \
                    .format(port, result))
            except Exception as e:
                print('   cdh-command #> handling exception: {}'.format(e))
                return False, str.encode('Unknown error processing data: ' + e)
        else:
            return False, b'Invalid CDH Opcode'

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
