from boa.code import pyop
from boa.code.method import method as BoaMethod
from boa.code.action import action as BoaAction
from boa.code.appcall import appcall as BoaAppcall

from boa.util import BlockType, get_block_type
from bytecode import UNSET, Bytecode, BasicBlock, ControlFlowGraph, dump_bytecode, Label
from boa.interop import VMOp
import importlib
from logzero import logger
from collections import OrderedDict
import os
import sys
import hashlib
import zipfile 
from boa import __version__
import json


class Module(object):

    bc = None
    cfg = None

    blocks = None

    methods = None
    actions = None
    app_call_registrations = None

    path = None

    all_vm_tokens = OrderedDict()

    module_name = ''

    to_import = None

    _extra_instr = None

    _local_methods = None

    abi_methods = {}
    abi_entry_point = None

    @property
    def extra_instructions(self):
        return self._extra_instr

    @property
    def local_methods(self):
        return self._local_methods

    @staticmethod
    def ImportFromBlock(block: BasicBlock, current_file_path):

        mpath = None
        mnames = []

        filepath = os.path.dirname(os.path.abspath(current_file_path))

        sys.path.append(filepath)

        for index, instr in enumerate(block):
            if instr.opcode == pyop.IMPORT_NAME:
                mpath = instr.arg
            elif instr.opcode == pyop.STORE_NAME:
                if instr.arg not in mnames:
                    mnames.append(instr.arg)
            elif instr.opcode == pyop.IMPORT_STAR:
                mnames = ['*']

        # Don't load the abi module when imported
        if 'boa.abi' in mpath:
            return

        pymodule = importlib.import_module(mpath, mpath)
        filename = pymodule.__file__
        return Module(filename, mpath, mnames)

    @property
    def main(self):
        """
        Return the default method in this module.

        :return: the default method in this module
        :rtype: ``boa.code.method.Method``
        """

        for m in self.methods:

            if m.name in ['Main', 'main']:
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
            if m.full_name == method_name or m.name == method_name:
                return m

        return None

    def has_method(self, full_name):
        for m in self.methods:
            if m.full_name == full_name:
                return True
        return False

    def __init__(self, path: str, module_name='', to_import=['*']):

        self.path = path
        self.to_import = to_import
        self.module_name = module_name
        self._local_methods = []
        self.abi_methods = {}
        self.abi_entry_point = None
        source = open(path, 'rb')

        compiled_source = compile(source.read(), path, 'exec')

        self.bc = Bytecode.from_code(compiled_source)
        self.cfg = ControlFlowGraph.from_bytecode(self.bc)

        source.close()

        self.build()

    def build(self):
        self.blocks = []
        self.methods = []
        self.actions = []
        self.app_call_registrations = []

        for block in self.cfg:
            start_ln = block[0].lineno
            for index, instr in enumerate(block):
                if instr.lineno != start_ln:
                    self.cfg.split_block(block, index)

        self._extra_instr = []
        new_method_blks = []
        for blk in self.cfg:
            type = get_block_type(blk)
            if type == BlockType.MAKE_FUNCTION:
                new_method_blks.append(blk)
            elif type == BlockType.IMPORT_ITEM:
                new_module = Module.ImportFromBlock(blk, self.path)
                if new_module:
                    for method in new_module.methods:
                        if not self.has_method(method.full_name):
                            self.methods.append(method)
                    for method in new_module.local_methods:
                        self.methods.append(method)
                    self._extra_instr = self._extra_instr + new_module.extra_instructions
            elif type == BlockType.UNKNOWN:
                self._extra_instr.append(blk)
            elif type == BlockType.CALL_FUNCTION:
                self._extra_instr.append(blk)
            elif type == BlockType.ACTION_REG:
                self.actions.append(BoaAction(blk))
            elif type == BlockType.MAKE_CLASS:
                pass
            elif type == BlockType.APPCALL_REG:
                self.app_call_registrations.append(BoaAppcall(blk))

        for m in new_method_blks:

            new_method = BoaMethod(self, m, self.module_name, self._extra_instr)

            if not self.has_method(new_method.full_name):
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

        from ..compiler import Compiler

        for method in self.methods:
            method.prepare()

        self.all_vm_tokens = OrderedDict()

        address = 0

        for method in self.orderered_methods:

            if not method.is_interop and not method.is_abi_decorator:
                #                print("ADDING METHOD %s " % method.full_name)
                method.address = address

                for key, vmtoken in method.vm_tokens.items():
                    self.all_vm_tokens[address] = vmtoken
                    address += 1

                    if vmtoken.data is not None and vmtoken.vm_op != VMOp.NOP:
                        address += len(vmtoken.data)

                    vmtoken.addr = vmtoken.addr + method.address

        for key, vmtoken in self.all_vm_tokens.items():
            if vmtoken.src_method is not None:

                target_method = self.method_by_name(vmtoken.target_method)
                if target_method:
                    jump_len = target_method.address - vmtoken.addr

                    param_ret_counts = bytearray()
                    if Compiler.instance().nep8:
                        param_ret_counts = vmtoken.data[0:2]
                        jump_len -= 2

                    if jump_len > -32767 and jump_len < 32767:
                        vmtoken.data = param_ret_counts + jump_len.to_bytes(2, 'little', signed=True)
                    else:
                        vmtoken.data = param_ret_counts + jump_len.to_bytes(4, 'little', signed=True)
                else:
                    raise Exception("Target method %s not found" % vmtoken.target_method)

        # abi methods decorator is used, but there is no abi entry point decorator
        if len(self.abi_methods) > 0 and self.abi_entry_point is None:
            raise Exception("ABI entry point not found")

    def to_s(self):
        """
        this method is used to print the output of the executable in a readable/ tokenized format.
        sample usage:

        >>> from boa.compiler import Compiler
        >>> module = Compiler.load('./boa/tests/src/LambdaTest.py').default
        >>> module.write()
        >>> print(module.to_s())
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
        output = []
        pstart = True

        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            if value.pytoken:
                pt = value.pytoken
                do_print_line_no = False
                to_label = None
                from_label = '    '

                if pt.lineno != lineno:
                    output.append("\n")
                    lineno = pt.lineno
                    do_print_line_no = True

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

                lno = "{:<10}".format(
                    pt.lineno if do_print_line_no or pstart else '')
                addr = "{:<5}".format(key)
                op = "{:<20}".format(pt.instruction.name)

                # If this is a number, it is likely a custom python opcode, get the name
                if str(pt.pyop).isnumeric():
                    opname = pyop.to_name(int(str(pt.pyop))).replace('HAVE_ARGUMENT', 'STORE_NAME').replace('YIELD_VALUE', 'REVERSE')
                    if opname is not None:
                        op = "{:<20}".format(opname)

                arg = "{:<50}".format(pt.arg_str)
                data = "[data] {:<20}".format(ds)
                output.append("%s%s%s%s%s%s" % (lno, from_label, addr, op, arg, data))

            pstart = False

        return "\n".join(output)

    def include_abi_method(self, method, types):
        num_methods = len(method.args)
        num_types = len(types)

        args_types = {}
        # params and return types
        if num_types == num_methods + 1:
            for index, arg in enumerate(method.args):
                args_types[arg] = types[index]
            args_types['return'] = types[num_types - 1]
        else:
            raise Exception("Number of arguments for the abi is incompatible with the function '%s'" % method.full_name)

        self.abi_methods[method.full_name] = args_types

    def set_abi_entry_point(self, method, types):
        if self.abi_entry_point is None:
            self.include_abi_method(method, types)
            self.abi_entry_point = method.full_name
        else:
            raise Exception("Only one method should be entry point")

    def export_debug(self, output_path):
        """
        this method is used to generate a debug map for NEO debugger
        """
        file = open(output_path, 'rb')
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.close()

        avm_name = os.path.splitext(os.path.basename(output_path))[0]

        debug_info = self.generate_avmdbgnfo(avm_name, file_hash)
        debug_json_filename = os.path.basename(output_path.replace('.avm', '.debug.json'))
        avmdbgnfo_filename = output_path.replace('.avm', '.avmdbgnfo')

        with zipfile.ZipFile(avmdbgnfo_filename, 'w', zipfile.ZIP_DEFLATED) as avmdbgnfo:
            avmdbgnfo.writestr(debug_json_filename, debug_info)

    def generate_avmdbgnfo(self, avm_name, file_hash):

        if self.all_vm_tokens is None:
            self.link_methods()

        data = {}
        files = []
        methods = []
        events = []

        for m in self.methods:
            if m.is_interop:
                continue

            method = {}
            method['id'] = m.id.urn
            method['name'] = "{0},{1}".format(m.module.module_name, m.name)
            (_, start) = next(x for x in m.vm_tokens.items())
            (_, end) = next(x for x in reversed(m.vm_tokens.items()))
            method['range'] = '{}-{}'.format(start.addr, end.addr)
            method['params'] = ["{},".format(a) for a in m.args]
            method['return'] = ""
            argCount = len(m.args)
            method['variables'] = ["{},".format(a[0]) for a in m.scope.items() if a[1] >= argCount]

            tokens = []
            last_lineno = None
            method['sequence-points'] = tokens
            for _, (_, value) in enumerate(m.vm_tokens.items()):
                if value.pytoken:
                    pt = value.pytoken

                    if pt.file not in files:
                        files.append(pt.file)

                    fileIndex = files.index(pt.file)
                    lineno = pt.method_lineno + pt.lineno

                    if last_lineno != lineno:                    
                        tokens.append("{}[{}]{}:0-{}:0".format(value.addr, fileIndex, lineno, lineno))
                        last_lineno = lineno

            methods.append(method)

        data['entrypoint'] = self.main.id.urn
        data['documents'] = files
        data['methods'] = methods
        data['events'] = events
        json_data = json.dumps(data, indent=4)
        return json_data

    def export_abi_json(self, output_path):
        """
        this method is used to generate a debug map for NEO debugger
        """
        file = open(output_path, 'rb')
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.close()

        avm_name = os.path.splitext(os.path.basename(output_path))[0]

        abi_info = self.generate_abi_json(avm_name, file_hash)
        abi_json_filename = output_path.replace('.avm', '.abi.json')

        with open(abi_json_filename, 'w+') as out_file:
            out_file.write(abi_info)
            out_file.close()

    def generate_abi_json(self, avm_name, file_hash):
        # Initialize if needed
        if self.all_vm_tokens is None:
            self.link_methods()

        data = {}

        functions = []
        events = []

        data['hash'] = file_hash
        if self.abi_entry_point is not None:
            data['entrypoint'] = self.abi_entry_point
        elif 'main' in self.abi_methods:
            data['entrypoint'] = 'main'
        elif 'Main' in self.abi_methods:
            data['entrypoint'] = 'Main'
        elif len(self.abi_methods) > 0:
            data['entrypoint'] = self.abi_methods.get(0)

        data['functions'] = functions
        data['events'] = events

        for method in self.abi_methods:
            types = self.abi_methods[method]
            params = []
            for t in types:
                if t != 'return':
                    params.append({'name': t, 'type': types[t]})

            function = {
                'name': method,
                'parameters': params,
                'returnType': types['return']
            }

            functions.append(function)
            print()

        json_data = json.dumps(data, indent=4)
        return json_data

    def generate_debug_json(self, avm_name, file_hash):

        # Initialize if needed
        if self.all_vm_tokens is None:
            self.link_methods()

        lineno = 0

        data = {}
        data['avm'] = {'name': avm_name, 'hash': file_hash}
        data['compiler'] = {'name': 'neo-boa', 'version': __version__}

        files = {}
        breakpoints = []
        data['files'] = files

        map = []
        start_ofs = -1
        last_ofs = 0
        fileid = 0
        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            if value.pytoken:
                pt = value.pytoken

                if pt.file:
                    if pt.file not in files.keys():
                        fileid = len(files.values()) + 1
                        files[pt.file] = fileid
                    else:
                        fileid = files[pt.file]

                if pt.lineno != lineno:
                    if start_ofs >= 0:
                        map.append({'start': start_ofs, 'end': key - 1, 'file': fileid, 'method': pt.method_name,
                                    'line': lineno, 'file_line_no': pt.method_lineno + lineno})
                    start_ofs = key
                    lineno = pt.lineno

                if pt.is_breakpoint:
                    breakpoints.append(start_ofs)

                last_ofs = key

        if last_ofs >= 0:
            map.append({'start': start_ofs, 'end': last_ofs, 'file': fileid, 'line': lineno})

        data['map'] = map
        data['breakpoints'] = breakpoints
        data['files'] = [{'id': val, 'url': os.path.abspath(key)} for key, val in files.items()]
        json_data = json.dumps(data, indent=4)
        return json_data
