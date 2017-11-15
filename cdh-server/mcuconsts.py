#MCU constants
from enum import Enum
from collections import namedtuple
import opcodes as op

class Addr:
    GCM = 0x80 #subject to change
    FCM = 0x40  #subject to change
    CDH = 0xC0 #subject to change

Relay = namedtuple('Relay', 'addr relay')


FCMRelays = [
    consts.Relays.PRESS_PROP,
    consts.Relays.OX_FILL,
    consts.Relays.PRESS_VENT,
    consts.Relays.OX_VENT,
    consts.Relays.FUEL_VENT,
    consts.Relays.FUEL_CC,
    consts.Relays.OX_CC,
    consts.Relays.OX_DUMP
]

class Relays(Enum):
    PRESS_PROP = Relay(Addr.FCM, 0)
    OX_FILL = Relay(Addr.FCM, 1)
    PRESS_VENT = Relay(Addr.FCM, 2)
    OX_VENT = Relay(Addr.FCM, 3)
    FUEL_VENT = Relay(Addr.FCM, 4)
    FUEL_CC = Relay(Addr.FCM, 5)
    OX_CC = Relay(Addr.FCM, 6)
    OX_DUMP = Relay(Addr.FCM, 7)
    PRESS_FILL = Relay(Addr.GCM, 0)
    IGNITION = Relay(Addr.GCM, 1)
    QD = Relay(Addr.GCM, 2)

class Opcode(Enum):
    RELAY_OFF = 0x10
    RELAY_ON = 0x11
    RELAY_GET = 0x12
    RELAY_GET_ALL_STATES = 0x13
    RELAY_ALL_OFF = 0x14
    RELAY_ALL_ON = 0x15
    RELAY_SET_ALL = 0x16

OPCODE_MATCHER = {
	op.PRESS_PROP_SET: Relays.PRESS_PROP,
	op.OX_FILL_SET: Relays.OX_FILL,
	op.PRESS_VENT_SET: Relays.PRESS_VENT,
	op.PRESS_VENT_DELAYED_SET: Relays.PRESS_VENT,
	op.OX_VENT_SET: Relays.OX_VENT,
	op.OX_VENT_DELAYED_SET: Relays.OX_VENT,
	op.FUEL_VENT_SET: Relays.FUEL_VENT,
	op.FUEL_VENT_DELAYED_SET: Relays.FUEL_VENT,
	op.FUEL_CC_SET: Relays.FUEL_CC,
	op.FUEL_CC_DELAYED_SET: Relays.FUEL_CC,
	op.OX_CC_SET: Relays.OX_CC,
	op.OX_CC_DELAYED_SET: Relays.OX_CC,
	op.PRESS_FILL_SET: Relays.PRESS_FILL,
	op.IGNITION_SET: Relays.IGNITION,
    op.OX_DUMP_SET: Relays.OX_DUMP
	# op.IGNITE_FOR_TIME: Relays.IGNITION
}

IS_NORMALLY_CLOSED = {
	Relays.PRESS_PROP: True,
    Relays.OX_FILL: True,
    Relays.PRESS_VENT: False,
    Relays.FUEL_VENT: False,
    Relays.OX_VENT: False,
    Relays.FUEL_CC: True,
    Relays.OX_CC: True,
    Relays.PRESS_FILL: True,
    Relays.IGNITION: True,
    Relays.QD: True,
    Relays.OX_DUMP: True
}
