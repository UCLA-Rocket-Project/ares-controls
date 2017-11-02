import serialHandler as ser
import opcodes as op
import mcuconsts as consts

ERROR = [consts.Addr.CDH, 0xe1]

OPEN_VALVE = 0x01
CLOSE_VALVE = 0x00

RELAY_ON = 0x01
RELAY_OFF = 0x00

def getRelaysObject(command):
	if command in consts.OPCODE_MATCHER:
		return consts.OPCODE_MATCHER[command]
	return consts.Relays.ERROR

def isDelayed(command):
	return command == op.PRESS_VENT_DELAYED_SET or command == op.OX_VENT_DELAYED_SET or command == op.FUEL_VENT_DELAYED_SET or command == op.FUEL_CC_DELAYED_SET or command == op.OX_CC_DELAYED_SET

def isSpecial(command):
	return command == op.VALVES_SET_ALL or command == op.VALVES_GET_ALL or command == op.IGNITE_FOR_TIME or command == op.QD_RELEASE or command == op.QD_CHECK_READY
	
def setOnOrOff(turnOnRelay):
	if turnOnRelay:
		return consts.Opcode.RELAY_ON.value
	return consts.Opcode.RELAY_OFF.value

def delayHandler(byteArray, commandObject):
	if not len(byteArray) == 4:
		return ERROR
	valveStatus = byteArray[1]
	if consts.IS_NORMALLY_CLOSED[commandObject]:
			relayStatus = valveStatus
	else:
		if valveStatus == CLOSE_VALVE:
			relayStatus = RELAY_ON
		else:
			relayStatus = RELAY_OFF
	return [commandObject.value.addr, consts.Opcode.RELAY_SET_DELAYED.value, commandObject.value.relay, relayStatus, byteArray[2], byteArray[3]]
	
def setValves(byteArray):
	#print("Checked setValves")
	array = [consts.Addr.FCM, consts.Opcode.RELAY_SET_ALL.value]
	if not len(byteArray) == 8:
		return ERROR
	objects = [
		getRelaysObject(op.PRESS_PROP_SET), 
		getRelaysObject(op.OX_FILL_SET),
		getRelaysObject(op.PRESS_VENT_SET),
		getRelaysObject(op.OX_VENT_SET),
		getRelaysObject(op.FUEL_VENT_SET),
		getRelaysObject(op.FUEL_CC_SET),
		getRelaysObject(op.OX_CC_SET),
	]
	for i in range(1, len(byteArray)):
		valveStatus = byteArray[i]
		commandObject = objects[i - 1]
		if consts.IS_NORMALLY_CLOSED[commandObject]:
				relayStatus = valveStatus
		else:
			if valveStatus == CLOSE_VALVE:
				relayStatus = RELAY_ON
			else:
				relayStatus = RELAY_OFF
		array.append(relayStatus)
	return array

def handleCommand(byteArray):
	command = byteArray[0]
	if isSpecial(command):
		if command == op.VALVES_SET_ALL:
			return setValves(byteArray)
		if command == op.VALVES_GET_ALL:
			return [consts.Addr.FCM, consts.Opcode.GET_ALL_RELAY_STATES]
	valveStatus = byteArray[1]
	commandObject = getRelaysObject(command)
	if commandObject == consts.Relays.ERROR:
		return ERROR
	turnOnRelay = 0x01
	if isDelayed(command):
		return delayHandler(byteArray, commandObject)	
	if not consts.IS_NORMALLY_CLOSED[commandObject]:
		turnOnRelay = 0x00
	if (not (isDelayed(command) or isSpecial(command))):
		return [commandObject.value.addr, setOnOrOff(turnOnRelay == valveStatus), commandObject.value.relay]
	return ERROR
	
array = [0x34, 0x00]
print(handleCommand(array))