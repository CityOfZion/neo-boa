========================
[Interop] Neo Blockchain
========================

The items below are used for gathering state data contained within the blockchain.
Because all items below are implemented in the Neo Virtual Machine, their source is not available here.
Please see the `neo-python <https://github.com/CityOfZion/neo-python>`_ project if you would like to know more about their exact implementation.


Blockchain
^^^^^^^^^^

.. automodule:: boa.blockchain.vm.Neo.Blockchain


Header
^^^^^^
The header object contains all of information about a block except for the transaction data

.. automodule:: boa.blockchain.vm.Neo.Header


Block
^^^^^

The block object contains the transaction data for a block

.. automodule:: boa.blockchain.vm.Neo.Block



Account
^^^^^^^

The account object represents an address on the blockchain

.. automodule:: boa.blockchain.vm.Neo.Account


Action
^^^^^^

Actions are used to register an action/ event listener on the blockchain

.. automodule:: boa.blockchain.vm.Neo.Action


App
^^^

App calls are used to call other contracts on the blockchain

.. automodule:: boa.blockchain.vm.Neo.App


Asset
^^^^^

Assets are used to look up information about blockchain native assets such as NEO or Gas

.. automodule:: boa.blockchain.vm.Neo.Asset


