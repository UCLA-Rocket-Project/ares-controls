import RPi.GPIO as GPIO
import time
from multiprocessing import Process, SimpleQueue
import serverClient as serv
import socket
from libares.moistconsts import *
from libares.constants import *

dataQueue = SimpleQueue()

def sendData(opcode, data):
    toSend = []
    toSend.append(opcode)
    toSend.extend(data)
    dataQueue.put(toSend)
    print("event-raw> Send data: 0x{}".format(bytearray(toSend).hex()))

def getSwitch(channel):
    return not GPIO.input(channel)

def switch_callback(channel):
    if not moistEnabled:
        print("event> not enabled :(")
        return

    time.sleep(0.01)
    switch_in = getSwitch(channel)
    switch = MAP[channel]

    print("\nevent> channel:", channel, "input:", switch_in)
    print("event-english> ", opcodes[switch.opcode][op_POS_STR],
        " is being ", ("OPENED" if switch_in else "CLOSED"))

    output = (1 if (switch.is_no != switch_in) else 0)
    GPIO.output(LEDMAP[switch], output)
    sendData(switch.opcode, [output])

GPIO.setmode(GPIO.BCM)

def resetLEDS(enable=True):
    for channel, switch in MAP.items():
        switch_in = getSwitch(channel)
        if enable:
            GPIO.output(LEDMAP[switch], switch_in != switch.is_no)
        else:
            GPIO.output(LEDMAP[switch], 0)

for pin in MAP:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=switch_callback, bouncetime=25)

for channel, switch in MAP.items():
    switch_in = getSwitch(channel)
    GPIO.setup(LEDMAP[switch], GPIO.OUT)
    sendData(switch.opcode, [1 if (switch.is_no != switch_in) else 0])

GPIO.setup(ENABLE_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#main begins here
clientProcess = Process(target=serv.sendFromQueue, args=(dataQueue,))
usingServer = True
moistEnabled = False

try:
    serv.connect('arescdhbeta', 9999)
    clientProcess.start()
    print("TCP> connected to server!")
except socket.error as e:
    print("TCP> Error starting connection to server, code ", e)
    usingServer = False

led = 0
resetLEDS(enable=moistEnabled)

while True:
    value = getSwitch(ENABLE_PIN)
    if moistEnabled != value:
        print("\nENABLE> ", "Enabling MOIST" if value else "Disabling MOIST")
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
