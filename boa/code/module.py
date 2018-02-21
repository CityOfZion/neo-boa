from boa.code import pyop
from boa.code.method import method as BoaMethod
from boa.util import print_block,BlockType,get_block_type
from bytecode import UNSET, Bytecode, BasicBlock,ControlFlowGraph, dump_bytecode,Label
from boa.interop import VMOp
import importlib
from logzero import logger
from collections import OrderedDict


class Module(object):

    bc = None
    cfg = None

    blocks = None

    methods = None

    path = None

    all_vm_tokens = OrderedDict()

    cwd = None
    module_name = ''

    to_import = None

    @staticmethod
    def ImportFromBlock(block:BasicBlock, current_path):
        mpath = None
        mnames = []
        for index, instr in enumerate(block):
            if instr.opcode == pyop.IMPORT_NAME:
                mpath = instr.arg
            elif instr.opcode in [pyop.IMPORT_FROM, pyop.STORE_NAME]:
                if not instr.arg in mnames:
                    mnames.append(instr.arg)
            elif instr.opcode == pyop.IMPORT_STAR:
                mnames = ['*']

#        if 'boa.interop' in mpath:
#            return None
        try:
            pymodule = importlib.import_module(mpath, mpath)
            filename = pymodule.__file__
            return Module(filename,current_path,mpath,mnames)
        except Exception as e:
            print("Could not import: %s " % e)
        return None

    @property
    def actions(self):
        return []
    @property
    def app_call_registrations(self):
        return []

    @property
    def main(self):
        """
        Return the default method in this module.

        :return: the default method in this module
        :rtype: ``boa.code.method.Method``
        """

        for m in self.methods:

            if m.name in ['Main','main']:
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

    def method_by_name(self, method_name):
        """
        Look up a method by its name from the module ``methods`` list.
        :param method_name: the name of the method to look up
        :type method_name: str

        :return: the method ( if it is found)
        :rtype: ``boa.code.method.Method``
        """

        #        print("METHODS FOR MODULE: %s " % self.path)
        for m in self.methods:
            if m.full_name == method_name:
                return m
            elif m.name == method_name:
                return m
        return None


    def __init__(self, path:str, working_dir, module_name='', to_import=['*']):

        self.path = path
        self.cwd = working_dir
        self.to_import = to_import
        self.module_name = module_name

        source = open(path, 'rb')

        compiled_source = compile(source.read(), path, 'exec')

        self.bc = Bytecode.from_code(compiled_source)
        self.cfg = ControlFlowGraph.from_bytecode(self.bc)

        source.close()

        self.build()


    def build(self):
        self.blocks = []
        self.methods = []

        for block in self.cfg:
            start_ln = block[0].lineno
            for index,instr in enumerate(block):
                if instr.lineno != start_ln:
                    self.cfg.split_block(block,index)

        extra_instr = []
        new_method_blks=[]
        for blk in self.cfg:
            type = get_block_type(blk)
            if type == BlockType.MAKE_FUNCTION:
                new_method_blks.append(blk)
            elif type == BlockType.IMPORT_ITEM:
                new_module = Module.ImportFromBlock(blk, self.cwd)
                if new_module:
                    for method in new_module.methods:
                        self.methods.append(method)
            elif type == BlockType.UNKNOWN:
                extra_instr.append(blk)
            elif type == BlockType.CALL_FUNCTION:
                extra_instr.append(blk)
            else:
                logger.info("Block type not used:: %s " % type)

        for m in new_method_blks:
            new_method = BoaMethod(self, m, self.module_name,extra_instr)
            if self.to_import == ['*'] or new_method.name in self.to_import:
                self.methods.append(new_method)

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

#        self.to_s()
        return b_array

    def link_methods(self):
        """
        Perform linkage of addresses between methods.
        """

        for method in self.methods:
#            method.link_return_types()
            method.prepare()

        self.all_vm_tokens = OrderedDict()

        address = 0

        for method in self.orderered_methods:

            if not method.is_interop:
                method.address = address

                for key, vmtoken in method.vm_tokens.items():
                    self.all_vm_tokens[address] = vmtoken
                    address += 1

                    if vmtoken.data is not None:
                        address += len(vmtoken.data)

                    vmtoken.addr = vmtoken.addr + method.address

        for key, vmtoken in self.all_vm_tokens.items():
            if vmtoken.src_method is not None:

                target_method = self.method_by_name(vmtoken.target_method)
                if target_method:
                    jump_len = target_method.address - vmtoken.addr
                    vmtoken.data = jump_len.to_bytes(2, 'little', signed=True)
                else:

                    #                    pdb.set_trace()
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
        # Initialize if needed
        if self.all_vm_tokens is None:
            self.link_methods()

        lineno = 0
        pstart = True

        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            if value.pytoken:
                pt = value.pytoken
                do_print_line_no = False
                to_label = None
                from_label = '    '

                if pt.lineno != lineno:
                    print("\n")
                    lineno = pt.lineno
                    do_print_line_no = True

                if pt.args and type(pt.args) is BasicBlock:
                    addr = value.addr
                    if value.data is not None:
                        plus_addr = int.from_bytes(
                            value.data, 'little', signed=True)
                        target_addr = addr + plus_addr
                        to_label = 'to %s    [ %s ]' % (target_addr, pt.arg_str)
                    else:
                        to_label = 'from << %s ' % pt.arg_str
                        #                    to_label = 'to %s ' % pt.args
#                elif pt.jump_label:
#                    from_label = ' >> '
#                    to_label = 'from [%s]' % pt.jump_label

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

                if pt.pyop == pyop.CALL_FUNCTION:
                    if to_label is None:
                        old = ""
                    else:
                        old = to_label
#                    param_string = "("
#                    for param in pt.func_params:
#                        param_string += str(param.args) + ", "
#                    param_string = param_string.rstrip(", ") + ")"
#                    to_label = '%s %s %s' % (pt.func_name, param_string, old)

                lno = "{:<10}".format(
                    pt.lineno if do_print_line_no or pstart else '')
                addr = "{:<5}".format(key)
                op = "{:<20}".format(pt.instruction.name)

                # If this is a number, it is likely a custom python opcode, get the name
                if str(pt.pyop).isnumeric():
                    opname = pyop.to_name(int(str(pt.pyop))).replace('HAVE_ARGUMENT','STORE_NAME')
                    if opname is not None:
                        op = "{:<20}".format(opname)

                arg = "{:<50}".format(pt.arg_str)
                data = "[data] {:<20}".format(ds)
                print("%s%s%s%s%s%s" % (lno, from_label, addr, op, arg, data))

            pstart = False

