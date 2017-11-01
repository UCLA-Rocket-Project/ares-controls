import serialHandler as ser
import opcodes as op
import mcuconsts as consts

def getRelaysObject(command):
	if command == op.PRESS_PROP_SET:
		return consts.Relays.PRESS_PROP
	if command == op.OX_FILL_SET:
		return consts.Relays.OX_FILL
	if command == op.PRESS_VENT_SET or command == op.PRESS_VENT_DELAYED_SET:
		return consts.Relays.PRESS_VENT
	if command == op.OX_VENT_SET or command == op.OX_VENT_DELAYED_SET:
		return consts.Relays.OX_VENT
	if command == op.FUEL_VENT_SET or command == op.FUEL_VENT_DELAYED_SET:
		return consts.Relays.FUEL_VENT
	if command == op.FUEL_CC_SET or command == op.FUEL_CC_DELAYED_SET:
		return consts.Relays.FUEL_CC
	if command == op.OX_CC_SET or command == op.OX_CC_DELAYED_SET:
		return consts.Relays.OX_CC
	if command == op.PRESS_FILL_SET:
		return consts.Relays.PRESS_FILL
	if command == op.IGNITION_SET or command == op.IGNITE_FOR_TIME:
		return consts.Relays.IGNITION
	if command == op.QD_RELEASE or command == op.QD_CHECK_READY:
		return consts.Relays.QD
	return consts.Relays.ERROR
	#worry about others later

def isDelayed(command):
	if command == op.PRESS_VENT_DELAYED_SET or command == op.OX_VENT_DELAYED_SET or command == op.FUEL_VENT_DELAYED_SET or command == op.FUEL_CC_DELAYED_SET or command == op.OX_CC_DELAYED_SET:
		return True
	return False

def isSpecial(command):
	#print("checked special")
	if command == op.VALVES_SET_ALL or command == op.VALVES_GET_ALL or command == op.IGNITE_FOR_TIME or command == op.QD_RELEASE or command == op.QD_CHECK_READY:
		return True
	return False
	
def handleRelay(turnOnRelay):
	if turnOnRelay == True:
		return consts.Opcode.RELAY_ON
	return consts.Opcode.RELAY_OFF

def delayHandler(byteArray, commandObject):
	if consts.IS_NORMALLY_CLOSED[commandObject]:
			onOrOffByte = byteArray[1]
	else:
		if byteArray[1] == 0x00:
			onOrOffByte = 0x01
		else:
			onOrOffByte = 0x00
	return [commandObject.value.addr, consts.Opcode.RELAY_SET_DELAYED.value, onOrOffByte, byteArray[2], byteArray[3]]
	
def setValves(byteArray):
	#print("Checked setValves")
	array = [consts.Addr.FCM, consts.Opcode.RELAY_SET_ALL.value]
	for i in range(1, len(byteArray)):
		if i == 1: commandObject = getRelaysObject(op.PRESS_PROP_SET)
		if i == 2: commandObject = getRelaysObject(op.OX_FILL_SET)
		if i == 3: commandObject = getRelaysObject(op.PRESS_VENT_SET)
		if i == 4: commandObject = getRelaysObject(op.OX_VENT_SET)
		if i == 5: commandObject = getRelaysObject(op.FUEL_VENT_SET)
		if i == 6: commandObject = getRelaysObject(op.FUEL_CC_SET)
		if i == 7: commandObject = getRelaysObject(op.OX_CC_SET)
		if consts.IS_NORMALLY_CLOSED[commandObject]:
				onOrOffByte = byteArray[i]
		else:
			if byteArray[i] == 0x00: #off
				onOrOffByte = 0x01 #on
			else:
				onOrOffByte = 0x00
		array.append(onOrOffByte)
	return array
	
def getValves(byteArray):
	return []

def handleCommand(byteArray):
	command = byteArray[0]
	commandObject = getRelaysObject(command)
	if not isSpecial(command) and commandObject == consts.Relays.ERROR:
		return [consts.Addr.CDH, 0xe1]
	if isSpecial(command):
		if command == op.IGNITE_FOR_TIME:
			return [commandObject.value.addr, 0x01, byteArray[1], byteArray[2]]
		if command == op.VALVES_SET_ALL:
			return setValves(byteArray)
		if command == op.VALVES_GET_ALL:
			return getValves(byteArray)
	turnOnRelay = 0x01
	dirByte = 0x00
	if isDelayed(command):
		return delayHandler(byteArray, commandObject)	
	if not consts.IS_NORMALLY_CLOSED[commandObject]:
		turnOnRelay = 0x00
	if (not (isDelayed(command) or isSpecial(command))):
		return [commandObject.value.addr, handleRelay(turnOnRelay == byteArray[1]).value, commandObject.value.relay]
	#there are some more special statements that may be added here later
	return [consts.Addr.CDH, 0xe1] #subject to change

array = [0x39, 0x01, 0, 1]
print(handleCommand(array))