#serialHandler.py
import serial as pyserial
import time

class SerialHandler:
    def __init__(self, portName, timeout=10):
        self.con = pyserial.Serial(portName, timeout=timeout)
        self.con.flush()
        time.sleep(2)
        self.con.reset_input_buffer()

    def sendDataToMCU(self, dest, opcode, data):
        print("sending data: {}".format(data))

        toSend = []
        bytes_sent = 0

        adr_op = (dest & 0xc0) | (opcode & 0x3f)
        cont_code = (dest & 0xc0) | 0x3e
        end_code = (dest & 0xc0) | 0x3f

        toSend.append(adr_op)
        toSend.append(data[0])

        if len(data) > 1:
            for i,byte in enumerate(data):
                if i == 0:
                    continue
                if i == len(data):
                    break
                toSend.append(cont_code)
                toSend.append(byte)
                bytes_sent += 2

        toSend.append(end_code)

        data.insert(0, adr_op)
        crc = compute_crc(data)

        toSend.append(crc)
        print("calculated on pi- sent crc: {}".format(crc))
        bytes_sent += 4

        print("sent {} bytes".format(bytes_sent))
        print("sending bytes: {}".format(toSend))

        # send data
        self.con.write(toSend)
        return_message = self.con.read(1024)


        print("return message: {}".format(return_message))
        if len(return_message) != 4:
              print("the return message has been corrupted")
        else:
            crc_return_input = [return_message[0], return_message[1]]
            return_crc = compute_crc(crc_return_input)
            print("calculated on pi- return crc: {}".format(return_crc))
            
        return return_message


def compute_crc(input1):
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

fcmHandler = SerialHandler("/dev/ttyACM0", timeout=0.5)
gcmHandler = SerialHandler("/dev/ttyACM1", timeout=0.5)
