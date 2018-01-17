
from byteplay3 import Opcode
from boa.code.pytoken import PyToken
from boa.code import pyop
from boa.code.vmtoken import NEO_SC_FRAMEWORK
import pdb


class Block(object):

    """

    """
    forloop_counter = 0

    localmethod_counter = 0

    oplist = None  # list

    _label = None  # list

    iterable_variable = None
    iterable_loopcounter = None
    iterable_looplength = None
    iterable_item_name = None

    slice_item_length = None

    has_dynamic_iterator = False

    local_func_name = None
    local_func_varname = None

    def __init__(self, operation_list):
        self.oplist = operation_list

        self.iterable_variable = None
        self.iterable_loopcounter = None
        self.iterable_looplength = None
        self.iterable_item_name = None

        self.has_dynamic_iterator = False

        self.slice_item_length = None

    def __str__(self):
        if self._label:
            return '[Block] %s          [label] %s' % (self.oplist, self._label)
        return '[Block]: %s' % self.oplist

    def set_label(self, label):
        """

        :param label:
        """
        self._label = label
        self.oplist[0].jump_label = label

    @property
    def line(self):
        """

        :return:
        """
        if len(self.oplist):
            token = self.oplist[0]
            return token.line_no
        return None

    @property
    def has_store_fast(self):
        for token in self.oplist:
            if token.py_op == pyop.STORE_FAST:
                return True
        return False

    @property
    def has_load_attr(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.LOAD_ATTR and token.instance_type is None:
                if token.args not in ['reverse', 'append', 'remove', ]:
                    return True
        return False

    @property
    def has_store_attr(self):
        """

        Returns:
            bool
        """
        for token in self.oplist:
            if token.py_op == pyop.STORE_ATTR:
                return True
        return False

    @property
    def has_make_function(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.MAKE_FUNCTION:
                return True
        return False

    @property
    def has_slice(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.BUILD_SLICE:
                return True

    @property
    def is_return(self):
        """

        :return:
        """
        if len(self.oplist):
            token = self.oplist[-1]
            if token.py_op == pyop.RETURN_VALUE:
                return True
        return False

    @property
    def is_iter(self):
        """

        :return:
        """
        has_get_iter = False
        for token in self.oplist:
            if token.py_op == pyop.GET_ITER:
                has_get_iter = True
            elif token.py_op == pyop.MAKE_FUNCTION:
                return False
        return has_get_iter

    @property
    def iterable_local_vars(self):
        """

        :return:
        """
        return [
            self.iterable_looplength,
            self.iterable_loopcounter,
            self.iterable_item_name,
        ]

    @property
    def has_unprocessed_method_calls(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.CALL_FUNCTION and not token.func_processed:
                return True
        return False

    @property
    def has_unprocessed_array_sub(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.STORE_SUBSCR and not token.array_processed:
                return True
        return False

    @property
    def has_unprocessed_array(self):
        """

        :return:
        """
        for token in self.oplist:
            if token.py_op == pyop.BUILD_LIST and not token.array_processed:
                return True
        return False

    def preprocess_store_attr(self, method):

        for index, token in enumerate(self.oplist):
            if token.py_op == pyop.STORE_ATTR:
                to_store_into = self.oplist[index - 1].args

                if to_store_into == 'self':
                    ivar_type = method.parent
                    token.instance_type = ivar_type
                else:
                    try:
                        ivar_type = method.instance_vars[to_store_into]
                        token.instance_type = ivar_type
                        token.instance_name = to_store_into
                    except Exception as e:
                        print("Couldnt load instance variable: %s %s " % (to_store_into, e))

    def preprocess_load_attr(self, method):
        """

        :param method:
        """

        while self.has_load_attr:

            to_rep = {}
            to_del = []
            is_sys_attr_lookup = False

            for index, token in enumerate(self.oplist):

                index_to_rep = -1
                new_call = None

                if token.py_op == pyop.LOAD_ATTR:
                    from boa.code.items import Klass

                    to_load_from = self.oplist[index - 1]
                    varname = to_load_from.args
                    ivar_type = None
                    is_func_call = True
                    do_nothing = False

                    if varname in method.instance_vars.keys():
                        ivar_type = method.instance_vars[varname]

                        test_sysmodule = '%s.Get%s' % (ivar_type.module.module_path, token.args)

                        if NEO_SC_FRAMEWORK in test_sysmodule:
                            what_to_load = 'Get%s' % token.args
                            is_sys_attr_lookup = True
                        else:
                            what_to_load = '%s.%s' % (ivar_type.name, token.args)
                            token.instance_type = ivar_type

                            # if this is a class variable lookup, do this
                            if token.args in ivar_type.class_var_names:
                                is_func_call = False
                                what_to_load = token.args

                            # otherwise, it is a method call on an object, we don't want to do anything
                            else:
                                token.func_params = [self.oplist[index - 1]]
                                do_nothing = True

                    elif varname == 'self' and type(method.parent) is Klass:
                        ivar_type = method.parent

                        what_to_load = '%s.%s' % (str(ivar_type), token.args)
                        if token.args in ivar_type.class_var_names:
                            is_func_call = False
                            what_to_load = token.args

                    else:
                        what_to_load = 'Get%s' % token.args
                        is_sys_attr_lookup = True

                    if not do_nothing:
                        if is_func_call:
                            call_func = PyToken(
                                Opcode(pyop.CALL_FUNCTION), lineno=self.line, index=-1, args=what_to_load)
                            call_func.instance_type = ivar_type
                            call_func.func_processed = True
                            call_func.func_name = what_to_load
                            call_func.func_params = [self.oplist[index - 1]]

                            index_to_rep = index
                            new_call = call_func

                        else:
                            new_call = PyToken(Opcode(pyop.LOAD_CLASS_ATTR), lineno=self.line, args=what_to_load)
                            new_call.instance_type = ivar_type
                            new_call.instance_name = varname
                            new_call.func_processed = True
                            index_to_rep = index

                    if index_to_rep > 0:

                        td = self.oplist[index_to_rep - 1]
#                        print("TO DELETE: %s %s %s " % (td.py_op, td.jump_label, td.args))
                        if td.jump_label is not None and not is_sys_attr_lookup:
                            new_call.jump_label = td.jump_label

                        to_rep[index_to_rep] = new_call
                        to_del.append(self.oplist[index_to_rep - 1])

            for key, val in to_rep.items():
                self.oplist[key] = val

            for item in to_del:
                # print("WILL DELET: %s %s %s" % (item, vars(item), item.args))
                if item in self.oplist:
                    self.oplist.remove(item)
                else:
                    pdb.set_trace()

        # print("oplist: %s " % [str(op) for op in self.oplist])
        # pdb.set_trace()

    def preprocess_load_class(self, method):
        # print("PREPROCESS LOAD BUilD CLASS: %s %s " % (method, method.name))
        pass

    def preprocess_make_function(self, method):
        """

        :param method:
        """
        code_obj = self.oplist[0].args
        code_obj_name = self.oplist[1].args
        self.local_func_name = "%s_%s" % (
            code_obj_name, Block.localmethod_counter)
        Block.localmethod_counter += 1

        from boa.code.method import Method

        m = Method(code_object=code_obj, parent=method.parent,
                   make_func_name=self.local_func_name)
        method.parent.add_method(m)

        self.local_func_varname = self.oplist[-1].args

    def preprocess_slice(self):
        """
        this method processes slices of strings or byte arrays such as item[1:3]
        """
        index_to_remove = -1

        for index, token in enumerate(self.oplist):
            if token.py_op == pyop.BUILD_SLICE:

                # first, we want to take out the BINARY_SUBSC op, since we wont need it
                index_to_remove = index + 1

                # now we want to check the second item, for example item[2:4], we need to check 4
                # if you do item[2:], in python, normally the end is inferred
                # but we get None.
                # in that case, we need to convert None into the length of the item being sliced
                end_op = self.oplist[index - 1]

                if end_op.args is None:
                    # 0xffffff
                    # if you have a list greater than that length, well you'll have other problems than this
                    max_len = 16777215
                    end_op.args = max_len

        if index_to_remove > -1:
            del self.oplist[index_to_remove]

    def preprocess_iter(self):

        # in a better world this would be done in a more efficient way
        # for now this is kept to be as understandable as possible
        """

        """
        loopsetup = self.oplist[0]
        loopsetup.args = None
        loopsetup.jump_label = None

        # first we need to create a loop counter variable
        self.iterable_loopcounter = 'forloop_counter_%s' % Block.forloop_counter

        # load the value 0
        loopcounter_start_ld_const = PyToken(
            op=Opcode(pyop.LOAD_CONST), lineno=loopsetup.line_no, index=-1, args=0)
        # now store the loop counter
        loopcounter_store_fast = PyToken(op=Opcode(
            pyop.STORE_FAST), lineno=loopsetup.line_no, index=-1, args=self.iterable_loopcounter)

        # this loads the list that is going to be iterated over ( LOAD_FAST )
        # this will be removed... its added into the call get length token function params
        # unless this is a dynamic iteration, like for x in range(x,y)
        dynamic_iterable_items = []

        iterable_load = self.oplist[1]

        self.iterable_item_name = iterable_load.args

        if iterable_load.py_op == pyop.CALL_FUNCTION:

            self.has_dynamic_iterator = True

            self.iterable_item_name = 'forloop_dynamic_range_%s' % Block.forloop_counter

            dynamic_iterator_store_fast = PyToken(op=Opcode(pyop.STORE_FAST), lineno=loopsetup.line_no, index=-1,
                                                  args=self.iterable_item_name)

            # if we're calling a method in this for i in, like for i in range(x,y) then we need
            # to call the function
            dynamic_iterable_items = [
                iterable_load, dynamic_iterator_store_fast]

        # Now we need to get the length of that list, and store that as a local variable

        call_get_length_token = PyToken(
            op=Opcode(pyop.CALL_FUNCTION), lineno=loopsetup.line_no, args=1)
        call_get_length_token.func_params = [iterable_load]
        call_get_length_token.func_name = 'len'

        # now we need a variable name to store the length of the array
        self.iterable_looplength = 'forloop_length_%s' % Block.forloop_counter

        # now store the variable which is the output of the len(items) call
        looplength_store_op = PyToken(op=Opcode(
            pyop.STORE_FAST), lineno=loopsetup.line_no, index=-1, args=self.iterable_looplength)

        get_iter = self.oplist[2]
        for_iter = self.oplist[3]

        store_iterable_name = self.oplist[4]

        # set the iterable variable name ( for example, i ) so that the loop body can use it
        self.iterable_variable = store_iterable_name.args

        ld_loopcounter = PyToken(op=Opcode(
            pyop.LOAD_FAST), lineno=loopsetup.line_no, index=-1, args=self.iterable_loopcounter)

        ld_loop_length = PyToken(op=Opcode(
            pyop.LOAD_FAST), lineno=loopsetup.line_no, index=-1, args=self.iterable_looplength)

        new__compare_op = PyToken(
            op=Opcode(pyop.COMPARE_OP), lineno=loopsetup.line_no, index=-1, args='<')
        new__popjump_op = PyToken(op=Opcode(
            pyop.POP_JUMP_IF_FALSE), lineno=loopsetup.line_no, index=-1, args=for_iter.args)

        for_iter.args = None

        self.oplist = [
            loopsetup,  # SETUP_LOOP

            get_iter,  # GET_ITER, keep this in for now


            # the following 4 ops set up the iterator

            loopcounter_start_ld_const,  # LOAD_CONST 0
            loopcounter_store_fast,  # STORE_FAST forloopcounter_X

            # dynamic load loop stuff would go here

            call_get_length_token,  # CALL_FUNCTION 1

            looplength_store_op,  # STORE_FAST forloop_length_X


            # these last 5 ops controls the operation of the loop

            for_iter,  # tihs is the jump target for the end of the loop execution block

            ld_loopcounter,  # load in the loop counter LOAD_FAST forloopcounter_X

            ld_loop_length,  # load in the loop length LOAD_FAST forloop_length_X

            new__compare_op,  # COMPARE_OP <, this will compare foorloop_counter_X < forloop_length_X

            new__popjump_op  # POP_JUMP_IF_FALSE jumps to the loop exit when counter == length
        ]

        if len(dynamic_iterable_items):
            self.oplist.insert(4, dynamic_iterable_items[0])
            self.oplist.insert(5, dynamic_iterable_items[1])

        Block.forloop_counter += 1

    def process_iter_body(self, setup_block):
        """

        :param setup_block:
        """
        first_op = self.oplist[0]

        #
        # the following loads the iterated item into the block
        #

        # load the iterable collection
        ld_load_iterable = PyToken(op=Opcode(
            pyop.LOAD_FAST), lineno=first_op.line_no, index=-1, args=setup_block.iterable_item_name)

        # load the counter var
        ld_counter = PyToken(op=Opcode(pyop.LOAD_FAST), lineno=first_op.line_no,
                             index=-1, args=setup_block.iterable_loopcounter)

        # binary subscript of the iterable collection
        ld_subscript = PyToken(op=Opcode(pyop.BINARY_SUBSCR),
                               lineno=first_op.line_no, index=-1)

        # now store the iterated item
        st_iterable = PyToken(op=Opcode(
            pyop.STORE_FAST), lineno=first_op.line_no, index=-1, args=setup_block.iterable_variable)

        #
        # the following load the forloop counter and increments it
        #

        # load the counter var
        ld_counter_2 = PyToken(op=Opcode(
            pyop.LOAD_FAST), lineno=first_op.line_no, index=-1, args=setup_block.iterable_loopcounter)
        # load the constant 1
        increment_const = PyToken(
            op=Opcode(pyop.LOAD_CONST), lineno=first_op.line_no, index=-1, args=1)
        # add it to the counter
        increment_add = PyToken(
            op=Opcode(pyop.INPLACE_ADD), lineno=first_op.line_no, index=-1)
        # and store it again
        increment_store = PyToken(op=Opcode(
            pyop.STORE_FAST), lineno=first_op.line_no, index=-1, args=setup_block.iterable_loopcounter)

        self.oplist = [
            ld_load_iterable, ld_counter, ld_subscript, st_iterable,

            ld_counter_2, increment_const, increment_add, increment_store

        ] + self.oplist

    def lookup_return_types(self, orig_method):
        ivars = {}
        klass_type = None
        for index, token in enumerate(self.oplist):
            if token.py_op == pyop.CALL_FUNCTION:
                param_count = token.args

                # why would param count be 256 when calling w/ kwargs?
                # when keyword args are sent, the param count is 256 * num params?
                if param_count % 256 == 0:
                    param_count = 2 * int(param_count / 256)

#                params = self.oplist[index - param_count:index]

                call_method_op = self.oplist[index - param_count - 1]
                call_method_name = call_method_op.args

                for method in orig_method.module.methods:
                    if method.name == call_method_name and method.return_type is not None:
                        klass_type = method.return_type

            if token.py_op == pyop.STORE_FAST and klass_type is not None:
                ivars[token.args] = klass_type
                klass_type = None

        return ivars

    def preprocess_method_calls(self, orig_method):
        """

        :param orig_method:
        """

        ivars = {}

        alreadythere = False

        while self.has_unprocessed_method_calls:
            start_index_change = None
            end_index_change = None
            changed_items = None
            klass = None

            for index, token in enumerate(self.oplist):

                if token.py_op == pyop.CALL_FUNCTION and not token.func_processed:
                    token.func_processed = True

                    param_count = token.args

                    # why would param count be 256 when calling w/ kwargs?
                    # when keyword args are sent, the param count is 256 * num paramms?
                    if param_count % 256 == 0:
                        param_count = 2 * int(param_count / 256)

                    params = self.oplist[index - param_count:index]

                    call_method_op = self.oplist[index - param_count - 1]
                    call_method_type = call_method_op.py_op
                    call_method_name = call_method_op.args

                    if call_method_op.instance_type:

                        # the call_method_op has a referecnce to the instance being called
                        # as the only item in the func_params ( this is python's self object )
                        # we will create a new param array by adding that one to the beginning of the method params

                        #                        print("PARAMS: %s "% params)
                        #                        print("COLL METHEHOD: %s "% call_method_op)
                        #                        print("call method name %s " % call_method_op.args)
                        #                        print("call method op func params: %s "% call_method_op.func_params)

                        #                        if call_method_name == 'owner':
                        #                            pdb.set_trace()

                        params = call_method_op.func_params + params

                        token.args = len(params)
                        param_count = token.args
                        if call_method_op.instance_type.name in call_method_op.args:
                            call_method_name = call_method_op.args
                            alreadythere = True

                        else:
                            call_method_name = "%s.%s" % (call_method_op.instance_type.name, call_method_op.args)

                    # we need to check if this is a method
                    # that is local to this block's method
                    if orig_method:
                        for key, value in orig_method.local_methods.items():
                            if key == call_method_name:
                                call_method_name = value

                    token.func_name = call_method_name
                    token.func_type = call_method_type

                    # check to see if this method call creates an instance of another object
                    if orig_method:
                        klass = orig_method.lookup_type(token.func_name)

                    if klass:
                        ivar_iname = self.oplist[2].args
                        ivars[ivar_iname] = klass

                    # if this method is the target of a jump
                    # or if one of its parameters is the target of a jump
                    # we need to catch that and use that jump label
                    # otherwise bad things
                    if call_method_op.jump_label is not None:
                        if len(params) > 0:
                            params[0].jump_label = call_method_op.jump_label
                        else:
                            token.jump_label = call_method_op.jump_label

                    token.func_params = params
                    changed_items = [token]

                    start_index_change = index - param_count - 1
                    end_index_change = index

            if start_index_change is not None and end_index_change is not None:
                tstart = self.oplist[0:start_index_change]
                tend = self.oplist[end_index_change + 1:]
                self.oplist = tstart + changed_items + tend

        if alreadythere:
            if self.oplist[-1].py_op == pyop.STORE_FAST:
                self.oplist = self.oplist[-2:]

        return ivars

    def preprocess_array_subs(self):
        """

        """
        while self.has_unprocessed_array_sub:
            start_index_change = None
            end_index_change = None
            changed_items = None

            for index, token in enumerate(self.oplist):
                if token.py_op == pyop.STORE_SUBSCR and not token.array_processed:
                    token.array_processed = True
                    start_index_change = index - 3
                    end_index_change = index

                    item_to_sub = self.oplist[index - 3].args
                    array_to_sub = self.oplist[index - 2].args
                    index_to_sub_at = self.oplist[index - 1].args
                    changed_items = []

                    # load the array to set the item into
                    ld_op = PyToken(Opcode(pyop.LOAD_FAST),
                                    token.line_no, args=array_to_sub)
                    changed_items.append(ld_op)

                    # create the setitem op
                    settoken = PyToken(Opcode(
                        pyop.SETITEM), token.line_no, args=index_to_sub_at, array_item=item_to_sub)
                    changed_items.append(settoken)

            if start_index_change is not None and end_index_change is not None:
                tstart = self.oplist[0:start_index_change]
                tend = self.oplist[end_index_change + 2:]
                self.oplist = tstart + changed_items + tend

    def preprocess_arrays(self):
        """

        """
        while self.has_unprocessed_array:

            blist_start_index = None
            blist_end_index = None
            array_items = []
            for index, token in enumerate(self.oplist):
                if token.py_op == pyop.BUILD_LIST and not token.array_processed and blist_start_index is None:

                    num_list_items = token.args
                    blist_start_index = index - num_list_items
                    blist_end_index = index
                    array_items = self.oplist[index -
                                              num_list_items:num_list_items]
                    array_items.reverse()

                    token.array_processed = True

            if blist_start_index is not None:
                self.oplist = self.oplist[0:blist_start_index] + \
                    array_items + self.oplist[blist_end_index:]

    def mark_as_end(self):
        """

        """
        tstart = self.oplist[:-1]
        tend = self.oplist[-1:]

        newitems = [PyToken(Opcode(pyop.NOP), self.line),
                    #                    PyToken(pyop.DROP_BODY, self.line),
                    PyToken(Opcode(pyop.FROMALTSTACK), self.line),
                    PyToken(Opcode(pyop.DROP), self.line)]

        self.oplist = tstart + newitems + tend
