from multiprocessing import Queue
import socket
import sys

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def connect(HOST, PORT):
    #connect to server and send data
    sock.connect((HOST, PORT))
    global connected
    connected = True

def send(data):
    global connected
    print("Sending data 0x{}".format(data.hex()))
    if not connected:
        print("Please call connect() first")
        return

    sock.sendall(bytearray(data))
    print("Sent:    {}".format(data))

    received = sock.recv(1024)

    if not received:
        print("No data received: check socket connection")
        connected = False
        return

    print("Received: {}".format(received))

    print("Socket connection closed")
