from enum import Enum
from collections import namedtuple

class MCUOpcode(Enum):
    RELAY_OFF = 0x10
    RELAY_ON = 0x11
    RELAY_GET = 0x12
    RELAY_GET_ALL_STATES = 0x13
    RELAY_ALL_OFF = 0x14
    RELAY_ALL_ON = 0x15
    RELAY_SET_ALL = 0x16

class Addr:
    GCM = 0x80 #subject to change
    FCM = 0x40  #subject to change
    CDH = 0xC0 #subject to change

Relay = namedtuple('Relay', 'addr relay nc')

class Relays(Enum):
    PRESS_VENT = Relay(Addr.FCM, 0, False)
    OX_VENT = Relay(Addr.FCM, 1, False)
    FUEL_VENT = Relay(Addr.FCM, 2, False)
    FUEL_CC = Relay(Addr.FCM, 3, True)
    OX_CC = Relay(Addr.FCM, 4, True)
    OX_DUMP = Relay(Addr.FCM, 5, True)
    KBTL_FILL = Relay(Addr.GCM, 0, True)
    TBTL_FILL = Relay(Addr.GCM, 1, True)
    IGNITION = Relay(Addr.GCM, 2, True)
    QD = Relay(Addr.GCM, 3, True)

class OpType(Enum):
    SETVALVE = 1
    SETBULK = 2
    SETDELAYED = 3
    CDH_OP = 4

_data = {
    #CDH
    "OP_CDH_GET_CONNECTED_DEVICES":   [0xc0, OpType.CDH_OP, "getConnectedDevices", None],
    "OP_CDH_CONNECT_DEVICE":          [0xc1, OpType.CDH_OP, "connectDevice", None],

    #FCM
    "OP_FCM_VALVES_SET_ALL":          [0x30, OpType.SETBULK, "setAllValves"],
    "OP_FCM_VALVES_GET_ALL":          [0x31, OpType.SETBULK, "getAllValves"],
    "OP_FCM_PRESS_VENT_SET":          [0x32, OpType.SETVALVE, "pressVentSet", Relays.PRESS_VENT],
    "OP_FCM_PRESS_VENT_DELAY":        [0x33, OpType.SETDELAYED, "pressVentDelay", Relays.PRESS_VENT],
    "OP_FCM_OX_VENT_SET":             [0x34, OpType.SETVALVE, "oxVentSet", Relays.OX_VENT],
    "OP_FCM_OX_VENT_DELAY":           [0x35, OpType.SETDELAYED, "oxVentDelay", Relays.OX_VENT],
    "OP_FCM_FUEL_VENT_SET":           [0x36, OpType.SETVALVE, "fuelVentSet", Relays.FUEL_VENT],
    "OP_FCM_FUEL_VENT_DELAY":         [0x37, OpType.SETDELAYED, "fuelVentDelay", Relays.FUEL_VENT],
    "OP_FCM_FUEL_CC_SET":             [0x38, OpType.SETVALVE, "fuelCCSet", Relays.FUEL_CC],
    "OP_FCM_FUEL_CC_DELAY":           [0x39, OpType.SETDELAYED, "fuelCCDelay", Relays.FUEL_CC],
    "OP_FCM_OX_CC_SET":               [0x3a, OpType.SETVALVE, "oxCCSet", Relays.OX_CC],
    "OP_FCM_OX_CC_DELAY":             [0x3b, OpType.SETDELAYED, "oxCCDelay", Relays.OX_CC],
    "OP_FCM_OX_DUMP_SET":             [0x3c, OpType.SETVALVE, "oxDumpSet", Relays.OX_DUMP],
    "OP_FCM_OX_DUMP_DELAY":           [0x3d, OpType.SETDELAYED, "oxDumpDelay", Relays.OX_DUMP],

    #GCM
    "OP_GCM_IGNITION_SET":            [0x40, OpType.SETVALVE, "ignitionSet", Relays.IGNITION],
    "OP_GCM_QD_SET":                  [0x41, OpType.SETVALVE, "qdSet", Relays.QD],
    "OP_GCM_KBTL_FILL_SET":           [0x42, OpType.SETVALVE, "kbtlSet", Relays.KBTL_FILL],
    "OP_GCM_TBTL_FILL_SET":           [0x43, OpType.SETVALVE, "tbtlSet", Relays.TBTL_FILL]
}

opcodes = {}
op_POS_TYPE = 0;
op_POS_STR = 1;
op_POS_RELAY = 2;

for key in _data:
    name = key.strip("OP_")

    copy = _data[key].copy()
    copy.append(name)
    value = copy.pop(0)
    globals()[key] = value
    opcodes[value] = copy
