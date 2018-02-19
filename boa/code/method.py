from bytecode import ControlFlowGraph,BasicBlock,Instr,Bytecode
from boa.util import print_block
from boa.code.vmtoken import VMTokenizer
from boa.code.expression import Expression
from boa.code import pyop
import pdb

class method(object):

    code = None # type:code
    bytecode = None # type:Bytecode

    block = None

    blocks = []

    stack_size = 0

    tokens = []
    tokenizer = None

    address = 0

    module = None

    name = None
    module_name = None

    _expressions = None

    _scope = None


    @property
    def vm_tokens(self):
        """
        Returns a list of all vm tokens in this method.

        :return: a list of vm tokens in this method
        :rtype: list
        """

        return self.tokenizer.vm_tokens

    @property
    def full_name(self):
        if len(self.module_name):
            return '%s.%s' %  (self.module_name,self.name)
        return self.name

    @property
    def scope(self):
        return self._scope

    @property
    def args(self):
        return self.bytecode.argnames

    @property
    def stacksize(self):
        return self.bytecode.argcount + len(self.cfg)

    def __init__(self, module, block, module_name=''):
        self.module = module
        self.block = block
        self.module_name = module_name
        self._scope = {}
        try:
            self.code = self.block[0].arg
            self.name = self.block[1].arg
        except Exception as e:
            print("Colud not get code or name %s " % e)

        self.bytecode = Bytecode.from_code(self.code)
        self.cfg = ControlFlowGraph.from_bytecode(self.bytecode)

        for index,name in enumerate(self.bytecode.argnames):
            self._scope[name] = index


        for block in self.cfg:
            start_ln = block[0].lineno
            for index,instr in enumerate(block):
                if instr.lineno != start_ln:
                    self.cfg.split_block(block,index)

        jmptargets=[]
        for block in self.cfg:
            if block.get_jump():
                jmptargets.append(block.get_jump())

        for index,block in enumerate(self.cfg):
            if block in jmptargets:
                if block[-1].opcode == pyop.RETURN_VALUE and len(block) > 1:
                    self.cfg.split_block(block, 1)

#        print_block(self.cfg, self.cfg[0])

        for block in self.cfg:
            for instr in block:
                if instr.opcode == pyop.STORE_FAST:
                    current_total = len(self._scope)
                    self._scope[instr.arg] = current_total

        self.tokenizer = VMTokenizer(self)

        self._expressions = []

    def prepare(self):
        for blk in self.cfg:
            exp = Expression(blk, self.tokenizer)
            exp.tokenize()
            self._expressions.append(exp)
        self.convert_jumps()

    def convert_jumps(self):
        for block in self.cfg:
            jmp = block.get_jump()
            if jmp:
                j_start=None
                j_end = None
                for key,vmtoken in self.tokenizer.vm_tokens.items():
                    if vmtoken.pytoken and vmtoken.pytoken.expression.block == block:
                        j_start = vmtoken
                    if not j_end and vmtoken.pytoken:
                        if vmtoken.pytoken.expression.block == jmp:
                            j_end = vmtoken

                if j_start and j_end:
                    diff = j_end.addr - j_start.addr
                    j_start.data = diff.to_bytes(2, 'little',signed=True)
                else:
                    raise Exception("Could not determine conditional jump for block %s " % block)


#        print("method end items!!! %s " % self.tokenizer.vm_tokens[-1])
        #pdb.set_trace()
#            self._cfblocks.append( BlockToken(blk, self.tokenizer))








