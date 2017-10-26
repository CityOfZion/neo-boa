from byteplay3 import Code, SetLinenoType, Label
from boa.code import pyop

from boa.code.line import Line
from boa.code.method import Method
from boa.code.items import Definition, Klass, Import, Action, SmartContractAppCall

from boa.blockchain.vm import VMOp

from collections import OrderedDict

import pdb


class Module():
    """
    A Module is the top level component which contains code objects.
    When, for example, compiling ``path/to/my/file.py``, the items contained in ``file.py`` are the module.
    An executable may have many modules.  The 'default' or 'entry' module in the example above would be ``file.py``

    When calling ``Compiler.load_and_save('path/to/file.py')``, a module is created for ``file.py``.
    If `file.py` imports any other functionality, those modules will also be added to the executable
    and placed in the Module.loaded_modules attribute.

    After modules have been processed as methods, and then methods processed as blocks, and blocks processed to tokens,
    The main or ``default`` module's ``write()`` method is called, which writes the executable to a byte string and returns
    it to be saved to disk.

    If you would like to inspect the contents of a module, you may use the ``Compiler.load('path/to/file.py')`` which will
    return an instance of the compiler.  With that instance, you can access the ``default`` module of the compiler
    which will in turn give you access to any other loaded modules contained in the default module.


    Each module ( as well as each method object ) contains a reference to a ``byteplay3`` object, named ``bp``.
    This object contains the instruction set as it would be viewed in the Python interpreter.

    You can call ``print(module.bp.code)`` on any object with a ``bp`` attribute, and it will output the Python interpreter code.


    >>> from boa.compiler import Compiler
    >>> module = Compiler.load('./boa/tests/src/AddTest1.py').default
    >>> print(module.bp.code)
    2     1 LOAD_CONST           <byteplay3.Code object at 0x10cc3d6a0>
          2 LOAD_CONST           'Main'
          3 MAKE_FUNCTION        0
          4 STORE_NAME           Main
          5 LOAD_CONST           None
          6 RETURN_VALUE


    Once an executable has been processed and tokenized, it will then have a set of vm tokens that are similar
    to the ``byteplay3`` tokens, but different in important ways. These are contained in the module's ``all_vm_tokens`` attribute

    You may call ``module.to_s()`` to view the program as it has been tokenized for the NEO Virtual Machine.


    >>> module.to_s()
    4             31  LOAD_FAST           a                [data]
                  36  LOAD_CONST          2                [data]
                  37  BINARY_MULTIPLY                      [data]
                  38  STORE_FAST          a2               [data]
    6             45  LOAD_FAST           b                [data]
                  50  LOAD_CONST          1                [data]
                  51  BINARY_ADD                           [data]
                  52  STORE_FAST          b2               [data]
    8             59  LOAD_FAST           c                [data]
                  64  LOAD_CONST          2                [data]
                  65  BINARY_TRUE_DIVIDE                   [data]
                  66  STORE_FAST          c2               [data]
    10            73  LOAD_FAST           d                [data]
                  78  LOAD_CONST          1                [data]
                  79  BINARY_SUBTRACT                      [data]
                  80  STORE_FAST          d2               [data]
    13            87  243                 b'\x03\x00'      [data] 3
                  90  LOAD_FAST           a2               [data]
                  95  LOAD_FAST           b2               [data]
                  100 BINARY_ADD                           [data]
                  101 LOAD_FAST           c2               [data]
                  106 BINARY_ADD                           [data]
                  107 LOAD_FAST           d2               [data]
                  112 BINARY_ADD                           [data]
                  113 NOP                                  [data]
                  114 241                                  [data]
                  115 242                                  [data]
                  116 RETURN_VALUE                         [data]
    """
    
    bp = None  # this is to store the byteplay reference

    path = None  # the path where this file is

    lines = None  # this contains the code objects split up into different line start indexes

    imports = None  # a list of import statements

    module_variables = None  # list of module variables

    classes = None  # a list of classes

    methods = None  # a list to keep all methods in the module

    actions = None  # a list to keep track of event registrations

    app_call_registrations = None  # a list to keep track of app call registrations

    is_sys_module = None

    all_vm_tokens = None # dict for converting method tokens into linked method tokens for writing

    loaded_modules = None

    _module_name = None

    _names_to_load = None


    @property
    def module_path(self):
        """
        Return the file path of the module.

        :return: the path of the module
        :rtype: str
        """
        
        return self._module_name
        

    @property
    def main(self):
        """
        Return the default method in this module.

        :return: the default method in this module
        :rtype: ``boa.code.method.Method``
        """
        
        for m in self.methods:
            
            if m.name == 'Main':
                return m
                
        if len(self.methods):
            return self.methods[0]
            
        return None
        

    @property
    def orderered_methods(self):
        """
        An ordered list of methods

        :return: A list of ordered methods is this module
        :rtype: list
        """
        
        oms = []
        
        self.methods.reverse()
        
        if self.main:
            oms = [self.main]

        for m in self.methods:
            
            if m == self.main:
                continue
            oms.append(m)

        return oms


    def add_method(self, method):
        """
        Adds a method to this module

        :param method: the method object to add to this module
        :type method: ``boa.code.method.Method``

        :return: whether the method was added
        :rtype: bool
        """
        
        for m in self.methods:
            
            if m.name == method.name:
    
                if m.name != m.full_name:
                    
                    if m.full_name == method.full_name:
                        return False
                else:
                    return False
                # return False

        # print("appending method %s %s " % (method.name, method.full_name))
        self.methods.append(method)
        
        return True


    def method_by_name(self, method_name):
        """
        Look up a method by its name from the module ``methods`` list.
        :param method_name: the name of the method to look up
        :type method_name: str

        :return: the method ( if it is found)
        :rtype: ``boa.code.method.Method``
        """
        
        for m in self.methods:
            if m.full_name == method_name:
                return m
            elif m.name == method_name:
                return m
        return None
        

    def __init__(self, path, module_name='', is_sys_module=False, items_to_import=None):

        self.path = path

        self._module_name = module_name

        self.is_sys_module = is_sys_module
        
        self._names_to_load = ['STAR'] if items_to_import is None else items_to_import

        source = open(path, 'rb')

        suite = compile(source.read(), path, 'exec')

        self.bp = Code.from_code(suite)

        source.close()

        self.build()
        

    def build(self):
        """
        Split the ``bp.code`` object into lines, and assembles the lines into different items.
        """
        
        self.lines = []
        self.imports = []
        self.module_variables = []
        self.methods = []
        self.actions = []
        self.app_call_registrations = []
        self.classes = []
        self.loaded_modules = []

        self.split_lines()

        for lineset in self.lines:

            if lineset.is_import:

                if not self.is_sys_module:
                    imp = Import(lineset.items)
                    self.process_import(imp)
                else:
                    print("will not import items from sys module")

            elif lineset.is_docstring:
                pass
            elif lineset.is_definition:
                self.module_variables.append(Definition(lineset.items))
            elif lineset.is_class:
                self.classes.append(Klass(lineset.items, self))
            elif lineset.is_method:
                self.process_method(lineset)
            elif lineset.is_action_registration:
                self.process_action(lineset)
            elif lineset.is_smart_contract_appcall_registration:
                self.process_smart_contract_app_registration(lineset)
            else:
                print('not sure what to do with line %s ' % lineset)
                pdb.set_trace()


    def process_import(self, import_item):
        """
        Processes an import statement within this module.

        :param import_item:
        :type import_item: ``boa.code.items.Import subclass``
        """
        
        self.imports.append(import_item)

        self.loaded_modules.append(import_item.imported_module)

        # Go through all the methods in the imported module.
        for method in import_item.imported_module.methods:
            self.add_method(method)


    def process_method(self, lineset):
        """
        processes a set of lines that contain a byteplay3 code object

        :param lineset: the lineset to process and add
        :type lineset: list
        """
        
        m = Method(lineset.code_object, self)

        if 'STAR' in self._names_to_load:
            self.add_method(m)
        else:
            for item in self._names_to_load:
                
                if item == m.name:
                    self.add_method(m)

    def process_action(self, lineset):
        """
        Processes an action within this module.
        A sample action would be to create an event like so:

        .. code-block:: python

            from boa.blockchain.vm.Neo.Action import RegisterAction

            # Register the action.
            onRefund = RegisterAction('refund', 'to_address', 'amount')

            # Dispatch an action.
            onRefund(my_address, 100)

        :param lineset: The set of lines containing an app call registration
        :type lineset: list
        """
        
        action = Action(lineset)
        for act in self.actions:
            if act.method_name == action.method_name:
                return None
                
        self.actions.append(action)


    def process_smart_contract_app_registration(self, lineset):
        """
        processes a smart contract app registration, for when you would like to call another
        smart contract from your contract.  for example:

        .. code-block:: python

            from boa.blockchain.vm.Neo.App import RegisterAppCall

            # register the contract
            otherContract = RegisterAppCall('contract_hash', 'param1','param2')

            # call the contract
            result = otherContract( a, b )

        :param lineset: The set of lines containing an app call registration
        :type lineset: list
        """
        
        appcall_registration = SmartContractAppCall(lineset)
        for registration in self.app_call_registrations:
            if registration.method_name == appcall_registration.method_name:
                return
        self.app_call_registrations.append(appcall_registration)


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


    def write(self):
        """
        Write the current module to a byte string.

        Note that if you are using the ``Compiler.load('path/to/file.py')``, you must 
        call ``module.write()`` before any inspection of the module is possible.

        :return: A bytestring of representing the current module
        :rtype: bytes
        """
        self.link_methods()

        return self.write_methods()


    def write_methods(self):
        """
        Write all methods in the current module to a byte string.

        :return: A bytestring of all current methods in this module
        :rtype: bytes
        """

        b_array = bytearray()
        for key, vm_token in self.all_vm_tokens.items():

            b_array.append(vm_token.out_op)

            if vm_token.data is not None and vm_token.vm_op != VMOp.NOP:
                b_array = b_array + vm_token.data

        return b_array
        

    def link_methods(self):
        """
        Perform linkage of addresses between methods.
        """

        self.all_vm_tokens = OrderedDict()

        address = 0

        for method in self.orderered_methods:
            method.method_address = address

            for key, vmtoken in method.vm_tokens.items():
                self.all_vm_tokens[address] = vmtoken

                address += 1

                if vmtoken.data is not None:
                    address += len(vmtoken.data)

                vmtoken.addr = vmtoken.addr + method.method_address

        for key, vmtoken in self.all_vm_tokens.items():
            if vmtoken.src_method is not None:

                target_method = self.method_by_name(vmtoken.target_method)
                if target_method:

                    jump_len = target_method.method_address - vmtoken.addr
                    vmtoken.data = jump_len.to_bytes(2, 'little', signed=True)
                else:
                    raise Exception("Target method %s not found" % vmtoken.target_method)


    def to_s(self):
        """
        this method is used to print the output of the executable in a readable/ tokenized format.
        sample usage:

        >>> from boa.compiler import Compiler
        >>> module = Compiler.load('./boa/tests/src/LambdaTest.py').default
        >>> module.write()
        >>> module.to_s()
        12            3   LOAD_CONST          9                [data]
                      4   STORE_FAST          j                [data]
        22            11  LOAD_FAST           j                [data]
                      17  CALL_FUNCTION       Main.<locals>.q_1 \
					  [<boa.code.pytoken.PyToken object at 0x10cb53c50>] [data] 22
                      20  STORE_FAST          m                [data]
        24            27  243                 b'\x03\x00'      [data] 3
                      30  LOAD_FAST           m                [data]
                      35  NOP                                  [data]
                      36  241                                  [data]
                      37  242                                  [data]
                      38  RETURN_VALUE                         [data]
        20            49  243                 b'\x03\x00'      [data] 3
                      52  LOAD_FAST           x                [data]
                      57  LOAD_CONST          1                [data]
                      58  BINARY_ADD                           [data]
                      59  NOP                                  [data]
                      60  241                                  [data]
                      61  242                                  [data]
                      62  RETURN_VALUE                         [data]
        """

        lineno = 0
        pstart = True
        
        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            if value.pytoken:
                pt = value.pytoken
                do_print_line_no = False
                to_label = None
                from_label = '    '
                
                if pt.line_no != lineno:
                    print("\n")
                    lineno = pt.line_no
                    do_print_line_no = True

                if pt.args and type(pt.args) is Label:
                    addr = value.addr
                    if value.data is not None:
                        plus_addr = int.from_bytes(
                            value.data, 'little', signed=True)
                        target_addr = addr + plus_addr
                        to_label = 'to %s    [ %s ]' % (target_addr, pt.args)
                    else:
                        to_label = 'from << %s ' % pt.args
                        #                    to_label = 'to %s ' % pt.args
                elif pt.jump_label:
                    from_label = ' >> '
                    to_label = 'from [%s]' % pt.jump_label

                ds = ''
                if value.data is not None:
                    try:
                        ds = int.from_bytes(value.data, 'little', signed=True)
                    except Exception as e:
                        pass
                    if type(ds) is not int and len(ds) < 1:
                        try:
                            ds = value.data.decode('utf-8')
                        except Exception as e:
                            pass

                if pt.py_op == pyop.CALL_FUNCTION:
                    to_label = '%s %s ' % (pt.func_name, pt.func_params)

                lno = "{:<10}".format(
                    pt.line_no if do_print_line_no or pstart else '')
                addr = "{:<4}".format(key)
                op = "{:<20}".format(str(pt.py_op))
                arg = "{:<50}".format(
                    to_label if to_label is not None else pt.arg_s)
                data = "[data] {:<20}".format(ds)
                print("%s%s%s%s%s%s" % (lno, from_label, addr, op, arg, data))

            pstart = False
