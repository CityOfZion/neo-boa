Basic Usage
-----------

The compiler may be used as follows

::

    from boa.compiler import Compiler

    Compiler.load_and_save('path/to/your/file.py')


For legacy purposes, if you wish to compile without NEP8 stack isolation functionality, you may do the following:

::

    from boa.compiler import Compiler

    Compiler.load_and_save('path/to/your/file.py', use_nep=False)



See `boa.compiler.Compiler` and other modules for more advanced usage.
