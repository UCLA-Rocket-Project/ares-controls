from multiprocessing import Queue
import socket
import sys

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(HOST, PORT):
    #connect to server and send data
    sock.connect((HOST, PORT))

def send(data):
    sock.sendall(bytearray(data))
    print("Sent:    {}".format(data))

    received = sock.recv(1024)

    if not received:
        print("No data received: check socket connection")
    break

    print("Received: {}".format(received))

    print("Socket connection closed")

ops = {}
