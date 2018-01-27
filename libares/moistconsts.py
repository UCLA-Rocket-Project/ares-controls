from collections import namedtuple
from libares.constants import *

Switch = namedtuple('Switch', 'opcode is_no')

QUICK_DISC = Switch(OP_GCM_QD_SET, 0)
IGNITE = Switch(OP_GCM_IGNITION_SET, 0)
KBTL_FILL = Switch(OP_GCM_KBTL_FILL_SET, 0)
TBTL_FILL = Switch(OP_GCM_TBTL_FILL_SET, 0)
OX_FILL = Switch(OP_GCM_OX_FILL_SET, 0)

OX_VENT = Switch(OP_FCM_OX_VENT_SET, 1)
OX_DUMP = Switch(OP_FCM_OX_DUMP_SET, 0)
PRESS_VENT = Switch(OP_FCM_PRESS_VENT_SET, 1)
FUEL_VENT = Switch(OP_FCM_FUEL_VENT_SET, 1)
FUEL_CC = Switch(OP_FCM_FUEL_CC_SET, 0)
OX_CC = Switch(OP_FCM_OX_CC_SET, 0)

LEDMAP = {
    TBTL_FILL: 16,
    KBTL_FILL: 20,
    OX_FILL: 21,
    QUICK_DISC: 26,
    PRESS_VENT: 12,
    OX_VENT: 7,
    FUEL_VENT: 8,
    OX_DUMP: 25,
    OX_CC: 24,
    FUEL_CC: 23,
    IGNITE: 18
}

IGNITE_INDEX = 13

MAP = {
    5: TBTL_FILL,
    11: KBTL_FILL,
    9: OX_FILL,
    10: QUICK_DISC,
    22: PRESS_VENT,
    27: OX_VENT,
    17: FUEL_VENT,
    4: OX_DUMP,
    3: OX_CC,
    2: FUEL_CC,
    IGNITE_INDEX: IGNITE
}

ENABLE_PIN = 19
