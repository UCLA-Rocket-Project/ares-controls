#MCU constants
from enum import Enum
from collections import namedtuple

SERIAL_STOPCODE = 0xFF

class Addr:
    GCM = 0xA1 #subject to change
    FCM = 0xA2 #subject to change

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

class Opcode(Enum):
    RELAY_OFF = 0xC0
    RELAY_ON = 0xC1
    RELAY_SET_DELAYED = 0xCF

IS_NORMALLY_CLOSED = {
    Relays.PRESS_PROP: True,
    Relays.OX_FILL: True,
    Relays.PRESS_VENT: False
}
