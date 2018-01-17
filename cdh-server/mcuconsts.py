#MCU constants
from enum import Enum
from collections import namedtuple
import opcodes as op

class Addr:
    GCM = 0x80 #subject to change
    FCM = 0x40  #subject to change
    CDH = 0xC0 #subject to change

Relay = namedtuple('Relay', 'addr relay')

class Relays(Enum):
    PRESS_VENT = Relay(Addr.FCM, 0)
    OX_VENT = Relay(Addr.FCM, 1)
    FUEL_VENT = Relay(Addr.FCM, 2)
    FUEL_CC = Relay(Addr.FCM, 3)
    OX_CC = Relay(Addr.FCM, 4)
    OX_DUMP = Relay(Addr.FCM, 5)
    
    KBTL_FILL = Relay(Addr.GCM, 0)
    TBTL_FILL = Relay(Addr.GCM, 1)
    IGNITION = Relay(Addr.GCM, 2)
    QD = Relay(Addr.GCM, 3)

class Opcode(Enum):
    RELAY_OFF = 0x10
    RELAY_ON = 0x11
    RELAY_GET = 0x12
    RELAY_GET_ALL_STATES = 0x13
    RELAY_ALL_OFF = 0x14
    RELAY_ALL_ON = 0x15
    RELAY_SET_ALL = 0x16

FCMRelays = [
    Relays.PRESS_VENT,
    Relays.OX_VENT,
    Relays.FUEL_VENT,
    Relays.FUEL_CC,
    Relays.OX_CC,
    Relays.OX_DUMP
]

OPCODE_MATCHER = {
	op.PRESS_VENT_SET: Relays.PRESS_VENT,
	op.PRESS_VENT_DELAYED_SET: Relays.PRESS_VENT,
	op.OX_VENT_SET: Relays.OX_VENT,
	op.OX_VENT_DELAYED_SET: Relays.OX_VENT,
        op.OX_DUMP_SET: Relays.OX_DUMP,
	op.FUEL_VENT_SET: Relays.FUEL_VENT,
	op.FUEL_VENT_DELAYED_SET: Relays.FUEL_VENT,
	op.FUEL_CC_SET: Relays.FUEL_CC,
	op.FUEL_CC_DELAYED_SET: Relays.FUEL_CC,
	op.OX_CC_SET: Relays.OX_CC,
	op.OX_CC_DELAYED_SET: Relays.OX_CC,
	op.TBTL_FILL_SET: Relays.TBTL_FILL,
        op.KBTL_FILL_SET: Relays.KBTL_FILL,
	op.IGNITION_SET: Relays.IGNITION,
        op.QD_SET: Relays.QD
	# op.IGNITE_FOR_TIME: Relays.IGNITION
}

IS_NORMALLY_CLOSED = {
    Relays.PRESS_VENT: False,
    Relays.FUEL_VENT: False,
    Relays.OX_VENT: False,
    Relays.FUEL_CC: True,
    Relays.OX_CC: True,
    Relays.OX_DUMP: True,
    Relays.TBTL_FILL: True,
    Relays.KBTL_FILL: True,
    Relays.IGNITION: True,
    Relays.QD: True
}
