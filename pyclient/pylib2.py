from libares import constants
import serverClient as _sc
import code

lambdas = {}

commands = []

def init():
    for opcode in constants.opcodes:
        data = constants.opcodes[opcode]
        if data[constants.op_POS_TYPE] == constants.OpType.SETVALVE:
            name = data[constants.op_POS_STR]
            nc = data[constants.op_POS_RELAY].value.nc
            lambdas[name] = lambda set, _opcode=opcode, _nc=nc: _sc.send(bytes([_opcode, set == _nc]))

    lambdas['connect'] = lambda host, port: _sc.connect(host, port)

    for function in lambdas:
        commands.append(function)

    lambdas['help'] = help

    globals().update(lambdas)

    print("""\n
    # Welcome to Ares PyLib!
    # Type help() for a list of commands, or connect(HOST, PORT) to get started\n\n""")


def help():
    print("""
    List of commands: {}
    Required parameter: True/False (for Open/Close)
    """.format(", ".join(commands)))

init()
code.interact(banner=None, readfunc=None, local=lambdas)
