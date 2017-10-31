import serial as ps
import time
import socket
import sys

"""address = 0x01
op_code = 0xc1
data = 0x03
stop_code = 0xff

b = [address,op_code,data,stop_code] #should only be opcode data and checksum
out = []"""

#FCM
VALVES_SET_ALL = 0x30 
VALVES_GET_ALL = 0x31 
PRESS_PROP_SET = 0x32 #Relay0
OX_FILL_SET = 0x33 #Relay1
PRESS_VENT_SET = 0x34 #Relay2
PRESS_VENT_DELAYED_SET = 0x35 #Relay2
OX_VENT_SET = 0x36 #Relay3
OX_VENT_DELAYED_SET = 0x37 #Relay3
FUEL_VENT_SET = 0x38 #Relay4
FUEL_VENT_DELAYED_SET = 0x39 #Relay4
FUEL_CC_SET = 0x3a #Relay5
FUEL_CC_DELAYED_SET =0x3b #Relay5
OX_CC_SET = 0x3c #Relay6
OX_CC_DELAYED_SET = 0x3d #Relay6

#GCM
PRESS_FILL_SET = 0x40 #Relay0
IGNITION_SET = 0x41 #Relay1
IGNITE_FOR_TIME = 0x42 #Relay1
QD_RELEASE = 0x43 #Relay2
QD_CHECK_READY = 0x44 #Relay2

VALVE_CLOSE = 0x00
VALVE_OPEN = 0x01

RELAY_OFF = 0xC0
RELAY_ON = 0xC1
RELAY_SET_DELAYED = 0xCF

RELAY0 = 0x00
RELAY1 = 0x01
RELAY2 = 0x02
RELAY3 = 0x03
RELAY4 = 0x04
RELAY5 = 0x05
RELAY6 = 0x06
RELAY7 = 0x07

GCMADDRESS = 0xA1 #subject to change
FCMADDRESS = 0xA2 #subject to change

STOPCODE = 0xff

bytesToSend = []

fcmNormallyClosed = [PRESS_PROP_SET, OX_FILL_SET, FUEL_CC_SET, FUEL_CC_DELAYED_SET, OX_CC_SET, OX_CC_DELAYED_SET]
fcmNormallyOpen = [PRESS_VENT_SET, PRESS_VENT_DELAYED_SET, OX_VENT_SET, OX_VENT_DELAYED_SET, FUEL_VENT_SET, FUEL_VENT_DELAYED_SET]
fcmCommands = fcmNormallyClosed.append(fcmNormallyOpen)
gcmCommands = [PRESS_FILL_SET, IGNITION_SET, IGNITE_FOR_TIME, QD_RELEASE, QD_CHECK_READY]
commands = fcmCommands.append(gcmCommands)

def isCorrectData(byteArray):
	return True; #will change soon

def opcodeMatcher(command, opcode):
	if command == PRESS_PROP_SET or command == OX_FILL_SET or command == FUEL_FUEL_SET or command == FUEL_CC_DELAYED_SET or command == OX_CC_SET or command == OX_CC_DELAYED_SET or command == PRESS_FILL_SET:
		if opcode == VALVE_CLOSE: return RELAY_OFF
		if opcode == VALVE_OPEN: return RELAY_ON
	else:
		if opcode == VALVE_CLOSE: return RELAY_ON
		if opcode == VALVE_OPEN: return RELAY_OFF

def setRelay(command, relay):
	mapper = []
	mapper.append(command)
	mapper.append(relay)
	return mapper
	
setRelay(PRESS_PROP_SET, RELAY0)	#map rest of relays

	
def getRelay(command):
	return mapper[1]

def handleArray(array, address):
	command = array[0]
	data = array[1]
	if len(array) == 3: #regular
		tempArray = [address, opcodeMatcher(command, data), getRelay(command), STOPCODE]
	else if len(array) == 5: #delayed
		data1 = array[1]
		data2 = array[2]
		data3 = array[3]
		tempArray = [address, RELAY_SET_DELAYED, getRelay(command), data1, data2, data3, STOPCODE]
	else if len(array) == 9: #set valves
		tempArray = [address, opcodeMatcher(PRESS_PROP_SET, array[1]), opcodeMatcher(OX_FILL_SET, array[2]), opcodeMatcher(PRESS_VENT_SET, array[3]), opcodeMatcher(OX_VENT_SET, array[4]), opcodeMatcher(FUEL_VENT_SET, array[5]), opcodeMatcher(FUEL_CC_SET, array[6]), opcodeMatcher(OX_CC_SET, array[7]), 0x00, STOPCODE]
	return tempArray
	
def handleData(byteArray):
	command = byteArray[0]
	if command in fcmCommands:
		return handleArray(byteArray, FCMADDRESS)
	else if command in gcmCommands:
		return handleArray(byteArray, GCMADDRESS)
					
	"""else if byteArray[0] == PRESS_PROP_SET:
		if byteArray[1] == VALVE_CLOSE:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY0, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY0, STOPCODE]
	else if byteArray[0] == OX_FILL_SET:
		if byteArray[1] == VALVE_CLOSE:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY1, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY1, STOPCODE]
	else if byteArray[0] == PRESS_VENT_SET:
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY2, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY2, STOPCODE]
	else if byteArray[0] == PRESS_VENT_DELAYED_SET
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY2, RELAY_OFF, byteArray[2], byteArray[3], STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY2, RELAY_ON, byteArray[2], byteArray[3], STOPCODE]
	else if byteArray[0] == OX_VENT_SET
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY3, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY3, STOPCODE]
	else if byteArray[0] == OX_VENT_DELAYED_SET
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY3, RELAY_OFF, byteArray[2], byteArray[3], STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY3, RELAY_ON, byteArray[2], byteArray[3], STOPCODE]
	else if byteArray[0] == FUEL_VENT_SET:
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY4, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY4, STOPCODE]
	else if byteArray[0] == FUEL_VENT_DELAYED_SET:
		if byteArray[1] == VALVE_OPEN:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY4, RELAY_OFF, byteArray[2], byteArray[3], STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY4, RELAY_ON, byteArray[2], byteArray[3], STOPCODE]
	else if byteArray[0] == FUEL_CC_SET:
		if byteArray[1] == VALVE_CLOSED:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY5, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY5, STOPCODE]
	else if byteArray[0] == FUEL_CC_DELAYED_SET:
		if byteArray[1] == VALVE_CLOSED:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY5, RELAY_OFF, byteArray[2], byteArray[3], STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY5, RELAY_ON, byteArray[2], byteArray[3], STOPCODE]
	else if byteArray[0] == OC_CC_SET:
		if byteArray[1] == VALVE_CLOSED:
			bytesToSend = [FCMADDRESS, RELAY_OFF, RELAY6, STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_ON, RELAY6, STOPCODE]
	else if byteArray[0] == OX_CC_DELAYED_SET:
		if byteArray[1] == VALVE_CLOSED:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY6, RELAY_OFF, byteArray[2], byteArray[3], STOPCODE]
		else:
			bytesToSend = [FCMADDRESS, RELAY_SET_DELAYED, RELAY6, RELAY_ON, byteArray[2], byteArray[3], STOPCODE]
			
	else if byteArray[0] == PRESS_FILL_SET:
		if byteArray[1] == VALVE_CLOSED:
			bytesToSend = [GCMADDRESS, RELAY_OFF, RELAY0, STOPCODE]
		else:
			bytesToSend = [GCMADDRESS, RELAY_ON, RELAY0, STOPCODE]
	else if byteArray[0] == IGNITION_SET:
		if byteArray[1] == """
		
def serialSend(data):
	con.write(b)
	for i in range(0,4):
		out.append(con.read())
	print(out)
	print(out)

con = ps.Serial('/dev/cu.usbmodem1421')
con.flush()
time.sleep(2)
con.reset_input_buffer()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
	
		while True:
			data = connection.recv(30)
			print >>sys.stderr, 'received' + data
			if data: #and isCorrectData(data):
				data = handleData(data)
				print >>sys.stderr, 'sending data back to connection and to FCM'
				connection.sendall(data)
				serialSend(data)
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
			
	finally:
		connection.close()

