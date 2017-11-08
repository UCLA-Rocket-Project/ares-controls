import serialHandler
import TCPServer


serialPorts = serialHandler.RIGHT_PORTS

for port in serialPorts:
    result = serialHandler.getHandler().connect(port, timeout=0, wait=2)
    if result:
        print("SERIAL> Successfully connected to device at port {}".format(port))
    else:
        print("SERIAL> Error connecting to device at port {}".format(port))


serverThread = TCPServer.getServerThread('0.0.0.0', 9999)
serverThread.daemon = True
serverThread.start()

print("TCP-SERVER> Started server")

serverThread.join()
