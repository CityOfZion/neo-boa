from bytecode import ControlFlowGraph,BasicBlock,Instr,Bytecode,Label,Compare
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


    _forloop_counter = 0

    _finished_loops = None

    @property
    def forloop_counter(self):
        self._forloop_counter+=1
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
        return self.bytecode.argcount + len(self.cfg) + 20

    def __init__(self, module, block, module_name=''):
        self.module = module
        self.block = block
        self.module_name = module_name
        self._finished_loops = []

        try:
            self.code = self.block[0].arg
            self.name = self.block[1].arg
        except Exception as e:
            print("Colud not get code or name %s " % e)

        self.bytecode = Bytecode.from_code(self.code)
        self.init_cfg()

    def init_cfg(self):

        self._scope = {}

        self.cfg = ControlFlowGraph.from_bytecode(self.bytecode)

        for index,name in enumerate(self.bytecode.argnames):
            self._scope[name] = index


#        print_block(self.cfg, self.cfg[0])

        for block in self.cfg:
            start_ln = block[0].lineno
            for index,instr in enumerate(block):
                if instr.lineno != start_ln:
                    self.cfg.split_block(block,index)


        # checking for loop iterations
        got_setup = False
        for index,block in enumerate(self.cfg):
            if not got_setup and block[0].opcode == pyop.SETUP_LOOP and not block[0].lineno in self._finished_loops:
                next_block = self.cfg[index+1]
                print("FOUND A SETUP!!!!!!!! %s " % block)
                got_setup = True
                for item in next_block:
                    # we've found a for loop
                    if item.opcode == pyop.GET_ITER:
                        print("FOUND A GETER %s " % block)
                        loop_end_idex = self.cfg.get_block_index( block[0].arg)
                        loopblocks = self.cfg[index:loop_end_idex]
                        self.reprogram_loop(loopblocks, index, loop_end_idex)
                        return

        jmptargets=[]
        for block in self.cfg:
            if block.get_jump():
                jmptargets.append(block.get_jump())

        for index,block in enumerate(self.cfg):
            if block in jmptargets:
                if block[-1].opcode == pyop.RETURN_VALUE and len(block) > 1:
                    self.cfg.split_block(block, 1)


        for block in self.cfg:
            for instr in block:
                if instr.opcode == pyop.STORE_FAST:
                    self.add_to_scope(instr.arg)


        self.tokenizer = VMTokenizer(self)

        self._expressions = []


    def add_to_scope(self, argname):
        if not argname in self.scope.keys():
            current_total = len(self._scope)
            self._scope[argname] = current_total

    def prepare(self):
        for blk in self.cfg:
            exp = Expression(blk, self.tokenizer)
            self._expressions.append(exp)
            exp.tokenize()

        self.convert_jumps()
        self.convert_breaks()


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
#                    print("START, END %s%s\n %s%s " % (vars(j_start.pytoken),vars(j_start), vars(j_end.pytoken),vars(j_end)))
#                    pdb.set_trace()
                    diff = j_end.addr - j_start.addr
                    j_start.data = diff.to_bytes(2, 'little',signed=True)
                else:
                    print("Could not determine conditional jump for block %s " % block)

    def convert_breaks(self):
        tokens = list(self.vm_tokens.values())
        tokens.reverse()
        brk_token = None
        for tkn in tokens:
            if tkn.pytoken:
                if tkn.pytoken.pyop == pyop.BREAK_LOOP:
                    brk_token=tkn
                if tkn.pytoken.pyop == pyop.SETUP_LOOP and brk_token:
                    setup_token_jump_target = int.from_bytes(tkn.data,'little') + tkn.addr
                    diff = setup_token_jump_target - brk_token.addr
                    brk_token.data = diff.to_bytes(2,'little',signed=True)
                    brk_token = None



    def reprogram_loop(self, loopblocks, startloop, endloop):
        print("reprogramming olooppp")
        self._finished_loops.append(loopblocks[0][0].lineno)

        instructions = []
        for index,blk in enumerate(self.cfg):
            if index < startloop:
                for item in blk:
                    instructions.append(item)

        instructions += self.create_loop_instructions(loopblocks)

        for index,blk in enumerate(self.cfg):
            if index >= endloop:
                for item in blk:
                    instructions.append(item)

        self.bytecode = Bytecode(instructions)
        self.init_cfg()



    def create_loop_instructions(self, loopblocks):

        ln = loopblocks[0][0].lineno

        new_items = []

        for index,blk in enumerate(loopblocks):
            if index > 3 and index < len(loopblocks) -1:
                for instr in blk:
                    new_items.append(instr)

        if len(new_items) and new_items[-1].opcode == pyop.JUMP_ABSOLUTE:
            new_items.pop(-1)

        if len(new_items):
            last_ln = new_items[-1].lineno

        counter = self.forloop_counter

        loopcounter_name = 'fl_counter_%s' % counter
        looplength_name = 'fl_len_%s' % counter

        iterable = loopblocks[1][0].arg
        iterable_name = loopblocks[3][0].arg
        self.add_to_scope(loopcounter_name)
        self.add_to_scope(looplength_name)
        self.add_to_scope(iterable_name)

        loop_start = Label()
        loop_done = Label()
        loop_exit = Label()

        instructions = [
#            Instr("SETUP_LOOP", loop_exit,lineno=ln),

            Instr("LOAD_CONST",0,lineno=ln),
            Instr("STORE_FAST",arg=loopcounter_name,lineno=ln),
            Instr("LOAD_FAST", arg=iterable,lineno=ln),
            Instr("LOAD_GLOBAL",arg="len",lineno=ln),
            Instr("CALL_FUNCTION",arg=1,lineno=ln),
            Instr("STORE_FAST",arg=looplength_name,lineno=ln),

            loop_start,
#                Instr("FOR_ITER",loop_done,lineno=ln),
                Instr("LOAD_FAST",arg=loopcounter_name,lineno=ln),
                Instr("LOAD_FAST",arg=looplength_name,lineno=ln),
                Instr("COMPARE_OP",arg=Compare.LT,lineno=ln),
                Instr("POP_JUMP_IF_FALSE",loop_done,lineno=ln),


                Instr("LOAD_FAST",arg=iterable,lineno=ln),
                Instr("LOAD_FAST",arg=loopcounter_name, lineno=ln),
                Instr("BINARY_SUBSCR",lineno=ln),
                Instr("STORE_FAST",arg=iterable_name,lineno=ln),

                Instr("LOAD_FAST",loopcounter_name,lineno=ln),
                Instr("LOAD_CONST",1,lineno=ln),
                Instr("INPLACE_ADD",lineno=ln),
                Instr("STORE_FAST",loopcounter_name, lineno=ln),

        ] + new_items + [

                Instr("JUMP_ABSOLUTE", loop_start,lineno=last_ln+1),
            loop_done,
                Instr("POP_BLOCK",lineno=last_ln+1),
            loop_exit,

        ]

        return instructions



