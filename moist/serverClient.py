from multiprocessing import Queue
import socket
import sys

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(HOST, PORT):
    #connect to server and send data
    sock.connect((HOST, PORT))

def sendFromQueue(queue):
    while True:

        if not queue.empty():
            data=queue.get()
            sock.sendall(bytearray(data))
            print("Sent:    {}".format(data))

            received = sock.recv(1024)

            if not received:
                break

            print("Received: {}".format(received))

    print("Socket disconnection closed")


