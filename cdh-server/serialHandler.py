#serialHandler.py
import serial as pyserial
import time

class SerialHandler:
    def __init__(self, delay=0.5):
        self.delay = delay
        self.con = []

    def connect(self, serialPort, timeout=0, wait=2):
        try:
            newCon = pyserial.Serial(serialPort, timeout=timeout)
            newCon.flush()
            time.sleep(wait) # wait while arduinos reboot
            newCon.reset_input_buffer()
            self.con.append(newCon)
        except pyserial.SerialException:
            return false
        return true


    def sendDataToMCUs(self, dest, opcode, data):
        print("sending data: {}".format(data))

        adr_op = (dest & 0xc0) | (opcode & 0x3f)
        cont_code = (dest & 0xc0) | 0x3e
        end_code = (dest & 0xc0) | 0x3f
        crc = self.compute_crc([adr_op] + data)

        toSend = []
        toSend.append(adr_op)
        toSend.append(data[0])

        if len(data) > 1:
            for i,byte in enumerate(data):
                if i == 0: #sent with adr_op
                    continue
                if i == len(data):
                    break
                toSend.append(cont_code)
                toSend.append(byte)

        toSend.append(end_code)
        toSend.append(crc)

        print("calculated on pi- sent crc: {}".format(crc))
        print("sent {} bytes".format(len(toSend)))
        print("sending bytes: {}".format(toSend))

        # send data
        for con in self.con:
            con.write(toSend)

        time.sleep(self.delay)

        messages = []
        for con in self.con :
            messages.append(self.con.read(1024))

        print("received messages: {}".format(messages))
        return messages

    def getConnectedPorts(self):
        ports = []
        for con in self.con:
            ports.append(con.port)
        return ports

    def compute_crc(self, input1):
        crc8 = 0x00
        for pos in range(len(input1)):
            crc8 ^= input1[pos]
            for i in range(8,0,-1):
                if ((crc8 & 0x01) !=0):
                    crc8 >>= 1
                    crc8 ^= 0x8c
                else:
                    crc8 >>= 1
        return crc8

def getHandler():
    if not mcuHandler:
        mcuHandler = SerialHandler()
    return mcuHandler
