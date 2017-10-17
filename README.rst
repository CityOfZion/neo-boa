
===========================================
Python compiler for the Neo Virtual Machine
===========================================


-  `Overview`_
-  `Installation`_
-  `Usage`_
-  `License`_
-  `Tests`_
-  `Donatitons`_

Overview
--------

A Python compiler for the Neo Virtual Machine

What does it currently do
^^^^^^^^^^^^^^^^^^^^^^^^^

-  Compiles a subset of the Python language to the ``.avm`` format for
   use in the `Neo Virtual Machine`_
-  Works for Python 3.4 and 3.5

What will it do
^^^^^^^^^^^^^^^

-  Compile a larger subset of the Python language
-  Support Python 3.6

Get Help or give help
^^^^^^^^^^^^^^^^^^^^^

-  Open a new `issue`_ if you encounter a problem.
-  Or ping **@localhuman** on the `NEO Slack`_.
-  Pull requests welcome. New features, writing tests and documentation
   are all needed.

Installation
------------

Pip
^^^

::

    pip install neo-boa

Manual
^^^^^^

Clone the repository and navigate into the project directory. Make a
Python 3 virtual environment and activate it via

::

    python3 -m venv venv
    source venv/bin/activate

or to install Python 3.5 specifically

::

    virtualenv -p /usr/local/bin/python3.5 venv
    source venv/bin/activate

Then install requirements

::

    pip install -r requirements.txt

Usage
-----

The compiler may be used like the following

::

    from boa.compiler import Compiler

    Compiler.load_and_save('path/to/your/file.py')

Tests
-----

Tests are important.

License
-------

-  Open-source `MIT`_.
-  Main author is **localhuman** [ https://github.com/localhuman ].

Donations
---------

Accepted at **ATEMNPSjRVvsXmaJW4ZYJBSVuJ6uR2mjQU**

.. _Overview: #overview
.. _Installation: #installation
.. _Usage: #usage
.. _License: #license
.. _Tests: #tests
.. _Donatitons: #donations
.. _Neo Virtual Machine: https://github.com/neo-project/neo-vm
.. _issue: https://github.com/CityOfZion/neo-boa/issues/new
.. _NEO Slack: https://join.slack.com/t/neoblockchainteam/shared_invite/MjE3ODMxNDUzMDE1LTE1MDA4OTY3NDQtNTMwM2MyMTc2NA
.. _MIT: https://github.com/CityOfZion/neo-python/blob/master/LICENSE.md