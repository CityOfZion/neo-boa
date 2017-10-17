<p align="center">
  <img
    src="http://res.cloudinary.com/vidsy/image/upload/v1503160820/CoZ_Icon_DARKBLUE_200x178px_oq0gxm.png"
    width="125px;">
</p>

<h1 align="center">neo-boa</h1>

<p align="center">
  Python compiler for the Neo Virtual Machine
</p>

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Tests](#tests)
- [Donatitons](#donations)

## Overview

A Python compiler for the Neo Virtual Machine


#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm)
- Works for Python 3.4 and 3.5
 
#### What will it do

- Compile a larger subset of the Python language
- Support Python 3.6

#### Get Help or give help

- Open a new [issue](https://github.com/CityOfZion/neo-boa/issues/new) if you encounter a problem.
- Or ping **@localhuman** on the [NEO Slack](https://join.slack.com/t/neoblockchainteam/shared_invite/MjE3ODMxNDUzMDE1LTE1MDA4OTY3NDQtNTMwM2MyMTc2NA).
- Pull requests welcome. New features, writing tests and documentation are all needed. 


## Installation

#### Pip

``` 
pip install neo-boa
```

#### Manual

Clone the repository and navigate into the project directory. Make a Python 3 virtual environment and activate
it via

```
python3 -m venv venv
source venv/bin/activate
```

or to install Python 3.5 specifically

```
virtualenv -p /usr/local/bin/python3.5 venv
source venv/bin/activate
```

Then install requirements
```
pip install -r requirements.txt
```

## Usage

The compiler may be used like the following

```
from boa.compiler import Compiler

Compiler.load_and_save('path/to/your/file.py')
```


## Tests

Tests are important.  

## License

- Open-source [MIT](https://github.com/CityOfZion/neo-python/blob/master/LICENSE.md).
- Main author is [@localhuman](https://github.com/localhuman).


## Donations

Accepted at __ATEMNPSjRVvsXmaJW4ZYJBSVuJ6uR2mjQU__