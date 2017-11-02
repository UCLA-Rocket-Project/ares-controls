import opcodes as op
import mcuconsts as consts

ERROR = [consts.Addr.CDH, 0xe1]

OPEN_VALVE = 0x01
CLOSE_VALVE = 0x00

RELAY_ON = 0x01
RELAY_OFF = 0x00

FCM_RELAY_OBJECTS = [
consts.Relays.PRESS_PROP,
consts.Relays.OX_FILL,
consts.Relays.PRESS_VENT,
consts.Relays.OX_VENT,
consts.Relays.FUEL_VENT,
consts.Relays.FUEL_CC,
consts.Relays.OX_CC
]

def getRelayFromOpcode(command):
	if command in consts.OPCODE_MATCHER:
		return consts.OPCODE_MATCHER[command]
	return consts.Relays.ERROR

def getRelayOpcode(turnOn):
	if turnOn:
		return consts.Opcode.RELAY_ON.value
	return consts.Opcode.RELAY_OFF.value

def handleSetDelayed(cmd_opcode, byteArray):
    commandObject = getRelayFromOpcode(cmd_opcode)
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
	array = [consts.Addr.FCM, consts.Opcode.RELAY_SET_ALL.value, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	relays = []
	if not len(byteArray) == 8:
		return ERROR
	for i in range(1, len(byteArray)):
		valveStatus = byteArray[i]
		commandObject = FCM_RELAY_OBJECTS[i - 1]
		relays.append(commandObject.value.relay)
		if consts.IS_NORMALLY_CLOSED[commandObject]:
				relayStatus = valveStatus
		else:
			if valveStatus == CLOSE_VALVE:
				relayStatus = RELAY_ON
			else:
				relayStatus = RELAY_OFF
		array[relays[i - 1] + 2] = relayStatus
	return array

def handleSetBulkCommand(cmd_opcode, byteArray):
    if cmd_opcode == op.VALVES_SET_ALL:
        return setValves(byteArray)
    if cmd_opcode == op.VALVES_GET_ALL:
        return [consts.Addr.FCM, consts.Opcode.RELAY_GET_ALL_STATES.value]
    return ERROR

def handleQD(cmd_opcode):
    cmd_relay = consts.Relays.QD
    return [cmd_relay.value.addr, getRelayOpcode(1), cmd_relay.value.relay]

def handleSetValve(cmd_opcode, byteArray):
    cmd_direction = byteArray[1] # 0x01: open, 0x00: close

    cmd_relay = getRelayFromOpcode(cmd_opcode)

    if cmd_relay == consts.Relays.ERROR:
        return ERROR

    # close (false) & NC (true) -> false (OFF)
    # open (true) & NC (true) -> true (ON)
    shouldTurnRelayOn = (cmd_direction == consts.IS_NORMALLY_CLOSED[cmd_relay])
    relayCommand = getRelayOpcode(shouldTurnRelayOn)

    return [cmd_relay.value.addr, relayCommand, cmd_relay.value.relay]


# Returns an MCU command corresponding to a given CDH command sequence
def handleCommand(byteArray):
	cmd_opcode = byteArray[0]
	return getMCUCommand(cmd_opcode, byteArray)

def getMCUCommand(cmd_opcode, byteArray):
    # TODO: check correct length
	cmd_optype = op.OPCODE_TYPES[cmd_opcode]

	if(cmd_optype == op.OpType.SETVALVE):
		return handleSetValve(cmd_opcode, byteArray)

	elif(cmd_optype == op.OpType.SETBULK):
		return handleSetBulkCommand(cmd_opcode, byteArray)

	elif(cmd_optype == op.OpType.QD):
		return handleQD(cmd_opcode, byteArray)

	elif(cmd_optype == op.OpType.SETDELAYED):
		return handleSetDelayed(cmd_opcode, byteArray)

	return ERROR
