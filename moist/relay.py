import RPi.GPIO as GPIO
import time
from multiprocessing import Process, SimpleQueue
import serverClient as serv

dataQueue = SimpleQueue()

clientProcess = Process(target=serv.sendFromQueue, args=(dataQueue,))
clientProcess.start()

def sendData(opcode, data):
    toSend = []
    toSend.append(opcode)
    toSend.extend(data)
    dataQueue.put(toSend)
    print("Put data: {}".format(toSend))

GPIO.setmode(GPIO.BCM)

relay_pins = [4,3,17,27,11,10,22,9,2]
opcodes = [0x32, 0x33, 0x3e, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x40]
valve_default_state = [0,0,0,1,1,1,0,0,0]

for a in range(0,9):
    GPIO.setup(relay_pins[a], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def my_callback(channel):
    time.sleep(0.1)
    relay_data = GPIO.input(channel)
    index = relay_pins.index(channel)
    if relay_data == 1:
        if valve_default_state[index] == 0:
            data = 0
        else:
            data = 1
    if relay_data == 0:
        if valve_default_state[index] == 0:
            data = 1
        else:
            data = 0
    print(channel)
    sendData(opcodes[index], [data])

for b in range(0,9):
    GPIO.add_event_detect(relay_pins[b], GPIO.BOTH, callback=my_callback, bouncetime=300)

#main begins here
serv.connect('arescdh', 9999)

