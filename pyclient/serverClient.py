from multiprocessing import Queue, SimpleQueue, Process
import socket
import sys

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataQueue = SimpleQueue()

def connect(HOST, PORT):
    #connect to server and send data
    sock.connect((HOST, PORT))
    global connected

def sendFromQueue(queue):
    while True:

        if not queue.empty():
            data=queue.get()
            sock.sendall(bytearray(data))
            print("Sent:    {}".format(data))

            received = sock.recv(1024)

            if not received:
                print("No data received: check socket connection")
                break

            print("Received: {}".format(received))

    print("Socket connection closed")

def send(toSend):
    dataQueue.put(toSend)
    #print("event-raw> Send data: 0x{}".format(bytearray(toSend).hex()))

clientProcess = Process(target=sendFromQueue, args=(dataQueue,))
clientProcess.start()
