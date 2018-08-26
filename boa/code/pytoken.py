from bytecode import Instr, UNSET, Compare, Label
from boa.interop import VMOp
from boa.code import pyop
from logzero import logger
import opcode


class PyToken():

    instruction = None  # type:Instr
    expression = None
    index = 0

    jump_found = False

    jump_target = None
    jump_from = None
    jump_from_addr = None
    jump_to_addr = None

    is_dynamic_appcall = False

    _methodname = None

    is_breakpoint = False

    def __init__(self, instruction, expression, index, fallback_ln):
        self.instruction = instruction
        self.expression = expression
        self.index = index
        self._methodname = None
        self.jump_from = None
        self.jump_target = None
        self.jump_found = False
        self.jump_from_addr = None
        self.jump_to_addr = None
        # self.jump_to_addr_abs = None
        # self.jump_from_addr_abs = None

        if isinstance(instruction, Label):
            self.jump_target = instruction
            self.instruction = Instr("NOP", lineno=fallback_ln)
        elif isinstance(instruction.arg, Label):
            self.jump_from = instruction.arg

    @property
    def jump_to_addr_abs(self):
        if self.jump_to_addr and self.expression.container_method:
            return self.jump_to_addr + self.expression.container_method.address
        return 0

    @property
    def jump_from_addr_abs(self):
        if self.jump_from_addr and self.expression.container_method:
            return self.jump_from_addr + self.expression.container_method.address
        return 0

    @property
    def file(self):
        try:
            return self.expression.container_method.module.path
        except Exception as e:
            print("Could not get file %s " % e)
        return None

    @property
    def method_lineno(self):
        return self.expression.container_method.start_line_no - 1

    @property
    def method_name(self):
        return self.expression.container_method.name

    @property
    def lineno(self):
        return self.instruction.lineno

    @property
    def arg_str(self):
        #        print("INSTRUCTION ARG: %s %s" % (type(self.instruction.arg), self.instruction.arg))
        params = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
        if self.jump_target:
            return 'from %s' % (self.jump_from_addr_abs)
        elif self.jump_from:
            return 'to %s' % (self.jump_to_addr_abs)
        elif self._methodname:
            return '%s(%s)' % (self._methodname, ','.join(params[0:self.instruction.arg]))
        elif isinstance(self.instruction.arg, Compare):
            return self.instruction.arg.name
        elif isinstance(self.instruction.arg, bytes) or isinstance(self.instruction.arg, bytearray):
            return str(self.instruction.arg)
        return self.instruction.arg if self.instruction.arg != UNSET else ''

    @property
    def args(self):
        return self.instruction.arg

    @property
    def pyop(self):
        return self.instruction.opcode

    @property
    def func_name(self):
        if not self._methodname:
            self._methodname = self.expression.lookup_method_name(self.index)
        return self._methodname

    @property
    def num_params(self):
        return self.args

    def to_vm(self, tokenizer, prev_token=None):
        """

        :param tokenizer:
        :param prev_token:
        :return:
        """

        op = self.instruction.opcode
#        print("CONVERTING OP: %s %s " % (self.instruction.name, self.instruction.arg))

        if op == pyop.NOP:
            tokenizer.convert1(VMOp.NOP, self)

        elif op == pyop.RETURN_VALUE:
            tokenizer.method_end_items()
            tokenizer.convert1(VMOp.RET, self)

        # control flow

        elif op == pyop.JUMP_FORWARD:
            tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

        elif op == pyop.JUMP_ABSOLUTE:
            tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

        elif op == pyop.POP_JUMP_IF_FALSE:
            tokenizer.convert1(
                VMOp.JMPIFNOT, self, data=bytearray(2))
        # JUMP_IF_FALSE_OR_POP is not supported by the VM
        # elif op == pyop.JUMP_IF_FALSE_OR_POP:
        #     tokenizer.convert_pop_jmp_if(self)
        #         VMOp.JMPIFNOT, self, data=bytearray(2))

        elif op == pyop.POP_JUMP_IF_TRUE:
            tokenizer.convert_pop_jmp_if(self)

        # JUMP_IF_TRUE_OR_POP is not supported by the VM
        # elif op == pyop.JUMP_IF_TRUE_OR_POP:
        #     tokenizer.convert_pop_jmp_if(self)
        # loops
        elif op == pyop.SETUP_LOOP:
            tokenizer.convert1(VMOp.NOP, self)
        elif op == pyop.BREAK_LOOP:
            tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

        elif op == pyop.POP_BLOCK:
            tokenizer.convert1(VMOp.NOP, self)

        elif op == pyop.FROMALTSTACK:
            tokenizer.convert1(VMOp.FROMALTSTACK, self)
        elif op == pyop.DROP:
            tokenizer.convert1(VMOp.DROP, self)
        elif op == pyop.XSWAP:
            tokenizer.convert1(VMOp.XSWAP, self)
        elif op == pyop.ROLL:
            tokenizer.convert1(VMOp.ROLL, self)

        # loading constants ( ie 1, 2 etc)
        elif op == pyop.LOAD_CONST:
            tokenizer.convert_load_const(self)

        # storing / loading local variables
        elif op in [pyop.STORE_FAST, pyop.STORE_NAME]:
            tokenizer.convert_store_local(self)
        elif op == pyop.LOAD_GLOBAL:

            if self.instruction.arg in self.expression.container_method.scope:
                tokenizer.convert_load_local(self)
            else:
                self.expression.add_method(self)

        elif op in [pyop.LOAD_FAST, pyop.LOAD_NAME]:
            tokenizer.convert_load_local(self)

        # unary ops

        elif op == pyop.UNARY_INVERT:
            tokenizer.convert1(VMOp.INVERT, self)

        elif op == pyop.UNARY_NEGATIVE:
            tokenizer.convert1(VMOp.NEGATE, self)

        elif op == pyop.UNARY_NOT:
            tokenizer.convert1(VMOp.NOT, self)

#            elif op == pyop.UNARY_POSITIVE:
            # hmmm
#                tokenizer.convert1(VMOp.ABS, self)
#                pass

        # math
        elif op in [pyop.BINARY_ADD, pyop.INPLACE_ADD]:

            # we can't tell by looking up the last token what type of item it was
            # will need to figure out a different way of concatting strings
            #                if prev_token and type(prev_token.args) is str:
            #                    tokenizer.convert1(VMOp.CAT, self)
            #                else:
            tokenizer.convert1(VMOp.ADD, self)

        elif op in [pyop.BINARY_SUBTRACT, pyop.INPLACE_SUBTRACT]:
            tokenizer.convert1(VMOp.SUB, self)

        elif op in [pyop.BINARY_MULTIPLY, pyop.INPLACE_MULTIPLY]:
            tokenizer.convert1(VMOp.MUL, self)

        elif op in [pyop.BINARY_FLOOR_DIVIDE, pyop.BINARY_TRUE_DIVIDE,
                    pyop.INPLACE_FLOOR_DIVIDE, pyop.INPLACE_TRUE_DIVIDE]:
            tokenizer.convert1(VMOp.DIV, self)

        elif op in [pyop.BINARY_MODULO, pyop.INPLACE_MODULO]:
            tokenizer.convert1(VMOp.MOD, self)

        elif op in [pyop.BINARY_OR, pyop.INPLACE_OR]:
            tokenizer.convert1(VMOp.OR, self)

        elif op in [pyop.BINARY_AND, pyop.INPLACE_AND]:
            tokenizer.convert1(VMOp.AND, self)

        elif op in [pyop.BINARY_XOR, pyop.INPLACE_XOR]:
            tokenizer.convert1(VMOp.XOR, self)

        elif op in [pyop.BINARY_LSHIFT, pyop.INPLACE_LSHIFT]:
            tokenizer.convert1(VMOp.SHL, self)

        elif op in [pyop.BINARY_RSHIFT, pyop.INPLACE_RSHIFT]:
            tokenizer.convert1(VMOp.SHR, self)

        # compare

        elif op == pyop.COMPARE_OP:

            #            pdb.set_trace()
            if self.instruction.arg == Compare.GT:
                tokenizer.convert1(VMOp.GT, self)
            elif self.instruction.arg == Compare.GE:
                tokenizer.convert1(VMOp.GTE, self)
            elif self.instruction.arg == Compare.LT:
                tokenizer.convert1(VMOp.LT, self)
            elif self.instruction.arg == Compare.LE:
                tokenizer.convert1(VMOp.LTE, self)
            elif self.instruction.arg == Compare.EQ:
                tokenizer.convert1(VMOp.EQUAL, self)
            elif self.instruction.arg == Compare.IS:
                tokenizer.convert1(VMOp.EQUAL, self)
            elif self.instruction.arg in [Compare.NE, Compare.IS_NOT]:
                tokenizer.convert1(VMOp.NUMNOTEQUAL, self)
            elif self.instruction.arg == Compare.IN:
                tokenizer.convert1(VMOp.SWAP, self)
                tokenizer.convert1(VMOp.HASKEY, self)

        # arrays
        elif op == pyop.BUILD_LIST:
            tokenizer.convert_new_array(self)
        elif op == pyop.DUP_TOP:
            tokenizer.convert1(VMOp.DUP, self)
        elif op == pyop.YIELD_VALUE:
            tokenizer.convert1(VMOp.REVERSE, self)
        elif op == pyop.STORE_SUBSCR:
            tokenizer.convert_store_subscr(self)
        elif op == pyop.BINARY_SUBSCR:
            tokenizer.convert1(VMOp.PICKITEM, self)

        # dict
        elif op == pyop.BUILD_CONST_KEY_MAP:
            tokenizer.convert1(VMOp.NEWMAP, self)
        elif op == pyop.BUILD_MAP:
            tokenizer.convert1(VMOp.NEWMAP, self)

        elif op == pyop.BUILD_SLICE:
            tokenizer.convert_build_slice(self)

        elif op in [pyop.CALL_FUNCTION, pyop.CALL_METHOD]:
            tokenizer.convert_method_call(self)
#        elif op == pyop.LOAD_METHOD:

        elif op == pyop.POP_TOP:
            pass
            # if prev_token:
            #     is_action = False
            #     for item in tokenizer.method.module.actions:
            #         if item.method_name == prev_token.func_name:
            #             is_action = True
            #
            # if is_action:
            #     tokenizer.convert1(VMOp.DROP, self)

        elif op == pyop.DUP_TOP_TWO:
            tokenizer.convert_dup_top_two(self)
        elif op == pyop.ROT_THREE:
            tokenizer.convert1(VMOp.ROT, self)
        elif op == pyop.ROT_TWO:
            tokenizer.convert1(VMOp.SWAP)
        elif op == pyop.RAISE_VARARGS:
            pass
#        elif op == pyop.CALL_METHOD:
#            pass
        elif op == pyop.EXTENDED_ARG:
            tokenizer.convert1(VMOp.NOP, self)
        else:
            #            import pdb
            #            pdb.set_trace()
            logger.warning("Op Not Converted %s %s %s %s %s" % (self.instruction.arg, self.instruction.name, self.method_name, self.lineno, self.method_lineno))
