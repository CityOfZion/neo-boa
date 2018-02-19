from bytecode import UNSET, Label, Instr, Bytecode, BasicBlock, ControlFlowGraph
from boa.code import pyop

class BlockType():
    MAKE_FUNCTION = 0
    CALL_FUNCTION = 1
    MAKE_CLASS = 2
    IMPORT_ITEM = 3
    MODULE_VAR = 4
    DOC_STRING = 5
    LOAD_CONST = 6
    UNKNOWN = 0

def get_block_type(block):
    for instr in block:
        if instr.opcode in [pyop.IMPORT_FROM, pyop.IMPORT_NAME, pyop.IMPORT_STAR]:
            return BlockType.IMPORT_ITEM
        if instr.opcode == pyop.MAKE_FUNCTION:
            return BlockType.MAKE_FUNCTION
        if instr.opcode == pyop.LOAD_BUILD_CLASS:
            return BlockType.MAKE_CLASS
        if instr.opcode == pyop.CALL_FUNCTION:
            return BlockType.CALL_FUNCTION
    return BlockType.UNKNOWN


def print_block(blocks, block, seen=None):
    # avoid loop: remember which blocks were already seen
    if seen is None:
        seen = set()
    if id(block) in seen:
        return
    seen.add(id(block))

    # display instructions of the block
    print("Block #%s" % (1 + blocks.get_block_index(block)))
    for instr in block:
        if isinstance(instr.arg, BasicBlock):
            arg = "<block #%s>" % (1 + blocks.get_block_index(instr.arg))
        elif instr.arg is not UNSET:
            arg = repr(instr.arg)
        else:
            arg = ''
        print("    [%s] %s %s" % (instr.lineno,instr.name, arg))

    # is the block followed directly by another block?
    if block.next_block is not None:
        print("    => <block #%s>"
              % (1 + blocks.get_block_index(block.next_block)))

    print()

    # display the next block
    if block.next_block is not None:
        print_block(blocks, block.next_block, seen)

    # display the block linked by jump (if any)
    target_block = block.get_jump()
    if target_block is not None:
        print_block(blocks, target_block, seen)



