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
    print("")


Switch = namedtuple('Switch', 'opcode is_no')

PRESS_PROP = Switch(0x32, 0)
OX_FILL = Switch(0x33, 0)
OX_DUMP = Switch(0x3e, 0)
PRESS_VENT = Switch(0x34, 0)
OX_VENT = Switch(0x36, 0)
FUEL_VENT = Switch(0x38, 0)
FUEL_CC = Switch(0x3a, 0)
OX_CC = Switch(0x3c, 0)

PRESS_FILL = Switch(0x40, 0)
QUICK_DISC = Switch(0x43, 0)
IGNITE = Switch(0x41, 0)

IGNITE_INDEX = 9

LEDMAP = {
    PRESS_PROP: 21,
    OX_FILL: 20,
    OX_DUMP: 12,
    PRESS_VENT: 25,
    OX_VENT: 8,
    FUEL_VENT: 7,
    FUEL_CC: 23,
    OX_CC: 18,
    PRESS_FILL: 16,
    QUICK_DISC: 26,
    IGNITE: 24
}

MAP = {
    11: PRESS_PROP,
    6: OX_FILL,
    13: OX_DUMP,
    2: PRESS_VENT,
    3: OX_VENT,
    10: FUEL_VENT,
    4: FUEL_CC,
    17: OX_CC,
    5: PRESS_FILL,
    22: QUICK_DISC,
    IGNITE_INDEX: IGNITE
}

ENABLE_PIN = 19

def getSwitch(channel):
    return not GPIO.input(channel)


def my_callback(channel):
    if not moistEnabled:
        print("not enabled :(")
        return

    time.sleep(0.01)
    switch_in = getSwitch(channel) 
    switch = MAP[channel]

    print("channel:", channel, "input:", switch_in)

    output = (1 if (switch.is_no != switch_in) else 0)
    GPIO.output(LEDMAP[switch], output)
    sendData(switch.opcode, [output])


GPIO.setmode(GPIO.BCM)

for pin in MAP:
    print('setup pin {}'.format(pin))
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=25)

for valve, ledpin in LEDMAP.items():
    GPIO.setup(ledpin, GPIO.OUT)
    GPIO.output(ledpin, 0)

for channel, switch in MAP.items():
    switch_in = getSwitch(channel)
    GPIO.output(LEDMAP[switch], switch_in)
    sendData(switch.opcode, [1 if (switch.is_no != switch_in) else 0])

GPIO.setup(ENABLE_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#main begins here
clientProcess = Process(target=serv.sendFromQueue, args=(dataQueue,))
usingServer = True
moistEnabled = False

try:
    serv.connect('arescdhbeta', 9999)
    clientProcess.start()
    print("connected to server!")
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
    
    turnOnLED = ((led < 10) if not usingServer else (led < 3 or (led > 5 and led < 8)))
    if not moistEnabled:
        turnOnLED = (led < 1)

    if turnOnLED:
        GPIO.output(LEDMAP[IGNITE], 1)
    else:
        GPIO.output(LEDMAP[IGNITE], 0)

    led = led + 1
    if(led > 10):
        led = 0

    time.sleep(0.02 if getSwitch(IGNITE_INDEX) else 0.2)
