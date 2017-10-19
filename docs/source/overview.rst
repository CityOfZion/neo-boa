Overview
========

The ``neo-boa`` compiler is a tool for compiling Python files to the ``.avm`` format for usage in the `Neo Virtual Machine <https://github.com/neo-project/neo-vm/>`_ which is used to execute contracts on the `Neo Blockchain <https://github.com/neo-project/neo/>`_

The compiler supports a subset of the Python language ( in the same way that a Boa Contstrictor is a subset of the Python snake species)


What does it currently do
^^^^^^^^^^^^^^^^^^^^^^^^^

-  Compiles a subset of the Python language to the ``.avm`` format for
   use in the `Neo Virtual Machine`_
-  Works for Python 3.4 and 3.5

What will it do
^^^^^^^^^^^^^^^

-  Compile a larger subset of the Python language
-  Support Python 3.6


What parts of Python are supported?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current portions of the Python language which are supported.  For more details, please see all samples in the ``boa.tests.src`` directory

- Flow Control:

    - If, Else, Elif, While, Break, Method calls, Lamdbas, for x in

- Arithmetric and equality Operators for integer math:

    - ADD,SUB,MUL,DIV,ABS,LSHIFT,RSHIFT,AND,OR,XOR,MODULO,INVERT,GT,GTE,LT,LTE,EQ,NOTEQ,

- list creation is supported via a custom builtin.  It should be noted that once created, a list length is not mutable.

    .. code-block:: python

        from boa.code.builtins import list

        # the following is ok
        x = list(length=10)
        x[3] = 84

        # this is also ok
        x = [1,3,65,23]

        # this is not ok
        x = []
        x.append(1)

- list manipulation ( building slices ) is currently supported

    .. code-block:: python

        x = [1,2,46,56]
        y = x[1:3]


- Where possible, some of Python's ``__builtins__`` have been implemented in a custom way for the Neo Virtual Machine:

    .. code-block:: python

        from boa.code.builtins import range

        xrange = range(1, 30)

        #this also works

        for i in range(2, 21):
            i = i + 1



What is not supported and why?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current Neo Virtual Machine is not as complex as your average Python interpreter, and for this reason, many of the things you might take for granted in Python will either not work, or not work as expected.  Because of this, there are many items in Python's standard
``__builtins__`` library that cannot be compiled to a source that the Neo Virtual Machine would understand. Due to these limitations, it would not be wise, or even possible to import your favorite python library to do some kind of work for you.  It is advised that you write
everything you plan on using in a smart contract using the functionality listed above.

- The ``__builtins__`` items listed below are not supported at the moment.  Many of them are not supported because the would not be supported inside the Neo Virtual Machine, while a few of these items are not supported because they have not yet been implemented.

    .. code-block:: python

         ['zip', 'type', 'tuple', 'super', 'str', 'slice',
                      'set', 'reversed', 'property', 'memoryview',
                      'map', 'list', 'frozenset', 'float', 'filter',
                      'enumerate', 'dict', 'divmod', 'complex', 'bytes', 'bytearray', 'bool',
                      'int', 'vars', 'sum', 'sorted', 'round', 'setattr', 'getattr',
                      'rep', 'quit', 'print', 'pow', 'ord', 'oct', 'next', 'locals', 'license',
                      'iter', 'isinstance', 'issubclass', 'input', 'id', 'hex',
                      'help', 'hash', 'hasattr', 'globals', 'format', 'exit',
                      'exec', 'eval', 'dir', 'deleteattr', 'credits', 'copyright',
                      'compile', 'chr', 'callable', 'bin', 'ascii', 'any', 'all', ]


- List comprehension expressions are also not currently supported.  This is on the roadmap.

    .. code-block:: python

        #not supported
        m = [x for x in range(1,10)]

- Class objects are currently not supported.  This functionality is on the roadmap
