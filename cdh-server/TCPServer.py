from threading import Thread
import sys
import socketserver

import serialHandler
from libares import opcodes
import commandHandler as ch

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
                    print("  tcph #> Error handling CDH command", file=sys.stderr)
                self.request.sendall(response)
            #if mcuCommand:
            else:
                success, response = self.handleMCUCommand(self.data)
                if not success:
                    print("  tcph #> Error handling MCU command", file=sys.stderr)
                self.request.sendall(response)

        # outside of while loop
        print("  tcp #> Client disconnected: {}".format(self.client_address[0]), file=sys.stderr)

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
                if result:
                    print('   cdh-command #> connection attempt success!')
                else:
                    print('   cdh-command #> connection attempt unsuccessful', file=sys.stderr)
                return True, str.encode('Opening serial connection to port {} success? {}' \
                    .format(port, result))
            except Exception as e:
                print('   cdh-command #> handling exception: {}'.format(e), file=sys.stderr)
                return False, str.encode('Unknown error processing data: ' + e)
        else:
            return False, b'Invalid CDH Opcode'

    def handleMCUCommand(self, data):
        mcuCommand = ch.handleCommand(data)
        print("  tcp #> MCU Command: {}".format(mcuCommand))

        if(mcuCommand == ch.ERROR):
            print("  tcph $> Bad Request")
            return False, b'Error bad request!' # success, response
        addr = mcuCommand.pop(0)
        opcode = mcuCommand.pop(0)

        attemptCount = 0
        mcuResponse = []
        errorCode = b''
        retry = True

        while retry and attemptCount < 5:
            mcuResponses = sh.sendDataToMCUs(addr, opcode, mcuCommand)
            tcpResponse = b' '.join(mcuResponses)

            retry = False
            attemptCount += 1
            for response in mcuResponses:
                if response[0] == b'\xc0': # pi address, success = 0
                    retry = True
                    print("  tcp #> Received error code: {}".format(response), file=sys.stderr)
                    errorCode = b'Received error code: ' + response
            if tcpResponse == b'':
                print("  tcp #> Nothing from MCU's", file=sys.stderr)
                errorCode = b'No response from MCUs'
                retry = True

            if not retry:
                return True, b'Success: ' + tcpResponse # success, response

        print("  tcph #> Failed 5 attempts")
        return False, errorCode # only get this far if attemptCount = 5


def getServerThread(HOST, PORT):
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), TCPServerHandler)
    t = Thread(target=server.serve_forever)
    print("  tcp #> Created server thread at {}:{}".format(HOST, PORT))
    return t
