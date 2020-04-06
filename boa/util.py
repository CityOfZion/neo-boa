from bytecode import UNSET, Label, Instr, Bytecode, BasicBlock, ControlFlowGraph
from boa.code import pyop
import glob
import importlib


class BlockType():
    MAKE_FUNCTION = 0
    CALL_FUNCTION = 1
    MAKE_CLASS = 2
    IMPORT_ITEM = 3
    MODULE_VAR = 4
    DOC_STRING = 5
    LOAD_CONST = 6
    ACTION_REG = 7
    APPCALL_REG = 8
    UNKNOWN = 9


def get_block_type(block):
    default = BlockType.UNKNOWN
    for instr in block:
        if instr.opcode == pyop.LOAD_NAME and instr.arg == 'RegisterAction':
            if default != BlockType.UNKNOWN:
                return default
            return BlockType.ACTION_REG
        elif instr.opcode == pyop.LOAD_NAME and instr.arg == 'RegisterAppCall':
            if default != BlockType.UNKNOWN:
                return default
            return BlockType.APPCALL_REG
        elif instr.opcode in [pyop.IMPORT_FROM, pyop.IMPORT_NAME, pyop.IMPORT_STAR]:
            if default != BlockType.UNKNOWN:
                return default
            return BlockType.IMPORT_ITEM
        elif instr.opcode == pyop.MAKE_FUNCTION:
            return BlockType.MAKE_FUNCTION
        elif instr.opcode == pyop.LOAD_BUILD_CLASS:
            if default != BlockType.UNKNOWN:
                return default
            return BlockType.MAKE_CLASS
        elif instr.opcode == pyop.CALL_FUNCTION:
            if default != BlockType.UNKNOWN:
                return default
            default = BlockType.CALL_FUNCTION

    return default
