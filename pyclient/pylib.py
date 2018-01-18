from libares import constants
from pyclient import serverClient as _sc

lambdas = {}

for opcode in constants.opcodes:
    data = constants.opcodes[opcode]
    if data[constants.op_POS_TYPE] == constants.OpType.SETVALVE:
        name = data[constants.op_POS_STR]
        nc = data[constants.op_POS_RELAY].value.nc
        lambdas[name] = lambda set, _opcode=opcode, _nc=nc: _sc.send(bytes([_opcode, set == _nc]))

lambdas['connect'] = lambda host, port: _sc.connect(host, port)

commands = []

for function in lambdas:
    commands.append(function)

lambdas['help'] = lambda commands=commands: print("\nList of commands: {}\n".format(", ".join(commands)))

globals().update(lambdas)

print("""

 # Welcome to Ares PyLib!
 # Type pylib.help() for a list of commands, or pylib.connect() to get started

""")
