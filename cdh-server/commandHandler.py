import libares.constants as consts

ERROR = [consts.Addr.CDH, 0xe1]

def getRelayFromOpcode(command):
	if command in consts.opcodes:
		return consts.opcodes[command][consts.op_POS_RELAY]
	return None

def getRelayOpcode(turnOn):
    if turnOn:
        return consts.MCUOpcode.RELAY_ON.value
    else:
        return consts.MCUOpcode.RELAY_OFF.value

def handleCommand(byteArray):
    cmd_opcode = byteArray[0];

    if cmd_opcode in consts.opcodes:
        cmd_optype = consts.opcodes[cmd_opcode][consts.op_POS_TYPE]
    else:
        return ERROR

    if(cmd_optype == consts.OpType.SETVALVE):
        return handleSetValveCommand(cmd_opcode, byteArray)

    return ERROR

def handleSetValveCommand(cmd_opcode, byteArray):
    cmd_direction = byteArray[1] # 0x01: open, 0x00: close

    cmd_relay = getRelayFromOpcode(cmd_opcode)

    if not cmd_relay:
        return ERROR

    # close (false) & NC (true) -> false (OFF)
    # open (true) & NC (true) -> true (ON)
    shouldTurnRelayOn = (cmd_direction == cmd_relay.value.nc)
    relayCommand = getRelayOpcode(shouldTurnRelayOn)

    return [cmd_relay.value.addr, relayCommand, cmd_relay.value.relay]

def handleSetBulkCommand(cmd_opcode, byteArray):
    if cmd_opcode == consts.OP_FCM_VALVES_SET_ALL:
        return setValves(byteArray)
    if cmd_opcode == consts.OP_FCM_VALVES_GET_ALL:
        return [consts.Addr.FCM, consts.MCUOpcode.RELAY_GET_ALL_STATES.value]
    return ERROR
#
# def setValves(byteArray):
#     array = [consts.Addr.FCM, consts.MCUOpcode.RELAY_SET_ALL.value]
#     if not len(byteArray) == 9:
#         return ERROR
#
#     for i in range(1, len(byteArray)):
#         cmd_direction = byteArray[i]
#         cmd_relay = mcuconsts.FCMRelays[i - 1]
#
#         shouldTurnRelayOn = (cmd_direction == cmd_relay.value.nc)
#         relayCommand = getRelayOpcode(shouldTurnRelayOn)
#         array.append(relayCommand)
#
#     return array
#
# def handleDelayCommand(cmd_opcode, byteArray):
#     cmd_relay = getRelayFromOpcode(cmd_opcode)
#
#     if not len(byteArray) == 4:
#         return ERROR
#
#     cmd_direction = byteArray[1] # 0x01: open, 0x00: close
#     shouldTurnRelayOn = (cmd_direction == cmd_relay.nc) # 1 = on, 0 = off
#
#     return [commandObject.value.addr, consts.MCUOpcode.RELAY_SET_DELAYED.value, cmd_relay.value.relay, shouldTurnRelayOn, byteArray[2], byteArray[3]]
