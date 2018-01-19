#MCU constants
from libares.opcodes import *

FCMRelays = []
OPCODE_MATCHER = {}

for r in Relays:
    if r.addr == Addr.FCM:
        FCMRelays.append(r)

for o in opcodes:
    OPCODE_MATCHER[o] = opcodes[o][op_POS_RELAY]
