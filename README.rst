
===========================================
Python compiler for the Neo Virtual Machine
===========================================

Overview
--------

The ``neo-boa`` compiler is a tool for compiling Python files to the
``.avm`` format for usage in the `Neo Virtual
Machine <https://github.com/neo-project/neo-vm/>`__ which is used to
execute contracts on the `Neo
Blockchain <https://github.com/neo-project/neo/>`__.

The compiler supports a subset of the Python language ( in the same way
that a *boa constrictor* is a subset of the Python snake species)

What does it currently do
^^^^^^^^^^^^^^^^^^^^^^^^^

-  Compiles a subset of the Python language to the ``.avm`` format for
   use in the `Neo Virtual
   Machine <https://github.com/neo-project/neo-vm>`__
-  Works for Python 3.6+
-  Adds debugging map for debugging in neo-python or other NEO debuggers


What will it do
^^^^^^^^^^^^^^^

-  Compile a larger subset of the Python language

Get Help or give help
^^^^^^^^^^^^^^^^^^^^^

-  Open a new
   `issue <https://github.com/CityOfZion/neo-boa/issues/new>`__ if you
   encounter a problem.
-  Or ping **@localhuman** on the `NEO official community
   chatroom <https://discord.gg/R8v48YA>`__.
-  Pull requests welcome. New features, writing tests and documentation
   are all needed.

Installation
------------

Make sure you are using a Python 3.6 or greater virtual environment

Pip
^^^

::

    pip install neo-boa

Docker
^^^^^^

This project contains a Dockerfile to batch compile Python smart
contracts. Clone the repository and navigate into the docker sub
directory of the project. Run the following command to build the
container:

::

    docker build -t neo-boa .

The neo-boa Docker container takes a directory on the host containing
python smart contracts as an input and a directory to compile the .avm
files to as an output. It can be executed like this:

::

    docker run -it -v /absolute/path/input_dir:/python-contracts -v /absolute/path/output_dir:/compiled-contracts neo-boa

The -v (volume) command maps the directories on the host to the
directories within the container.

Manual
^^^^^^

Clone the repository and navigate into the project directory. Make a
Python 3 virtual environment and activate it via:

::

    python3 -m venv venv
    source venv/bin/activate

or, to install Python 3.6 specifically:

::

    virtualenv -p /usr/local/bin/python3.6 venv
    source venv/bin/activate

Then, install the requirements:

::

    pip install -r requirements.txt

Usage
-----

The compiler may be used like in the following example:

::

    from boa.compiler import Compiler

    Compiler.load_and_save('path/to/your/file.py')

Docs
----

You can `read the docs
here <http://neo-boa.readthedocs.io/en/latest/>`__.

Tests
-----

All tests are located in ``boa_test/test``.  Tests can be run with the following command ``python -m unittest discover boa_test``

License
-------

-  Open-source `MIT <LICENSE.md>`__.
-  Main author is `localhuman <https://github.com/localhuman>`__.

Donations
---------

Accepted at **ATEMNPSjRVvsXmaJW4ZYJBSVuJ6uR2mjQU**
