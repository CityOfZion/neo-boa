========================
[Interop] Neo Blockchain
========================

The items below are used for gathering state data contained within the blockchain.
Because all items below are implemented in the Neo Virtual Machine, their source is not available here.
Please see the `neo-python <https://github.com/CityOfZion/neo-python>`_ project if you want to know more about their exact implementation.


Blockchain
^^^^^^^^^^

.. automodule:: boa.interop.Neo.Blockchain


Header
^^^^^^
A Header object contains all information about a block, except for the transaction data.

.. automodule:: boa.interop.Neo.Header


Block
^^^^^

A Block object contains the transaction data for a block.

.. automodule:: boa.interop.Neo.Block


Account
^^^^^^^

The Account object represents an address on the blockchain.

.. automodule:: boa.interop.Neo.Account


Action
^^^^^^

An Action object is used to register an action/event listener on the blockchain.

.. automodule:: boa.interop.Neo.Action


App
^^^

An App object used to call other contracts on the blockchain.

.. automodule:: boa.interop.Neo.App


Asset
^^^^^

An Asset object is used to look up information about native assets such as NEO or Gas.

.. automodule:: boa.interop.Neo.Asset
