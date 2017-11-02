import commandHandler as ch
import serialHandler as sh
import TCPServer

serverThread = TCPServer.getServerThread('0.0.0.0', 9999);
serverThread.start();
