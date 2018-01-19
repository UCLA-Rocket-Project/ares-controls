from collections import namedtuple
from libares.constants import *

Switch = namedtuple('Switch', 'opcode is_no')

QUICK_DISC = Switch(OP_GCM_QD_SET, 0)
IGNITE = Switch(OP_GCM_IGNITION_SET, 0)
KBTL_FILL = Switch(OP_GCM_KBTL_FILL_SET, 0)
TBTL_FILL = Switch(OP_GCM_TBTL_FILL_SET, 0)

OX_DUMP = Switch(OP_FCM_OX_DUMP_SET, 0)
PRESS_VENT = Switch(OP_FCM_PRESS_VENT_SET, 0)
OX_VENT = Switch(OP_FCM_OX_VENT_SET, 0)
FUEL_VENT = Switch(OP_FCM_FUEL_VENT_SET, 0)
FUEL_CC = Switch(OP_FCM_FUEL_CC_SET, 0)
OX_CC = Switch(OP_FCM_OX_CC_SET, 0)

LEDMAP = {
    KBTL_FILL: 21,
    OX_DUMP: 12,
    PRESS_VENT: 25,
    OX_VENT: 8,
    FUEL_VENT: 7,
    FUEL_CC: 23,
    OX_CC: 18,
    TBTL_FILL: 16,
    QUICK_DISC: 26,
    IGNITE: 24
}

IGNITE_INDEX = 9

MAP = {
    11: KBTL_FILL,
    5: TBTL_FILL,
    22: QUICK_DISC,
    2: PRESS_VENT,
    3: OX_VENT,
    10: FUEL_VENT,
    13: OX_DUMP,
    4: FUEL_CC,
    17: OX_CC,
    IGNITE_INDEX: IGNITE
}

ENABLE_PIN = 19
