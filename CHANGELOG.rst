Changelog
=========

All notable changes to this project following the ``v0.4.1`` release are noted in this file

[0.5.3] 2018-09-28
-----------------------
- ``module.to_s()`` method now returns a string instead of printing it
- Update to allow ``CALL_FUNCTION`` opcode within a ``GET_ITER`` instruction.

[0.5.2] 2018-09-25
-----------------------
- Implement NEP8 call functionality

[0.5.1] 2018-09-24
-----------------------
- Use reduced sized fixtures for quicker tests

[0.5.0] 2018-08-26
-----------------------
- Python 3.7 compatibility

[0.4.9] 2018-08-24
-----------------------
- Updated NEP5 sample
- Updated equality operator conversion

[0.4.8] 2018-07-05
-----------------------
- Updated module loading to prevent duplicates of modules.
- Updated ``LOAD_ATTR`` parsing to fix bug with multiple ``LOAD_ATTR`` in one statement
- Updated tests for compatibility with ``neo-python`` changes

[0.4.7] 2018-06-21
-----------------------
- Add support for python opcodes ``DUP_TOP_TWO``, ``ROT_THREE``, and ``ROT_TWO``

[0.4.6] 2018-06-19
-----------------------
- Add support for Enumerator/Iterator interop methods in NEO

[0.4.5] 2018-06-18
-----------------------
- update tests for changes in neo-python

[0.4.4] 2018-05-31
-----------------------
- remove support for JUMP_IF_TRUE_OR_POP and JUMP_IF_FALSE_OR_POP
- add support for NEP7 triggers

[0.4.3] 2018-05-14
-----------------------
- add support for JUMP_IF_TRUE_OR_POP and JUMP_IF_FALSE_OR_POP

[0.4.2] 2018-04-30
-----------------------
- add support for VERIFY opcode to verify arbitrary message
- add support for ``boa.interop.Neo.Storage.Find`` operation
- add tests for comparison ``in`` operator
- update documentation
- Print error msg with file/linenumber/method during tokenization error

