from bytecode import Instr, Compare, Label
from boa.code import pyop
from boa.code.pytoken import PyToken
from bytecode import Bytecode
import ast
import astor


class Expression(object):

    updated_blocklist = None
    block = None
    container_method = None
    tokenizer = None

    next = None

    methodnames = None

    ops = None

    def __init__(self, block, tokenizer, container_method):
        self.block = block
        self.tokenizer = tokenizer
        self.container_method = container_method
        self.methodnames = []
        self.next = None

        self.ops = []
        for item in self.block:
            if isinstance(item, Instr):
                self.ops.append(item.opcode)

    def add_method(self, pytoken):
        self.methodnames.append(pytoken.instruction.arg)

    def _reverselists(self):
        indices = []
        for index, instr in enumerate(self.updated_blocklist):
            if not isinstance(instr, Label) and instr.opcode == pyop.BUILD_LIST:
                indices.append(index)
        if len(indices):
            output = []
            for index, instr in enumerate(self.updated_blocklist):
                output.append(instr)
                if index in indices:
                    output.append(Instr("DUP_TOP", lineno=instr.lineno))
                    output.append(Instr('YIELD_VALUE', lineno=instr.lineno))
            self.updated_blocklist = output

    def _checkbytearray(self):
        to_remove = []
        for index, instr in enumerate(self.block):
            if not isinstance(instr, Label) and instr.opcode == pyop.LOAD_GLOBAL and instr.arg == 'bytearray':
                self.methodnames.append('bytearray')
                to_remove.append(instr)
                to_remove.append(self.block[index + 2])
        if len(to_remove):
            self._remove_instructions(to_remove)

    def _check_load_attr(self):
        replaceable_attr_calls = ['append', 'remove', 'reverse', 'keys', 'values', 'has_key', 'IterKey', 'IterValue', 'IterNext', 'next', ]
        needs_call_func = []

        for index, instr in enumerate(self.updated_blocklist):
            if not isinstance(instr, Label) and instr.opcode in [pyop.LOAD_ATTR, pyop.LOAD_METHOD]:
                #                if instr.opcode == pyop.LOAD_METHOD:
                #                    self.methodnames.append(instr.arg)
                if instr.arg in replaceable_attr_calls:
                    instr.opcode = pyop.LOAD_GLOBAL
                else:
                    attr_name = 'Get%s' % instr.arg
                    module_methods = self.container_method.module.methods
                    matches = []
                    for n in module_methods:
                        if attr_name in n.full_name:
                            matches.append(n)

                    # these two are special cases for name collisions between
                    # block.Hash, tx.Hash, and input.Hash
                    if len(matches) == 0:
                        attr_name = 'GetTX%s' % instr.arg
                        for n in module_methods:
                            if attr_name in n.full_name:
                                matches.append(n)
                    if len(matches) == 0:
                        attr_name = 'GetInput%s' % instr.arg
                        for n in module_methods:
                            if attr_name in n.full_name:
                                matches.append(n)

                    # Special case for enumerators/iterator
                    if len(matches) == 0:
                        attr_name = 'Enumerator%s' % instr.arg
                        for n in module_methods:
                            if attr_name in n.full_name:
                                matches.append(n)
                    if len(matches) == 0:
                        attr_name = 'Iter%s' % instr.arg
                        for n in module_methods:
                            if attr_name == n.full_name.split('.')[-1]:
                                matches.append(n)

                    if len(matches) == 0:
                        raise Exception("Could not load attribute %s " % instr.arg)
                    elif len(matches) > 1:
                        raise Exception(
                            "Could not determine attribute to load. Options: %s " % [n.full_name for n in matches])
                    else:
                        instr.opcode = pyop.LOAD_GLOBAL
                        instr.arg = attr_name
                        needs_call_func.append(instr)

        blocklist = []
        for index, instr in enumerate(self.updated_blocklist):
            blocklist.append(instr)
            if instr in needs_call_func:
                blocklist.append(Instr('CALL_FUNCTION', 1, lineno=instr.lineno))
        self.updated_blocklist = blocklist

    def _check_function_kwargs(self):
        to_remove = []
        for index, instr in enumerate(self.updated_blocklist):
            if not isinstance(instr, Label) and instr.opcode == pyop.CALL_FUNCTION_KW:
                instr.opcode = pyop.CALL_FUNCTION
                to_remove.append(self.updated_blocklist[index - 1])
        if len(to_remove):
            self._remove_instructions(to_remove)

    def _remove_instructions(self, to_remove):
        updated = []
        for item in self.block:
            if item not in to_remove:
                updated.append(item)
        self.updated_blocklist = updated

    def _checkslice(self):
        last = None
        to_del_index = -1
        for index, instr in enumerate(self.block):
            if isinstance(instr, Instr):
                if last == pyop.BUILD_SLICE and instr.opcode == pyop.BINARY_SUBSCR:
                    to_del_index = index
                last = instr.opcode

        if to_del_index > -1:
            self.block.pop(to_del_index)
            self.updated_blocklist = self.block
            self._checkslice()

    def _ast_to_instr(self, astobj, lineno):

        src = astor.to_source(astobj).replace('"""', "'")

        cp = compile(src, filename='<ast>', mode='eval')
        bc = Bytecode.from_code(cp)
        instructions = bc[:-1]
        for instr in instructions:
            instr.lineno = lineno

        # if its calling a method, we don't want it to do `LOAD_NAME`
        if instructions[-1].opcode == pyop.CALL_FUNCTION and instructions[0].opcode == pyop.LOAD_NAME:
            instructions[0] = Instr("LOAD_GLOBAL", arg=instructions[0].arg, lineno=instructions[0].lineno)

        return instructions

    def _check_dictionary_defs(self):
        new_instr = []
        new_instr_ind = -1

        for index, instr in enumerate(self.block):
            if isinstance(instr, Instr) and instr.opcode == pyop.STORE_FAST:
                for dictionary in self.container_method.dictionary_defs:
                    if dictionary.name == instr.arg:
                        new_instr_ind = index
                        for index, item in enumerate(dictionary.keys):
                            # load the value
                            new_instr += self._ast_to_instr(dictionary.values[index], instr.lineno)
                            # load the dict
                            new_instr.append(Instr("LOAD_FAST", arg=instr.arg, lineno=instr.lineno))
                            # load the key
                            new_instr += self._ast_to_instr(dictionary.keys[index], instr.lineno)
                            new_instr.append(Instr("STORE_SUBSCR", lineno=instr.lineno))

                        self.container_method.dictionary_defs.remove(dictionary)

        if new_instr_ind > -1:
            self.updated_blocklist = self.updated_blocklist[0:new_instr_ind + 1] + new_instr + self.updated_blocklist[new_instr_ind + 1:]

    def _checkloops(self):
        if pyop.SETUP_LOOP in self.ops and pyop.GET_ITER in self.ops:

            counter = self.container_method.forloop_counter

            loopcounter_name = 'forloop_counter_%s' % counter
            looplength_name = 'forloop_length_%s' % counter

            iterable = self.block[1].arg
            iterable_name = self.block[-1].arg
            ln = self.block[0].lineno

            if iterable in ['range', 'keys', 'values'] or self.block[2].opcode in [pyop.LOAD_ATTR, pyop.LOAD_METHOD]:

                dynamic_iterable_name = 'dynamic_iterable_%s' % counter

                self.container_method.add_to_scope(dynamic_iterable_name)

                get_iter_index = self.ops.index(pyop.GET_ITER)
                load_range_ops = self.block[1:get_iter_index]
                load_range_ops.append(Instr("STORE_FAST", dynamic_iterable_name, lineno=ln))

                loop_exit = self.block[0].arg
                loop_done = self.block[get_iter_index + 2].arg
                loop_start = self.block[get_iter_index + 1]

                instructions = [
                    #                Instr("SETUP_LOOP",loop_exit,lineno=ln),

                    Instr("LOAD_CONST", 0, lineno=ln),
                    Instr("STORE_FAST", arg=loopcounter_name, lineno=ln)
                ] + load_range_ops + [
                    Instr("LOAD_FAST", arg=dynamic_iterable_name, lineno=ln),
                    Instr("LOAD_GLOBAL", arg="len", lineno=ln),
                    Instr("CALL_FUNCTION", arg=1, lineno=ln),
                    Instr("STORE_FAST", arg=looplength_name, lineno=ln),

                    loop_start,
                    #                Instr("FOR_ITER",loop_done,lineno=ln),
                    Instr("LOAD_FAST", arg=loopcounter_name, lineno=ln),
                    Instr("LOAD_FAST", arg=looplength_name, lineno=ln),
                    Instr("COMPARE_OP", arg=Compare.LT, lineno=ln),
                    Instr("POP_JUMP_IF_FALSE", arg=loop_done, lineno=ln),

                    Instr("LOAD_FAST", arg=dynamic_iterable_name, lineno=ln),
                    Instr("LOAD_FAST", arg=loopcounter_name, lineno=ln),
                    Instr("BINARY_SUBSCR", lineno=ln),
                    Instr("STORE_FAST", arg=iterable_name, lineno=ln),

                    Instr("LOAD_FAST", loopcounter_name, lineno=ln),
                    Instr("LOAD_CONST", 1, lineno=ln),
                    Instr("INPLACE_ADD", lineno=ln),
                    Instr("STORE_FAST", loopcounter_name, lineno=ln),

                ]

            else:
                loop_exit = self.block[0].arg
                loop_done = self.block[4].arg
                loop_start = self.block[3]

                instructions = [
                    #                Instr("SETUP_LOOP",loop_exit,lineno=ln),

                    Instr("LOAD_CONST", 0, lineno=ln),
                    Instr("STORE_FAST", arg=loopcounter_name, lineno=ln),
                    Instr("LOAD_FAST", arg=iterable, lineno=ln),
                    Instr("LOAD_GLOBAL", arg="len", lineno=ln),
                    Instr("CALL_FUNCTION", arg=1, lineno=ln),
                    Instr("STORE_FAST", arg=looplength_name, lineno=ln),

                    loop_start,
                    #                Instr("FOR_ITER",loop_done,lineno=ln),
                    Instr("LOAD_FAST", arg=loopcounter_name, lineno=ln),
                    Instr("LOAD_FAST", arg=looplength_name, lineno=ln),
                    Instr("COMPARE_OP", arg=Compare.LT, lineno=ln),
                    Instr("POP_JUMP_IF_FALSE", arg=loop_done, lineno=ln),

                    Instr("LOAD_FAST", arg=iterable, lineno=ln),
                    Instr("LOAD_FAST", arg=loopcounter_name, lineno=ln),
                    Instr("BINARY_SUBSCR", lineno=ln),
                    Instr("STORE_FAST", arg=iterable_name, lineno=ln),

                    Instr("LOAD_FAST", loopcounter_name, lineno=ln),
                    Instr("LOAD_CONST", 1, lineno=ln),
                    Instr("INPLACE_ADD", lineno=ln),
                    Instr("STORE_FAST", loopcounter_name, lineno=ln),

                ]

            self.container_method.add_to_scope(loopcounter_name)
            self.container_method.add_to_scope(looplength_name)
            self.container_method.add_to_scope(iterable_name)

            self.block = self.updated_blocklist = instructions

    def tokenize(self):

        self.updated_blocklist = self.block
        self._check_dictionary_defs()
        self._checkslice()
        self._checkbytearray()
        self._checkloops()
        self._check_load_attr()
        self._check_function_kwargs()
        self._reverselists()

        ln = None
        last_token = None
        for index, instr in enumerate(self.updated_blocklist):
            if isinstance(instr, Instr):
                ln = instr.lineno

            try:
                token = PyToken(instr, self, index, ln)
                token.to_vm(self.tokenizer, last_token)
            except Exception as e:
                cm = self.container_method
                print("ERROR: %s:%s in %s() with msg - %s" % (cm.module.path, cm.start_line_no + ln - 1, cm.name, str(e)))
                raise e
            last_token = token

    def lookup_method_name(self, index):
        return self.methodnames.pop()
