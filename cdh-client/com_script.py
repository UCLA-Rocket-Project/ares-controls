import serial as ps
import time
con = ps.Serial('/dev/cu.usbmodem1411')
con.flush()
time.sleep(2)
con.reset_input_buffer()

address = 0xA1
op_code = 0xc1
data = 0x03
stop_code = 0xff

b = [address,op_code,data,stop_code]
out = []

con.write(b)
for i in range(0,4):
    out.append(con.read())

print(out)
