from byteplay3 import Opcode
from boa.code.pytoken import PyToken

import importlib
import binascii
import sys
import os

from byteplay3 import Code, SetLinenoType
from boa.code import pyop

from boa.code.line import Line
from boa.code.method import Method


class Item(object):
    """

    """
    items = None

    def __init__(self, item_list):
        self.items = item_list

    def is_valid(self):
        """

        :return:
        """
        return True


class Definition(Item):

    value = None
    attr = None

    operations = None
    block = None

    is_method_call = False
    fn_call = None

    def __init__(self, item_list):
        super(Definition, self).__init__(item_list)

        # this is a simple definition like a = 3
        if len(self.items) == 3:
            self.value = PyToken(self.items[1], 1, args=self.items[1][1])
            self.attr = PyToken(self.items[2], 1, args=self.items[2][1])
        # a method based definition linke ctx = GetContext
        elif len(self.items) == 4:
            self.is_method_call = True
            self.attr = PyToken(self.items[-1], 1, args=self.items[-1][1])
            self.value = PyToken(Opcode(pyop.LOAD_CONST), 1, args=7)
            self.convert_class_call_to_block()

        elif len(self.items) == 5:
            if self.items[-1][0] == pyop.RETURN_VALUE:
                self.items = self.items[:3]
                self.value = PyToken(self.items[1], 1, args=self.items[1][1])
                self.attr = PyToken(self.items[2], 1, args=self.items[2][1])

        else:

            #            self.is_method_call=True
            self.attr = PyToken(self.items[-1], 1, args=self.items[-1][1])
#            print("SOMETHING ELSE!")
#            pdb.set_trace()

    def convert_class_call_to_block(self):

        from boa.code.block import Block

        opitems = self.items[1:]
        current_line_num = 1
        blockitems = []
        for i, (op, arg) in enumerate(opitems):

            token = PyToken(op, current_line_num, i, arg)
            blockitems.append(token)

        self.block = Block(blockitems)
        self.block.preprocess_method_calls(None)
        self.fn_call = self.block.oplist[0]


class Action(Item):

    """

    """
    event_name = None
    event_args = None

    method_name = None

    def __init__(self, item_list):
        super(Action, self).__init__(item_list)

        arguments = []

        for i, (key, value) in enumerate(self.items.items):
            if key == pyop.LOAD_CONST:
                arguments.append(value)
            elif key == pyop.STORE_NAME:
                self.method_name = value

        self.event_name = arguments[0]

        self.event_args = arguments


class SmartContractAppCall(Item):

    """

    """
    script_hash = None
    script_args = None

    method_name = None

    def __init__(self, item_list):
        super(SmartContractAppCall, self).__init__(item_list)

        arguments = []

        for i, (key, value) in enumerate(self.items.items):
            if key == pyop.LOAD_CONST:
                arguments.append(value)
            elif key == pyop.STORE_NAME:
                self.method_name = value

        self.script_hash = arguments[0]

        self.script_args = arguments

        if type(self.script_hash) is str:
            if len(self.script_hash) != 40:
                raise Exception(
                    "Invalid script hash! length of string must be 40")
        elif type(self.script_hash) in [bytes, bytearray]:
            if len(self.script_hash) != 20:
                raise Exception(
                    "Invalid Script hash, length in bytes must be 20")
        else:
            raise Exception(
                "Invalid script hash type.  must be string, bytes, or bytearray")

    @property
    def script_hash_addr(self):
        """

        :return:
        """

        return SmartContractAppCall.to_script_hash_data(self.script_hash)

    @staticmethod
    def to_script_hash_data(item):
        """

        :return:
        """
        b_array = None
        if type(item) is str:
            bstring = item.encode('utf-8')
            b_array = bytearray(binascii.unhexlify(bstring))
        elif type(item) is bytearray:
            pass
        elif type(item) is bytes:
            b_array = bytearray(item)
        else:
            raise Exception("Invalid script hash")

        b_array.reverse()

        return bytes(b_array)


class Import(Item):

    """

    """
    NEO_SC_FRAMEWORK = 'neo.SmartContract.Framework.'

    module_path = None
    module_name = None

    imported_module = None

    is_system_module = None

    module_items_to_import = None

    file_path = None

    def __init__(self, item_list, current_file_path):
        super(Import, self).__init__(item_list)
        self.module_items_to_import = []

        self.file_path = os.path.dirname(os.path.abspath(current_file_path))

        sys.path.append(self.file_path)

        for i, (op, arg) in enumerate(self.items):
            if op == pyop.IMPORT_NAME:
                self.module_path = arg
            elif op == pyop.STORE_NAME:
                self.module_items_to_import.append(arg)
#                print("SETTING MODALu nAme: %s " % self.module_name)

            elif op == pyop.IMPORT_STAR:
                self.module_items_to_import = ['STAR']

        self.is_system_module = False

        self.build()

    def build(self):
        # here is where we will check imports
        """

        """
        from boa.code.module import Module

        module = importlib.import_module(self.module_path, self.module_path)

        filename = module.__file__

        if self.NEO_SC_FRAMEWORK in self.module_path:
            self.is_system_module = True

        self.imported_module = Module(filename,
                                      module_name=self.module_path,
                                      is_sys_module=self.is_system_module,
                                      items_to_import=self.module_items_to_import)

    def is_valid(self):
        """

        :return:
        """
        return True

    def __str__(self):
        return "%s.%s" % (self.module_path, self.module_name)


class Klass(Item):

    """

    """
    name = None

    parent_name = None

    parent = None

    methods = None

    bp = None

    module = None

    lines = None

    class_vars = None
    class_method_calls = None

    @property
    def total_fields(self):
        return len(self.class_vars)

    @property
    def class_var_names(self):
        names = []
        for var in self.class_vars:
            names.append(var.attr.args)
        return names

    def index_of_varname(self, name):
        names = self.class_var_names
        return names.index(name)

    @property
    def all_method_names(self):
        return [m.full_name for m in self.methods]

    def __init__(self, item_list, module):
        super(Klass, self).__init__(item_list)
        self.module = self.parent = module
        self.methods = []
        self.lines = []
        self.class_vars = []
        self.class_method_calls = []
        self.build()

    def build(self):
        """

        """

        for i, (op, arg) in enumerate(self.items):

            # if the item is a byteplay3 code object, it is a method
            if type(arg) is Code:
                self.bp = arg

            # load name is called  to gather the class parent
            if op == pyop.LOAD_NAME:
                self.parent_name = arg

            # this occurs to store the name of the class
            if op == pyop.STORE_NAME:
                self.name = arg

        self.split_lines()

        for lineset in self.lines:

            if lineset.is_docstring:
                pass
            elif lineset.is_constant:
                self.class_vars.append(Definition(lineset.items))
            elif lineset.is_module_method_call:
                self.class_vars.append(Definition(lineset.items))

            elif lineset.is_method:

                m = Method(lineset.code_object, self)

                self.methods.append(m)

    def is_valid(self):
        # here is where we check if the class extends something reasonable
        """

        :return:
        """
        return True

    def split_lines(self):
        """
        Split the list of lines in the module into a set of objects that can be interpreted.
        """

        lineitem = None

        for i, (op, arg) in enumerate(self.bp.code):

            if isinstance(op, SetLinenoType):
                if lineitem is not None:
                    self.lines.append(Line(lineitem))

                lineitem = []

            lineitem.append((op, arg))

        if len(lineitem):
            self.lines.append(Line(lineitem))

    def __str__(self):
        return self.name
