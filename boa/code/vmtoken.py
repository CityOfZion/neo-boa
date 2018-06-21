from collections import OrderedDict
from boa.interop import VMOp
from boa.interop.BigInteger import BigInteger
from bytecode import Label
from boa.code.pyop import *
NEO_SC_FRAMEWORK = 'boa.interop.'


class VMToken(object):
    """

    """
    addr = None

    pytoken = None

    data = None

    vm_op = None

    src_method = None

    target_method = None

    is_annotation = None

    updatable_data = None

    @property
    def out_op(self):
        """

        :return:
        """
        if type(self.vm_op) is int:
            return self.vm_op
        elif type(self.vm_op) is bytes:
            return ord(self.vm_op)
        else:
            raise Exception('Invalid op: %s ' % self.vm_op)

    def __init__(self, vm_op=None, pytoken=None, addr=None, data=None):
        self.vm_op = vm_op
        self.pytoken = pytoken
        self.addr = addr

        self.data = data

        self.src_method = None
        self.target_method = None

        self.is_annotation = False


class VMTokenizer(object):
    """

    """
    method = None

    _address = None

    vm_tokens = None

    total_param_and_body_count_token = None

    def __init__(self, method):
        self.method = method
        self._address = 0
        self.vm_tokens = OrderedDict()

        self.method_begin_items()

    def method_begin_items(self):

        # we just need to inssert the total number of arguments + body variables
        # which is the length of the method `scope` dictionary
        # then create a new array for the vm to store

        self.convert_push_integer(self.method.stacksize)
        self.convert1(VMOp.NEWARRAY)
        self.convert1(VMOp.TOALTSTACK)

        for index, arg in enumerate(self.method.args):
            self.convert_load_parameter(arg, index)

    def method_end_items(self):
        self.insert1(VMOp.FROMALTSTACK)
        self.insert1(VMOp.DROP)

    def insert_vm_token_at(self, vm_token, index):
        """

        :param vm_token:
        :param index:
        """
        self.vm_tokens[index] = vm_token

    def insert1(self, vm_op, data=None):
        """

        :param vm_op:
        :param data:
        :return:
        """
        start_addr = self._address

        vmtoken = VMToken(vm_op=vm_op, addr=start_addr, data=data)

        self._address += 1

        if vmtoken.data is not None:
            self._address += len(vmtoken.data)

        self.insert_vm_token_at(vmtoken, vmtoken.addr)

        return vmtoken

    def insert_push_data(self, data):
        """

        :param data:
        :return:
        """
        dlen = len(data)

        if dlen == 0:
            return self.insert1(VMOp.PUSH0)

        elif dlen <= 75:
            return self.insert1(dlen, data)

        if dlen < 0x100:
            prefixlen = 1
            code = VMOp.PUSHDATA1

        elif dlen < 0x1000:
            prefixlen = 2
            code = VMOp.PUSHDATA2

        else:
            prefixlen = 4
            code = VMOp.PUSHDATA4

        byts = bytearray(dlen.to_bytes(prefixlen, 'little')) + data

        return self.insert1(code, byts)

    def insert_push_integer(self, i):
        """

        :param i:
        :return:
        """
        if i == 0:
            return self.insert1(VMOp.PUSH0)
        elif i == -1:
            return self.insert1(VMOp.PUSHM1)
        elif 0 < i <= 16:
            out = 0x50 + i
            return self.insert1(out)

        bigint = BigInteger(i)
        outdata = bigint.ToByteArray(signed=False)
        print("big int %s %s" % (bigint, outdata))

        return self.insert_push_data(outdata)

    def convert1(self, vm_op, py_token=None, data=None):
        """

        :param vm_op:
        :param py_token:
        :param data:
        :return:
        """
        start_addr = self._address

        vmtoken = VMToken(vm_op=vm_op, addr=start_addr,
                          pytoken=py_token, data=data)

        self._address += 1

        if vmtoken.data is not None and type(vmtoken.data) is not Label:
            self._address += len(data)

        self.insert_vm_token_at(vmtoken, start_addr)

        return vmtoken

    def convert_new_array(self, py_token=None):

        # push the length of the array
        """

        :param py_token:
        """
        if type(py_token.args) is int:

            self.insert_push_integer(py_token.args)
        else:
            self.convert_load_local(py_token, py_token.args)

        self.convert1(VMOp.PACK, py_token)

    def convert_dup_top_two(self, py_token=None):
        # a, b, c, d
        # <- SWAP
        # b, a, c, d
        # <- DUP
        # b, b, a, c, d
        # <- ROT
        # b, a, b, c, d
        # <- OVER
        # a, b, a, b, c, d
        self.convert1(VMOp.SWAP, py_token)
        self.convert1(VMOp.DUP, py_token)
        self.convert1(VMOp.ROT, py_token)
        self.convert1(VMOp.OVER, py_token)

    def convert_pop_jmp_if(self, pytoken):
        #                token = tokenizer.convert1(VMOp.JMPIF, self, data=bytearray(2))
        token = self.convert1(VMOp.JMPIF, pytoken, data=bytearray(2))
#        self.insert1(VMOp.DROP)
        return token

    def convert_load_const(self, pytoken):
        if type(pytoken.args) is int:
            token = self.convert_push_integer(pytoken.args, pytoken)
        elif type(pytoken.args) is str:
            str_bytes = pytoken.args.encode('utf-8')
#            pytoken.args = str_bytes
            token = self.convert_push_data(str_bytes, pytoken)
        elif type(pytoken.args) is bytes:
            token = self.convert_push_data(pytoken.args, pytoken)
        elif type(pytoken.args) is bytearray:
            token = self.convert_push_data(bytes(pytoken.args), pytoken)
        elif type(pytoken.args) is bool:
            token = self.convert_push_integer(pytoken.args, pytoken)
        elif isinstance(pytoken.args, type(None)):
            token = self.convert_push_data(bytearray(0))
        # TODO - process tuple
#        elif type(pytoken.args) == Code:
#            pass
        else:
            raise Exception("Could not load type %s for item %s " % (
                type(pytoken.args), pytoken.args))
        return token

    def convert_push_data(self, data, py_token=None):
        """

        :param data:
        :param py_token:
        :return:
        """
        dlen = len(data)
        if dlen == 0:
            return self.convert1(VMOp.PUSH0, py_token=py_token)
        elif dlen <= 75:
            return self.convert1(len(data), py_token=py_token, data=data)

        if dlen < 0x100:
            prefixlen = 1
            code = VMOp.PUSHDATA1
        elif dlen < 0x1000:
            prefixlen = 2
            code = VMOp.PUSHDATA2
        else:
            prefixlen = 4
            code = VMOp.PUSHDATA4

        byts = bytearray(dlen.to_bytes(prefixlen, 'little')) + data

        return self.convert1(code, py_token=py_token, data=byts)

    def convert_push_integer(self, i, py_token=None):
        """

        :param i:
        :param py_token:
        :return:
        """
        if i == 0:
            return self.convert1(VMOp.PUSH0, py_token=py_token)
        elif i == -1:
            return self.convert1(VMOp.PUSHM1, py_token=py_token)
        elif 0 < i <= 16:
            out = 0x50 + i
            return self.convert1(out, py_token=py_token)

        bigint = BigInteger(i)

        outdata = bigint.ToByteArray()

        return self.convert_push_data(outdata, py_token=py_token)

    def convert_store_local(self, py_token):

        # set array
        """

        :param py_token:
        """
        self.convert1(VMOp.DUPFROMALTSTACK, py_token=py_token)

        local_name = py_token.args

        if local_name in self.method.scope.keys():
            position = self.method.scope[local_name]

            self.convert_push_integer(position)

            # set item
            self.convert_push_integer(2)
            self.convert1(VMOp.ROLL)
            self.convert1(VMOp.SETITEM)
        else:
            raise Exception("local name '%s' not found in method scope '%s'" % (local_name, self.method.full_name))

    def convert_load_local(self, py_token, name=None):
        """

        :param py_token:
        :param name:
        """

        local_name = py_token.args

        # check to see if this local is a variable
        if local_name in self.method.scope:
            position = self.method.scope[local_name]

            # get array
            self.convert1(VMOp.DUPFROMALTSTACK, py_token=py_token)

            # get i
            self.convert_push_integer(position)
            self.convert1(VMOp.PICKITEM)

        else:
            raise Exception("CANNOT LOAD LOCAL! %s " % local_name)

    def convert_store_subscr(self, pytoken):

        self.convert1(VMOp.ROT)
        self.convert1(VMOp.SETITEM, pytoken)

    def convert_load_parameter(self, arg, position):
        """

        :param arg:
        :param position:
        """
        # get array
        self.convert1(VMOp.DUPFROMALTSTACK)

        self.insert_push_integer(position)
        self.insert_push_integer(2)

        self.insert1(VMOp.ROLL)
        self.insert1(VMOp.SETITEM)

    def convert_built_in_list(self, pytoken):
        """

        :param pytoken:
        """
        lenfound = False
        self.convert1(VMOp.NEWARRAY, pytoken)

    def convert_build_slice(self, pytoken):

        # this was fun!

        # rotate so list is on the top, then move it to alt stack
        self.convert1(VMOp.ROT)
        self.convert1(VMOp.TOALTSTACK, py_token=pytoken)

        # swap the end index and the start index, duplicate start index to alt stack
        self.convert1(VMOp.SWAP)
        self.convert1(VMOp.DUP)
        self.convert1(VMOp.TOALTSTACK)

        # subtract end index from start index, this is placed on the stack
        self.convert1(VMOp.SUB)

        # get the start index and list from alt stack
        self.convert1(VMOp.FROMALTSTACK)
        self.convert1(VMOp.FROMALTSTACK)

        # swap the list and the start index
        self.convert_push_integer(2)
        self.convert1(VMOp.XSWAP)

        # and now perform substr. whew.
        self.convert1(VMOp.SUBSTR)

    def convert_method_call(self, pytoken):

        # special case for list initialization
        """

        :param pytoken:
        :return:
        """

#        pdb.set_trace()

        if pytoken.func_name == 'list':
            return self.convert_built_in_list(pytoken)
        elif pytoken.func_name == 'bytearray':
            return self.convert_push_data(bytes(pytoken.instruction.arg), pytoken)
        elif pytoken.func_name == 'bytes':
            return self.convert_push_data(pytoken.func_params[0].args, pytoken)

#        for t in pytoken.func_params:
#            t.to_vm(self)

        param_len = pytoken.num_params

        if param_len <= 1:
            pass
        elif param_len == 2:
            # if we are using concat or take, we don't want to swap
            if pytoken.func_name != 'concat' and pytoken.func_name != 'take' and pytoken.func_name != 'has_key':
                self.insert1(VMOp.SWAP)

        elif param_len == 3:

            if pytoken.func_name != 'substr':
                self.insert_push_integer(2)
                self.insert1(VMOp.XSWAP)

        else:
            half_p = int(param_len / 2)

            for i in range(0, half_p):
                save_to = param_len - 1 - i

                self.insert_push_integer(save_to)
                self.insert1(VMOp.PICK)

                self.insert_push_integer(i + 1)
                self.insert1(VMOp.PICK)

                self.insert_push_integer(save_to + 2)
                self.insert1(VMOp.XSWAP)
                self.insert1(VMOp.DROP)

                self.insert_push_integer(i + 1)
                self.insert1(VMOp.XSWAP)
                self.insert1(VMOp.DROP)

        # self.insert1(VMOp.NOP)

        fname = pytoken.func_name
        full_name = None
        for m in self.method.module.methods:
            if fname == m.name:
                full_name = m.full_name

        # operational call like len(items) or abs(value)
        if self.is_op_call(fname):
            vmtoken = self.convert_op_call(fname, pytoken)

        # runtime.notify event
        elif self.is_notify_event(pytoken):
            vmtoken = self.convert_notify_event(pytoken)

        # app call ( for calling other contracts on blockchain )
        elif self.is_smart_contract_call(pytoken):
            vmtoken = self.convert_smart_contract_call(pytoken)

        elif self.is_sys_call(full_name):
            vmtoken = self.convert_sys_call(full_name, pytoken)

        # used for python specific built in methods like `enumerate` or `tuple`
        elif self.is_built_in(fname):
            vmtoken = self.convert_built_in(fname, pytoken)

        # otherwise we assume the method is defined by the module
        else:
            vmtoken = self.convert1(
                VMOp.CALL, py_token=pytoken, data=bytearray(b'\x05\x00'))

            vmtoken.src_method = self.method
            vmtoken.target_method = pytoken.func_name
#            pdb.set_trace()

        return vmtoken

    @staticmethod
    def is_op_call(op):
        """

        :param op:
        :return:
        """
        if op in ['len', 'abs', 'min', 'max', 'concat', 'take', 'substr',
                  'reverse', 'append', 'remove', 'keys', 'values', 'has_key',
                  'sha1', 'sha256', 'hash160', 'hash256', 'breakpoint',
                  'verify_signature',
                  'Exception', 'throw_if_null', ]:
            return True
        return False

    def convert_op_call(self, op, pytoken=None):
        """

        :param op:
        :param pytoken:
        :return:
        """
        if op == 'len':
            return self.convert1(VMOp.ARRAYSIZE, pytoken)
        elif op == 'abs':
            return self.convert1(VMOp.ABS, pytoken)
        elif op == 'min':
            return self.convert1(VMOp.MIN, pytoken)
        elif op == 'max':
            return self.convert1(VMOp.MAX, pytoken)
        elif op == 'concat':
            return self.convert1(VMOp.CAT, pytoken)
        elif op == 'take':
            return self.convert1(VMOp.LEFT, pytoken)
        elif op == 'substr':
            return self.convert1(VMOp.SUBSTR, pytoken)
        elif op == 'keys':
            return self.convert1(VMOp.KEYS, pytoken)
        elif op == 'values':
            return self.convert1(VMOp.VALUES, pytoken)
        elif op == 'has_key':
            return self.convert1(VMOp.HASKEY, pytoken)
        elif op == 'sha1':
            return self.convert1(VMOp.SHA1, pytoken)
        elif op == 'sha256':
            return self.convert1(VMOp.SHA256, pytoken)
        elif op == 'hash160':
            return self.convert1(VMOp.HASH160, pytoken)
        elif op == 'hash256':
            return self.convert1(VMOp.HASH256, pytoken)
        elif op == 'verify_signature':
            return self.convert1(VMOp.VERIFY, pytoken)
        elif op == 'reverse':
            return self.convert1(VMOp.REVERSE, pytoken)
        elif op == 'append':
            return self.convert1(VMOp.APPEND, pytoken)
        elif op == 'remove':
            return self.convert1(VMOp.REMOVE, pytoken)
        elif op == 'Exception':
            return self.convert1(VMOp.THROW, pytoken)
        elif op == 'throw_if_null':
            return self.convert1(VMOp.THROWIFNOT, pytoken)
        elif op == 'breakpoint':
            pytoken.is_breakpoint = True
            return self.convert1(VMOp.NOP, pytoken)
        return None

    @staticmethod
    def is_sys_call(op):
        """

        :param op:
        :return:
        """
        if op is not None and NEO_SC_FRAMEWORK in op:
            return True
        return False

    def convert_sys_call(self, op, pytoken=None):
        """

        :param op:
        :param pytoken:
        :return:
        """

        if 'TriggerType.ApplicationR' in op:
            return self.convert_push_data(bytearray(b'\x11'), pytoken)
        elif 'TriggerType.VerificationR' in op:
            return self.convert_push_data(bytearray(b'\x01'), pytoken)
        elif 'TriggerType.Application' in op:
            return self.convert_push_data(bytearray(b'\x10'), pytoken)
        elif 'TriggerType.Verification' in op:
            return self.convert_push_data(bytearray(b'\x00'), pytoken)
        elif 'TransactionType' in op:
            return self.convert_tx_type(op, pytoken)
        elif 'GetTXHash' in op:
            op = op.replace('GetTXHash', 'GetHash')
        elif 'GetInputHash' in op:
            op = op.replace('GetInputHash', 'GetHash')
        elif 'Iterator.Iter' in op:
            op = op.replace('Iterator.Iter', 'Iterator.')
        elif 'Enumerator.Enumerator' in op:
            op = op.replace('Enumerator.Enumerator', 'Enumerator.')
            if op == 'Neo.Enumerator':
                op = 'Neo.Enumerator.Create'

        syscall_name = op.replace(NEO_SC_FRAMEWORK, '').encode('utf-8')
        length = len(syscall_name)
        ba = bytearray([length]) + bytearray(syscall_name)
        pytoken.is_sys_call = False
        vmtoken = self.convert1(VMOp.SYSCALL, pytoken, data=ba)
        self.insert1(VMOp.NOP)
        return vmtoken

    def convert_tx_type(self, op, pytoken=None):
        if 'MinerTransaction' in op:
            return self.convert_push_data(bytearray(b'\x00'), pytoken)
        elif 'IssueTransaction' in op:
            return self.convert_push_data(bytearray(b'\x01'), pytoken)
        elif 'ClaimTransaction' in op:
            return self.convert_push_data(bytearray(b'\x02'), pytoken)
        elif 'EnrollmentTransaction' in op:
            return self.convert_push_data(bytearray(b'\x20'), pytoken)
        elif 'VotingTransaction' in op:
            return self.convert_push_data(bytearray(b'\x24'), pytoken)
        elif 'RegisterTransaction' in op:
            return self.convert_push_data(bytearray(b'\x40'), pytoken)
        elif 'ContractTransaction' in op:
            return self.convert_push_data(bytearray(b'\x80'), pytoken)
        elif 'AgencyTransaction' in op:
            return self.convert_push_data(bytearray(b'\xb0'), pytoken)
        elif 'PublishTransaction' in op:
            return self.convert_push_data(bytearray(b'\xd0'), pytoken)
        elif 'InvocationTransaction' in op:
            return self.convert_push_data(bytearray(b'\xd1'), pytoken)
        elif 'StateTransaction' in op:
            return self.convert_push_data(bytearray(b'\x90'), pytoken)

    @staticmethod
    def is_built_in(op):
        """

        :param op:
        :return:
        """
        if op in ['zip', 'type', 'tuple', 'super', 'str', 'slice',
                  'set', 'reversed', 'property', 'memoryview',
                  'map', 'list', 'frozenset', 'float', 'filter',
                  'enumerate', 'dict', 'divmod', 'complex', 'bytes', 'bytearray', 'bool',
                  'int', 'vars', 'sum', 'sorted', 'round', 'setattr', 'getattr',
                  'rep', 'quit', 'print', 'pow', 'ord', 'oct', 'next', 'locals', 'license',
                  'iter', 'isinstance', 'issubclass', 'input', 'id', 'hex',
                  'help', 'hash', 'hasattr', 'globals', 'format', 'exit',
                  'exec', 'eval', 'dir', 'deleteattr', 'credits', 'copyright',
                  'compile', 'chr', 'callable', 'bin', 'ascii', 'any', 'all', ]:
            return True

        return False

    def convert_built_in(self, op, pytoken):
        """

        :param op:
        :param pytoken:
        :return:
        """
        syscall_name = None
        if op == 'print':
            syscall_name = 'Neo.Runtime.Log'.encode('utf-8')

        elif op == 'enumerate':
            syscall_name = b'Neo.Enumerator.Create'
        elif op == 'iter':
            syscall_name = b'Neo.Iterator.Create'
        elif op == 'next':
            syscall_name = b'Neo.Enumerator.Next'

        elif op == 'reversed':
            raise NotImplementedError(
                "[Compilation error] Built in %s is not implemented. Use array.reverse() instead." % op)

        if syscall_name:
            length = len(syscall_name)
            ba = bytearray([length]) + bytearray(syscall_name)
            vmtoken = self.convert1(VMOp.SYSCALL, pytoken, data=ba)
            return vmtoken

        raise NotImplementedError(
            "[Compilation error] Built in %s is not implemented" % op)

    def is_notify_event(self, pytoken):
        """

        :param pytoken:
        :return:
        """
        name = pytoken.func_name
        for action in self.method.module.actions:
            if action.method_name == name:
                return True
        return False

    def convert_notify_event(self, pytoken):
        """

        :param pytoken:
        :return:
        """
        event_action = None
        for action in self.method.module.actions:
            if action.method_name == pytoken.func_name:
                event_action = action
        if event_action is None:
            raise Exception("Event action not found")

        # push the event name
        event_name = event_action.event_name.encode('utf-8')
        self.convert_push_data(event_name, py_token=None)

        # push the num params
        self.convert_push_integer(len(event_action.event_args))

        # pack the array
        self.convert1(VMOp.PACK)

        # insert syscall
        syscall_name = 'Neo.Runtime.Notify'.encode('utf-8')
        length = len(syscall_name)
        ba = bytearray([length]) + bytearray(syscall_name)
        vmtoken = self.convert1(VMOp.SYSCALL, pytoken, data=ba)
#        self.insert1(VMOp.NOP)

        return vmtoken

    def is_smart_contract_call(self, pytoken):
        """

        :param pytoken:
        :return:
        """
        name = pytoken.func_name

        if name == 'DynamicAppCall':
            pytoken.is_dynamic_appcall = True
            return True

        for appcall in self.method.module.app_call_registrations:
            if appcall.method_name == name:
                return True
        return False

    def convert_smart_contract_call(self, pytoken):
        """

        :param pytoken:
        :return:
        """

        if pytoken.is_dynamic_appcall:

            # push the contract hash
            vmtoken = self.convert1(
                VMOp.APPCALL, py_token=pytoken, data=bytearray(20))

            # self.insert1(VMOp.NOP)
            return vmtoken

        # this is used for app calls that are registered
        # using RegisterAppCall(script_hash, *args)
        sc_appcall = None
        for appcall in self.method.module.app_call_registrations:
            if appcall.method_name == pytoken.func_name:
                sc_appcall = appcall
        if sc_appcall is None:
            raise Exception("Smart Contract Appcall %s not found " %
                            pytoken.func_name)

        # push the contract hash
        vmtoken = self.convert1(
            VMOp.APPCALL, py_token=pytoken, data=sc_appcall.script_hash_addr)

        return vmtoken
