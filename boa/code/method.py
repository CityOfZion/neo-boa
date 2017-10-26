from byteplay3 import SetLinenoType, Label, Opcode

from boa.code.pytoken import PyToken
from boa.code.vmtoken import VMTokenizer
from boa.code.block import Block
from boa.code import pyop

import dis

import collections


class Method():

    """

    The method is the main unit of functionality.  Any method can take 0 to many arguments and return 1 value

    Each method contains a variable amount of lines, or ``boa.code.block.Block`` objects, which represent
    discrete units of functionality.

    Each line in split into discrete ``boa.code.pytoken.PyToken`` objects, which are tokens which would be used
    by a python interpreter.

    After this, each line is turned into a block.  Once a block is complete, a variable amount of processing
    happens on the block to turn it into something that the Neo Virtual Machine will understand.

    Once we have a list of processed blocks, we can string them together and feed them to the VMTokenizer

    The VMTokenizer is responsible for turning PyToken objects into VMToken objects.

    When the method has been tokenized, each token then has an address within the method.  Once these addresses are complete,
    the ``convert_jumps`` method is called to tell each flow control operation where (which address) it will need to jump to.

    """
    bp = None

    parent = None

    tokens = None

    tokenizer = None

    local_stores = None

    start_line_no = None

    blocks = None

    method_address = None

    dynamic_iterator_count = 0

    local_methods = None

    __make_func_name = None

    @property
    def name(self):
        """
        get the name of this method

        :return: the name of this method
        :rtype: str

        """
        return self.bp.name

    @property
    def full_name(self):
        """
        gets the full name of this method ( with module path )

        :return: module namespaced name of the method
        :rtype: str

        """

        if self.__make_func_name is None:
            if len(self.module.module_path):
                return '%s.%s' % (self.module.module_path, self.name)
            return self.name
        return self.__make_func_name

    @property
    def args(self):
        """
        returns a list of arguments in this method

        :return: list of arguments for this method
        :rtype: list

        """
        return self.bp.args

    @property
    def code(self):
        """

        returns the ``byteplay3`` code object

        :return: the ``byteplay3`` code object of this method
        :rtype: ``byteplay3.Code``
        """
        return self.bp.code

    @property
    def vm_tokens(self):
        """
        returns a list of all vm tokens in this method

        :return: a list of vm tokens in this method
        :rtype: list

        """
        return self.tokenizer.vm_tokens

    @property
    def firstlineno(self):

        """
        gets the starting line number of this method

        :return: starting line number
        :rtype: int

        """

        return self.bp.firstlineno

    @property
    def total_lines(self):

        """
        get the total number of lines ( aka blocks ) in this method

        :return: total number of lines
        :rtype: int

        """

        count = 0
        for index, (op, arg) in enumerate(self.code):
            if type(op) is SetLinenoType:
                count += 1

        return count

    @property
    def total_module_variables(self):
        """
        get the total number of local variables

        :return: the number of variables in this module
        :rtype: int

        """
        return len(self.module.module_variables)

    @property
    def module(self):

        """

        retrieves the module this method is a member of

        :return: the module this method is a member of
        :rtype: ``boa.code.module.Module``

        """
        from boa.code.module import Module

        if type(self.parent) is Module:
            return self.parent
        elif type(self.parent.parent) is Module:
            return self.parent.parent
        elif type(self.parent.parent.parent) is Module:
            return self.parent.parent.parent
        return None

    def __init__(self, code_object, parent, make_func_name=None):

        self.bp = code_object

        self.parent = parent

        self.__make_func_name = make_func_name

        self.read_module_variables()

        self.read_initial_tokens()

        self.process_block_groups()

        self.tokenize()

        self.convert_jumps()


    def print(self):

        """

        this method prints the output of the method's ``byteplay3`` object as it would be seen by a python interpreter
        compare this with the ``boa.code.method.Method.to_dis()`` output and you will see subtle differences.

        sample output:

        >>> method.print()
              2            STORE_FAST           j
              12         1 LOAD_CONST           9
              14         4 LOAD_CONST           <byteplay3.Code object at 0x10cb5ec88>
                         5 LOAD_CONST           'Main.<locals>.q'
                         6 MAKE_FUNCTION        0
                         7 STORE_FAST           q
              22         9 LOAD_FAST            q
                        10 LOAD_FAST            j
                        11 CALL_FUNCTION        1
                        12 STORE_FAST           m
              24        14 LOAD_FAST            m
                        15 RETURN_VALUE

        """

        print(self.code)

    def to_dis(self):

        """

        this method prints the output of the method as it would be seen by a python interpreter.
        compare this to the output of the ``boa.code.method.Method.print()`` and you will see
        some subtle differences.

        >>> method.to_dis()
          3             STORE_FAST               0 (j)
         12           0 LOAD_CONST               1 (9)
         14           6 LOAD_CONST               2 (<code object q at 0x10cbbc810, file "./boa/tests/src/LambdaTest.py", line 14>)
                      9 LOAD_CONST               3 ('Main.<locals>.q')
                     12 MAKE_FUNCTION            0
                     15 STORE_FAST               1 (q)
         22          18 LOAD_FAST                1 (q)
                     21 LOAD_FAST                0 (j)
                     24 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                     27 STORE_FAST               2 (m)
         24          30 LOAD_FAST                2 (m)
                     33 RETURN_VALUE




        """

        out = self.bp.to_code()
        dis.dis(out)

    def read_module_variables(self):

        """

        this method takes all module ``global`` variables and gives this method access to them.

        """

        for definition in self.module.module_variables:

            items = definition.items

            self.bp.code = items + self.bp.code


    def read_initial_tokens(self):

        """

        this method taken the initial set of tokens from the ``byteplay3`` code object and turns them into blocks.

        """

        self.blocks = []

        self.local_methods = collections.OrderedDict()

        self.local_stores = collections.OrderedDict()

        current_line_no = None

        block_group = None

        self.tokenizer = VMTokenizer(self)

        current_label = None

        current_loop_token = None

        for i, (op, arg) in enumerate(self.code):

            # print("[%s] %s  ->  %s " % (i, op, arg))

            if type(op) is SetLinenoType:

                current_line_no = arg

                if self.start_line_no is None:
                    self.start_line_no = current_line_no

                if block_group is not None:

                    self.blocks.append(Block(block_group))

                block_group = []

            elif type(op) is Label:

                current_label = op

            else:

                if op in [pyop.STORE_FAST, pyop.STORE_NAME, pyop.STORE_GLOBAL] and arg not in self.local_stores.keys():
                    length = len(self.local_stores)
                    self.local_stores[arg] = length

                token = PyToken(op, current_line_no, i, arg)

                if op == pyop.SETUP_LOOP:
                    current_loop_token = token

                if op == pyop.BREAK_LOOP and current_loop_token is not None:
                    token.args = current_loop_token.args
                    current_loop_token = None

                if current_label is not None:
                    token.jump_label = current_label
                    current_label = None

                block_group.append(token)

        if len(block_group):
            self.blocks.append(Block(block_group))

    def process_block_groups(self):

        """

        this method takes the current blocks ( similar to lines in a method ) and
        processes them so they can be tokenized properly

        """

        iter_setup_block = None

        for index, block in enumerate(self.blocks):

            # if it is a return block
            # we need to insert a jmp at the start of the block
            # for the vm
            if block.is_return:

                # this jump needs to jump 3 bytes.  why? stay tuned to find out
                block_addr = b'\x03\x00'

                ret_token = PyToken(Opcode(pyop.BR_S),
                                    block.line, args=block_addr)
                ret_token.jump_label = block.oplist[0].jump_label
                block.oplist[0].jump_label = None
                block.oplist.insert(0, ret_token)
                block.mark_as_end()
#                length = len(self.local_stores)
#                self.local_stores[block.local_return_name] = length

            if block.has_load_attr:
                block.preprocess_load_attr(self)

            if block.is_list_comprehension:
                block.preprocess_list_comprehension(self)
                for localvar in block.list_comp_iterable_local_vars:
                    if localvar in self.local_stores.keys():
                        pass
                    else:
                        length = len(self.local_stores)
                        self.local_stores[localvar] = length

            if block.has_make_function:
                block.preprocess_make_function(self)
                self.local_methods[block.local_func_varname] = block.local_func_name


            if block.has_unprocessed_array:
                block.preprocess_arrays()

            if block.has_unprocessed_array_sub:
                block.preprocess_array_subs()

            if block.has_unprocessed_method_calls:
                block.preprocess_method_calls(self)

            if block.has_slice:
                block.preprocess_slice()
                if block.slice_item_length is not None:
                    length = len(self.local_stores)
                    self.local_stores[block.slice_item_length] = length

            if iter_setup_block is not None:
                block.process_iter_body(iter_setup_block)
                iter_setup_block = None

            if block.is_iter and not block.is_list_comprehension:
                block.preprocess_iter()
                for localvar in block.iterable_local_vars:

                    if localvar in self.local_stores.keys():
                        pass
                    else:
                        length = len(self.local_stores)
                        self.local_stores[localvar] = length
                iter_setup_block = block
                self.dynamic_iterator_count += 1

        alltokens = []

        for block in self.blocks:
            if block.has_make_function:
                if block.is_list_comprehension:
                    alltokens = alltokens + block.oplist
            else:
                alltokens = alltokens + block.oplist
        self.tokens = alltokens

        for index, token in enumerate(self.tokens):
            token.addr = index

    def tokenize(self):

        """

        this method turns a set of ``boa.code.pytoken.PyToken`` objects into ``boa.code.vmtoken.VMToken`` objects

        """

        self.tokenizer.update_method_begin_items()
        prevtoken = None
        for t in self.tokens:
            t.to_vm(self.tokenizer, prevtoken)
            prevtoken = t

    def convert_jumps(self):

        """

        this method converts jumps that occur from flow control items such as if, else, for loops, while loops, and breaks

        """

        for key, vm_token in self.tokenizer.vm_tokens.items():

            if vm_token.pytoken and type(vm_token.pytoken.args) is Label:

                label = vm_token.pytoken.args

                for key2, vm_token_target in self.tokenizer.vm_tokens.items():

                    if vm_token_target.pytoken and vm_token_target.pytoken.jump_label is not None:

                        jump_to_label = vm_token_target.pytoken.jump_label

                        if jump_to_label == label:

                            difference = vm_token_target.addr - vm_token.addr

                            vm_token.data = difference.to_bytes(2, 'little', signed=True)

    def write(self):

        """
        this method writes the current state of the tokenizer to a byte string

        :return: a byte string of the current tokenizer
        :rtype: bytes

        """

        out = self.tokenizer.to_b()
        return out
