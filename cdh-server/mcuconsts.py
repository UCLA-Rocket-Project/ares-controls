#MCU constants
from enum import Enum
from collections import namedtuple
import opcodes as op

SERIAL_STOPCODE = 0xFF

class Addr:
    GCM = 0xA1 #subject to change
    FCM = 0xA2 #subject to change
    CDH = 0xAC #subject to change

Relay = namedtuple('Relay', 'addr relay')

class Relays(Enum):
    PRESS_PROP = Relay(Addr.FCM, 0)
    OX_FILL = Relay(Addr.FCM, 1)
    PRESS_VENT = Relay(Addr.FCM, 2)
    OX_VENT = Relay(Addr.FCM, 3)
    FUEL_VENT = Relay(Addr.FCM, 4)
    FUEL_CC = Relay(Addr.FCM, 5)
    OX_CC = Relay(Addr.FCM, 6)
    PRESS_FILL = Relay(Addr.GCM, 0)
    IGNITION = Relay(Addr.GCM, 1)
    QD = Relay(Addr.GCM, 2)
    ERROR = Relay(Addr.CDH, 0)

class Opcode(Enum):
    RELAY_OFF = 0xC0
    RELAY_ON = 0xC1
    RELAY_SET_DELAYED = 0xCF
    RELAY_SET_ALL = 0xCE
    GET_ALL_RELAY_STATES = 0xC4
    
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
	op.IGNITE_FOR_TIME: Relays.IGNITION
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
    Relays.IGNITION: True
}