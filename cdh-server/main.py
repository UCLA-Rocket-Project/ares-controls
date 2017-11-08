import serialHandler
import TCPServer


serialPorts = ["/dev/ttyACM0", "/dev/ttyACM1"]

for port in serialPorts:
    result = serialHandler.getHandler().connect(port, timeout=0, delay=2)
    if result:
        print("Successfully connected to device at port {}".format(port))
    else:
        print("Error connecting to device at port {}".format(port))

serverThread = TCPServer.getServerThread('0.0.0.0', 9999)
serverThread.daemon = true
serverThread.start()
