from bytecode import Instr, Bytecode, Label
from boa.code.vmtoken import VMTokenizer
from boa.code.expression import Expression
from boa.code import pyop
from boa.code.ast_preprocess import preprocess_method_body
from uuid import uuid4

import pdb
import dis


class method(object):

    code = None
    bytecode = None

    block = None

    blocks = []

    stack_size = 0

    tokens = []
    tokenizer = None

    address = 0

    module = None

    name = None
    module_name = None

    dictionary_defs = None

    start_line_no = None

    _blocks = None
    _expressions = None

    _scope = None

    _forloop_counter = 0

    _extra = None

    _id = None

    code_object = None

    @property
    def id(self):
        return self._id

    @property
    def forloop_counter(self):
        self._forloop_counter += 1
        return self._forloop_counter

    @property
    def vm_tokens(self):
        """
        Returns a list of all vm tokens in this method.

        :return: a list of vm tokens in this method
        :rtype: list
        """

        return self.tokenizer.vm_tokens

    @property
    def is_interop(self):
        if 'boa.interop' in self.full_name:
            return True
        if 'boa.builtins' in self.full_name and self.full_name != 'boa.builtins.range':
            return True
        return False

    @property
    def full_name(self):
        if len(self.module_name):
            return '%s.%s' % (self.module_name, self.name)
        return self.name

    @property
    def scope(self):
        return self._scope

    @property
    def args(self):
        return self.bytecode.argnames

    @property
    def stacksize(self):
        return self.bytecode.argcount + len(self._blocks) + 2

    def __init__(self, module, block, module_name, extra):
        self.module = module
        self.block = block
        self.module_name = module_name
        self._extra = extra
        self._id = uuid4()
        self.name = self.block[1].arg
        self.start_line_no = self.block[0].lineno
        self.code_object = self.block[0].arg

#        dis.dis(code_object)
        self.code, self.dictionary_defs = preprocess_method_body(self.code_object)

        self.bytecode = Bytecode.from_code(self.code)

        self.setup()

    def setup(self):

        self._scope = {}

        for index, name in enumerate(self.bytecode.argnames):
            self._scope[name] = index

        blocks = []

        # find LOAD_GLOBALS
        gbl = []
        for instr in self.bytecode:
            if isinstance(instr, Instr) and instr.opcode == pyop.LOAD_GLOBAL:
                gbl.append(instr.arg)

        # if there are global things passed in
        # we want to check if they are used in the method
        # and if so, load them in
        global_blocks = []

        if len(self._extra):
            for item in self._extra:
                if item[-1].opcode == pyop.STORE_NAME:
                    if item[-1].arg in gbl:
                        global_blocks.append(item)
                        self.add_to_scope(item[-1].arg)
                        if item[0].opcode == pyop.LOAD_NAME:
                            item[0].opcode = pyop.LOAD_GLOBAL
            blocks = global_blocks

        instructions = []
        last_ln = self.bytecode[0].lineno
        for instr in self.bytecode:
            if not isinstance(instr, Label) and instr.lineno != last_ln:
                last_ln = instr.lineno
                if len(instructions):
                    blocks.append(instructions)
                instructions = []
            if not isinstance(instr, Label) and instr.opcode == pyop.STORE_FAST:
                self.add_to_scope(instr.arg)

            instructions.append(instr)
        if len(instructions):
            blocks.append(instructions)

        self._blocks = blocks

        self.tokenizer = VMTokenizer(self)

        self._expressions = []

    def add_to_scope(self, argname):
        if argname not in self.scope.keys():
            current_total = len(self._scope)
            self._scope[argname] = current_total

    def prepare(self):

        last_exp = None
        for block in self._blocks:
            exp = Expression(block, self.tokenizer, self)
            self._expressions.append(exp)
            if last_exp:
                last_exp.next = exp
            last_exp = exp

        for exp in self._expressions:
            exp.tokenize()

        self.convert_breaks()
        self.convert_jumps()

    def convert_jumps(self):
        filtered = []
        for vmtoken in self.tokenizer.vm_tokens.values():
            if vmtoken.pytoken:
                filtered.append(vmtoken)
        for vmtoken in filtered:
            if vmtoken.pytoken.jump_from and not vmtoken.pytoken.jump_found:
                for vmtoken2 in filtered:
                    if vmtoken2.pytoken.jump_target == vmtoken.pytoken.jump_from:
                        diff = vmtoken2.addr - vmtoken.addr
                        vmtoken.data = diff.to_bytes(2, 'little', signed=True)
                        vmtoken2.pytoken.jump_from_addr = vmtoken.addr
                        vmtoken.pytoken.jump_to_addr = vmtoken2.addr

    def convert_breaks(self):
        tokens = list(self.tokenizer.vm_tokens.values())
        setup_token_label = None

        for tkn in tokens:
            if tkn.pytoken:
                if tkn.pytoken.pyop == pyop.SETUP_LOOP:
                    setup_token_label = tkn.pytoken.jump_from
                if tkn.pytoken.pyop == pyop.BREAK_LOOP:
                    if not setup_token_label:
                        raise Exception("No loopsetup for break")
                    tkn.pytoken.jump_from = setup_token_label
