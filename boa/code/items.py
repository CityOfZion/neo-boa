from byteplay3 import Code, Opcode
from boa.code.method import Method
from boa.code import pyop
import importlib
import binascii


class Item():
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
    pass
#    def __init__(self, item_list):
#        super(Definition, self).__init__(item_list)
#        self.items[-1] = (Opcode(pyop.STORE_FAST),self.items[-1][1])
#       print("self items %s " % self.items)


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
        b_array = None
        if type(self.script_hash) is str:
            bstring = self.script_hash.encode('utf-8')
            b_array = bytearray(binascii.unhexlify(bstring))
        elif type(self.script_hash) is bytearray:
            pass
        elif type(self.script_hash) is bytes:
            b_array = bytearray(self.script_hash)
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

    def __init__(self, item_list):
        super(Import, self).__init__(item_list)
        self.module_items_to_import = []

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

    def __init__(self, item_list, module):
        super(Klass, self).__init__(item_list)
        self.module = self.parent = module
        self.methods = []
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

#        print('Created class %s inherits from %s ' % (self.name, self.parent))

        # go through code object of the class and extract the method code
        # objects
        for i, (op, arg) in enumerate(self.bp.code):

            if type(arg) is Code:
                self.methods.append(Method(arg, self))

    def is_valid(self):
        # here is where we check if the class extends something reasonable
        """

        :return:
        """
        return True
