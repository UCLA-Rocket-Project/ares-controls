import libares.opcodes as op
import libares.mcuconsts as consts

ERROR = [consts.Addr.CDH, 0xe1]

def getRelayFromOpcode(command):
	if command in consts.OPCODE_MATCHER:
		return consts.OPCODE_MATCHER[command]
	return None

def getRelayOpcode(turnOn):
    if turnOn:
        return consts.Opcode.RELAY_ON.value
    else:
        return consts.Opcode.RELAY_OFF.value

def handleCommand(byteArray):
    cmd_opcode = byteArray[0];

    if cmd_opcode in op.OPCODE_TYPES:
        cmd_optype = op.OPCODE_TYPES[cmd_opcode]
    else:
        return ERROR

    if(cmd_optype == op.OpType.SETVALVE):
        return handleSetValveCommand(cmd_opcode, byteArray)

    elif(cmd_optype == op.OpType.SETBULK):
        return handleSetBulkCommand(cmd_opcode, byteArray)

    return ERROR

def handleSetValveCommand(cmd_opcode, byteArray):
    cmd_direction = byteArray[1] # 0x01: open, 0x00: close

    cmd_relay = getRelayFromOpcode(cmd_opcode)

    if not cmd_relay:
        return ERROR

    # close (false) & NC (true) -> false (OFF)
    # open (true) & NC (true) -> true (ON)
    shouldTurnRelayOn = (cmd_direction == consts.IS_NORMALLY_CLOSED[cmd_relay])
    relayCommand = getRelayOpcode(shouldTurnRelayOn)

    return [cmd_relay.value.addr, relayCommand, cmd_relay.value.relay]

def handleSetBulkCommand(cmd_opcode, byteArray):
    if cmd_opcode == op.VALVES_SET_ALL:
        return setValves(byteArray)
    if cmd_opcode == op.VALVES_GET_ALL:
        return [consts.Addr.FCM, consts.Opcode.RELAY_GET_ALL_STATES.value]
    return ERROR

def setValves(byteArray):
    array = [consts.Addr.FCM, consts.Opcode.RELAY_SET_ALL.value]
    if not len(byteArray) == 9:
        return ERROR

    for i in range(1, len(byteArray)):
        cmd_direction = byteArray[i]
        cmd_relay = consts.FCMRelays[i - 1]

        shouldTurnRelayOn = (cmd_direction == consts.IS_NORMALLY_CLOSED[cmd_relay])
        relayCommand = getRelayOpcode(shouldTurnRelayOn)
        array.append(relayCommand)

    return array

def handleDelayCommand(cmd_opcode, byteArray):
    cmd_relay = getRelayFromOpcode(cmd_opcode)

    if not len(byteArray) == 4:
        return ERROR

    cmd_direction = byteArray[1] # 0x01: open, 0x00: close
    shouldTurnRelayOn = (cmd_direction == consts.IS_NORMALLY_CLOSED[cmd_relay]) # 1 = on, 0 = off

    return [commandObject.value.addr, consts.Opcode.RELAY_SET_DELAYED.value, cmd_relay.value.relay, shouldTurnRelayOn, byteArray[2], byteArray[3]]
