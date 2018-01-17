from boa.code import pyop

from byteplay3 import Label, isopcode, haslocal

from opcode import opname

from boa.blockchain.vm import VMOp

NON_RETURN_SYS_CALLS = ['Notify', 'print', 'Log', 'Put', 'Register',
                        'reverse', 'append', 'remove',
                        'Delete', 'SetVotes', 'ContractDestroy',
                        'MerkleRoot', 'Hash', 'PrevHash', 'GetHeader', ]


class PyToken(object):

    """

    """
    py_op = None

    args = None

    line_no = None

    addr = None

    tokenizer = None

    jump_label = None

    array_processed = False

    array_item = None

    # method calling things

    func_processed = False

    func_params = None

    _func_name = None
    func_type = None

    script_hash_token = None

    is_dynamic_appcall = False

    instance_type = None
    instance_name = None

    @property
    def func_name(self):
        return self._func_name

    @func_name.setter
    def func_name(self, value):
        self._func_name = value

    @property
    def op_name(self):
        """

        :return:
        """
        if type(self.py_op) is int:
            return opname[self.py_op]
        elif type(self.py_op) is Label:
            return 'Label %s ' % self.py_op
        return self.py_op

    @property
    def is_op(self):
        """

        :return:
        """
        return isopcode(self.py_op)

    @property
    def is_local(self):
        """

        :return:
        """
        return haslocal(self.py_op)

    @property
    def arg_s(self):
        """

        :return:
        """
        if self.args:
            return str(self.args)
        return ''

    def __init__(self, op, lineno, index=None, args=None, array_item=None):

        self.py_op = op

        self.args = args

        self.line_no = lineno

        self.addr = index

        self.array_item = array_item

    def __str__(self):
        if self.args:
            if type(self.args) is Label:
                arg = str(self.args)
            else:
                arg = self.args
            return '%s      %s   %s  --> %s ' % (self.line_no, self.addr, self.op_name, arg)
        return '%s      %s   %s' % (self.line_no, self.addr, self.op_name)

    def to_vm(self, tokenizer, prev_token=None):
        """

        :param tokenizer:
        :param prev_token:
        :return:
        """
        self.tokenizer = tokenizer
        token = None

        if self.is_op:

            op = self.py_op

            if op == pyop.NOP:
                token = tokenizer.convert1(VMOp.NOP, self)

            elif op == pyop.RETURN_VALUE:
                token = tokenizer.convert1(VMOp.RET, self)

            # control flow
            elif op == pyop.BR_S:
                token = tokenizer.convert1(VMOp.JMP, self, data=self.args)

            elif op == pyop.JUMP_FORWARD:
                token = tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

            elif op == pyop.JUMP_ABSOLUTE:
                token = tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

            elif op == pyop.POP_JUMP_IF_FALSE:
                token = tokenizer.convert1(
                    VMOp.JMPIFNOT, self, data=bytearray(2))

            elif op == pyop.POP_JUMP_IF_TRUE:
                token = tokenizer.convert_pop_jmp_if(self)
            # loops
            elif op == pyop.SETUP_LOOP:
                token = tokenizer.convert1(VMOp.NOP, self)

            elif op == pyop.BREAK_LOOP:
                token = tokenizer.convert1(VMOp.JMP, self, data=bytearray(2))

            elif op == pyop.FOR_ITER:
                token = tokenizer.convert1(VMOp.NOP, self)

#            elif op == pyop.GET_ITER:
#                token = tokenizer.convert1(VMOp.NOP, self)

            elif op == pyop.POP_BLOCK:
                token = tokenizer.convert1(VMOp.NOP, self)

            elif op == pyop.FROMALTSTACK:
                token = tokenizer.convert1(VMOp.FROMALTSTACK, self)
            elif op == pyop.DROP:
                token = tokenizer.convert1(VMOp.DROP, self)
            elif op == pyop.XSWAP:
                token = tokenizer.convert1(VMOp.XSWAP, self)
            elif op == pyop.ROLL:
                token = tokenizer.convert1(VMOp.ROLL, self)

            # loading constants ( ie 1, 2 etc)
            elif op == pyop.LOAD_CONST:
                token = tokenizer.convert_load_const(self)

            # storing / loading local variables
            elif op in [pyop.STORE_FAST, pyop.STORE_NAME]:
                token = tokenizer.convert_store_local(self)

            elif op in [pyop.LOAD_FAST, pyop.LOAD_NAME, pyop.LOAD_GLOBAL]:
                token = tokenizer.convert_load_local(self)

            # unary ops

#            elif op == pyop.UNARY_INVERT:
#                token = tokenizer.convert1(VMOp.INVERT, self)

            elif op == pyop.UNARY_NEGATIVE:
                token = tokenizer.convert1(VMOp.NEGATE, self)

            elif op == pyop.UNARY_NOT:
                token = tokenizer.convert1(VMOp.NOT, self)

#            elif op == pyop.UNARY_POSITIVE:
                # hmmm
#                token = tokenizer.convert1(VMOp.ABS, self)
#                pass

            # math
            elif op in [pyop.BINARY_ADD, pyop.INPLACE_ADD]:

                # we can't tell by looking up the last token what type of item it was
                # will need to figure out a different way of concatting strings
                #                if prev_token and type(prev_token.args) is str:
                #                    token = tokenizer.convert1(VMOp.CAT, self)
                #                else:
                token = tokenizer.convert1(VMOp.ADD, self)

            elif op in [pyop.BINARY_SUBTRACT, pyop.INPLACE_SUBTRACT]:
                token = tokenizer.convert1(VMOp.SUB, self)

            elif op in [pyop.BINARY_MULTIPLY, pyop.INPLACE_MULTIPLY]:
                token = tokenizer.convert1(VMOp.MUL, self)

            elif op in [pyop.BINARY_FLOOR_DIVIDE, pyop.BINARY_TRUE_DIVIDE,
                        pyop.INPLACE_FLOOR_DIVIDE, pyop.INPLACE_TRUE_DIVIDE]:
                token = tokenizer.convert1(VMOp.DIV, self)

            elif op in [pyop.BINARY_MODULO, pyop.INPLACE_MODULO]:
                token = tokenizer.convert1(VMOp.MOD, self)

            elif op == [pyop.BINARY_OR, pyop.INPLACE_OR]:
                token = tokenizer.convert1(VMOp.BOOLOR, self)

            elif op == [pyop.BINARY_AND, pyop.INPLACE_AND]:
                token = tokenizer.convert1(VMOp.BOOLAND, self)

            elif op == [pyop.BINARY_XOR, pyop.INPLACE_XOR]:
                token = tokenizer.convert1(VMOp.XOR, self)

            elif op in [pyop.BINARY_LSHIFT, pyop.INPLACE_LSHIFT]:
                token = tokenizer.convert1(VMOp.SHL, self)

            elif op in [pyop.BINARY_RSHIFT, pyop.INPLACE_RSHIFT]:
                token = tokenizer.convert1(VMOp.SHR, self)

            # compare

            elif op == pyop.COMPARE_OP:

                if self.args == '>':
                    token = tokenizer.convert1(VMOp.GT, self)
                elif self.args == '>=':
                    token = tokenizer.convert1(VMOp.GTE, self)
                elif self.args == '<':
                    token = tokenizer.convert1(VMOp.LT, self)
                elif self.args == '<=':
                    token = tokenizer.convert1(VMOp.LTE, self)
                elif self.args == '==':
                    token = tokenizer.convert1(VMOp.NUMEQUAL, self)
                elif self.args == 'is':
                    token = tokenizer.convert1(VMOp.EQUAL, self)
                elif self.args == '!=':
                    token = tokenizer.convert1(VMOp.NUMNOTEQUAL, self)

            # arrays
            elif op == pyop.BUILD_LIST:
                token = tokenizer.convert_new_array(self)
            elif op == pyop.SETITEM:
                token = tokenizer.convert_set_element(self, self.args)
#                token = tokenizer.convert1(VMOp.SETITEM,self, data=self.args)
            elif op == pyop.STORE_SUBSCR:
                # this wont occur because this op is preprocessed into a SETITEM op
                pass
            elif op == pyop.BINARY_SUBSCR:
                token = tokenizer.convert1(VMOp.PICKITEM, self)

            elif op == pyop.BUILD_SLICE:
                token = tokenizer.convert_build_slice(self)

            # objects

            elif op == pyop.LOAD_CLASS_ATTR:
                token = tokenizer.convert_load_attr(self)

            elif op == pyop.STORE_ATTR:
                token = tokenizer.convert_store_attr(self)

            elif op == pyop.CALL_FUNCTION:
                token = tokenizer.convert_method_call(self)

            elif op == pyop.POP_TOP:
                if prev_token.func_name not in NON_RETURN_SYS_CALLS:
                    is_action = False
                    for item in tokenizer.method.module.actions:
                        if item.method_name == prev_token.func_name:
                            is_action = True

                    if not is_action:
                        token = tokenizer.convert1(VMOp.DROP, self)

#            else:
#                print("OP NOT CONVERTED %s " % op)

        return token
