Overview
========

The ``neo-boa`` compiler is a tool for compiling Python files to the ``.avm`` format for usage in the `Neo Virtual Machine <https://github.com/neo-project/neo-vm/>`_. The latter is used to execute contracts on the `Neo Blockchain <https://github.com/neo-project/neo/>`_.

The compiler supports a subset of the Python language (in the same way that a Boa Contstrictor is a subset of the Python snake species.)

What it currently does
^^^^^^^^^^^^^^^^^^^^^^

-  Compiles a subset of the Python language to the ``.avm`` format for
   use in the `Neo Virtual Machine`_.
-  Works for Python 3.6+
-  Support dictionary objects
-  Adds debugging map for debugging in neo-python or other NEO debuggers

What will it do
^^^^^^^^^^^^^^^

-  Compile a larger subset of the Python language.


What parts of Python are supported?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a glimpse into the currently supported Python language features. 
For details, please see all samples in the ``example`` directory.

- Flow Control:

    - If, Else, Elif, While, Break, Method calls, for x in y.

- Arithmetric and equality Operators for integer math:

    - ADD, SUB, MUL, DIV, ABS, LSHIFT, RSHIFT, AND, OR, XOR, MODULO, INVERT, GT, GTE, LT, LTE, EQ, NOTEQ.

- List creation is supported via a custom builtin. It should be noted that once created, a list length is not mutable.

    .. code-block:: python

        from boa.code.builtins import list

        # this works
        x = list(length=10)
        x[3] = 84

        # this also works
        x = [1,3,65,23]

        x.append('neo')

        x.remove(1)

        x.reverse()


- list manipulation (building slices) is supported for strings and byte arrays, but not for lists

    .. code-block:: python

        x = [1,2,46,56]
        # this will not work
        y = x[1:3]


        x = bytearray(b'\x01\x02\x03\x04')


        # this will be bytearray(b'\x03\x04')
        k = x[1:3]

        # you must specify the end element of a slice, the following will not work
        z = x[1:]

        # instead, use this
        z = x[1:len(x)]


        # the -1 index of a list does also not work at the moment

- Where possible, some of Python's ``__builtins__`` have been implemented in a custom way for the Neo Virtual Machine.

    .. code-block:: python

        from boa.code.builtins import range

        xrange = range(1, 30)

        # this also works
        for i in range(2, 21):
            i = i + 1

What is not supported and why?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current Neo Virtual Machine is not as complex as your average Python interpreter. Therefore, there are many items in Python's standard ``__builtins__`` library that cannot be compiled to an executable smart contract. It would thus not be wise, or even possible, to import your favorite python library to do some kind of work for you. It is instread advised that you write
everything you plan on using in a smart contract using the functionality listed above.

- The ``__builtins__`` items listed below are **not** supported at the moment. Many of them are not supported because the would not be supported inside the Neo Virtual Machine, while a few of these items are not supported because they just have not yet been implemented in boa.

    .. code-block:: python

         'zip', 'type', 'tuple', 'super', 'str', 'slice', 
         
         'set', 'reversed', 'property', 'memoryview',
         
         'map', 'list', 'frozenset', 'float', 'filter', 
         
         'enumerate', 'dict', 'divmod', 'complex', 
         
         'bytes',  'bool', 'int', 'vars',
          
         'sum', 'sorted', 'round', 'setattr', 'getattr',
          
         'rep', 'quit', 'print', 'pow', 'ord', 
          
         'oct', 'next', 'locals', 'license', 'iter', 
          
         'isinstance', 'issubclass', 'input', 'id', 'hex', 
          
         'help', 'hash', 'hasattr', 'globals', 'format', 
          
         'exit', 'exec', 'eval', 'dir', 'deleteattr', 
          
         'credits', 'copyright', 'compile', 'chr', 'callable', 
          
         'bin', 'ascii', 'any', 'all'

- List comprehension expressions are also **not** currently supported. This is on the roadmap.

    .. code-block:: python

        # this does NOT work
        m = [x for x in range(1,10)]

- Class objects are currently **not** supported. Use dictionaries instead


- Dictionaries are supported

    .. code-block:: python

        d = {
            'a': 10,
            'b': 4
            'j': mymethodCall(),
            'q': [1,3,5]
        }


        qlist = d['q']