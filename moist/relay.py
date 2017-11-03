import RPi.GPIO as GPIO
import time
from multiprocessing import Process, SimpleQueue
import serverClient as serv
import socket
from collections import namedtuple

dataQueue = SimpleQueue()

def sendData(opcode, data):
    toSend = []
    toSend.append(opcode)
    toSend.extend(data)
    dataQueue.put(toSend)
    print("Put data: 0x{}".format(bytearray(toSend).hex()))


Switch = namedtuple('Switch', 'opcode is_no')

PRESS_PROP = Switch(0x32, 0)
OX_FILL = Switch(0x33, 0)
OX_DUMP = Switch(0x3e, 0)
PRESS_VENT = Switch(0x34, 1)
OX_VENT = Switch(0x36, 1)
FUEL_VENT = Switch(0x38, 1)
FUEL_CC = Switch(0x3a, 0)
OX_CC = Switch(0x3c, 0)

PRESS_FILL = Switch(0x40, 0)
QUICK_DISC = Switch(0x43, 0)
IGNITE = Switch(0x41, 0)
IGNITE_SAFETY = Switch(0x41, 0)

IGNITE_INDEX = 6
SAFETY_INDEX = 13

MAP = {
    4: PRESS_PROP,
    2: OX_FILL,
    17: OX_DUMP,
    27: PRESS_VENT,
    11: OX_VENT,
    10: FUEL_VENT,
    22: FUEL_CC,
    9: OX_CC,
    3: PRESS_FILL,
    5: QUICK_DISC,
    IGNITE_INDEX: IGNITE,
    SAFETY_INDEX: IGNITE_SAFETY,
}

relay_pins = [4,3,17,27,11,10,22,9,2,5,IGNITE_INDEX, SAFETY_INDEX]

def getSwitch(channel):
    return not GPIO.input(channel)

moistEnabled = False

def my_callback(channel):
    if not moistEnabled:
        print("not enabled :(")
        return

    time.sleep(0.01)
    switch_in = getSwitch(channel) 
    switch = MAP[channel]

    print("channel: ", channel)
    print("input: ", switch_in)

    if(switch == IGNITE or switch == IGNITE_SAFETY):
        output = (1 if (getSwitch(IGNITE_INDEX) and getSwitch(SAFETY_INDEX)) else 0)
        sendData(switch.opcode, [output])
    else:
        output = (1 if (switch.is_no != switch_in) else 0)
        sendData(switch.opcode, [output])


GPIO.setmode(GPIO.BCM)

for pin in relay_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=100)

ENABLE_PIN = 19
GPIO.setup(ENABLE_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

LED_PIN = 26
GPIO.setup(LED_PIN, GPIO.OUT)

#main begins here
clientProcess = Process(target=serv.sendFromQueue, args=(dataQueue,))
usingServer = True

try:
    serv.connect('arescdh', 9999)
    clientProcess.start()
except socket.error as e:
    print("Error starting connection to server, code ", e)
    usingServer = False

led = 0

while True:
    value = getSwitch(ENABLE_PIN)
    if moistEnabled != value:
        print("Enabling MOIST" if value else "Disabling MOIST")
        moistEnabled = value
        led = 0
    
    if(led == 0 and moistEnabled):
        GPIO.output(LED_PIN, 1)
    else:
        GPIO.output(LED_PIN, 0)

    led = led + 1
    if(led > (1 if usingServer else 2)):
        led = 0

    time.sleep(0.1 if getSwitch(SAFETY_INDEX) else 1)
