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
- [Docs](#docs)
- [License](#license)
- [Tests](#tests)
- [Donations](#donations)

## Overview

The `neo-boa` compiler is a tool for compiling Python files to the `.avm` format for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

The compiler supports a subset of the Python language ( in the same way that a _boa constrictor_ is a subset of the Python snake species)


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

#### Docker

This project contains a Dockerfile to batch compile Python smart contracts. Clone the repository and navigate into the docker sub directory of the project. Run the following command to build the container:

```
docker build -t neo-boa .
```

The neo-boa Docker container takes a directory on the host containing python smart contracts as an input and a directory to compile the .avm files to as an output. It can be executed like this:

```
docker run -it -v /absolute/path/input_dir:/python-contracts -v /absolute/path/output_dir:/compiled-contracts neo-boa
```

The -v (volume) command maps the directories on the host to the directories within the container.

#### Manual

Clone the repository and navigate into the project directory. Make a Python 3 virtual environment and activate it via:

```
python3 -m venv venv
source venv/bin/activate
```

or, to install Python 3.5 specifically:

```
virtualenv -p /usr/local/bin/python3.5 venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```



## Usage

The compiler may be used like in the following example:

```
from boa.compiler import Compiler

Compiler.load_and_save('path/to/your/file.py')
```


## Docs

You can [read the docs here](http://neo-boa.readthedocs.io/en/latest/).


## Tests

Tests are important.


## License

- Open-source [MIT](https://github.com/CityOfZion/neo-python/blob/master/LICENSE.md).
- Main author is [@localhuman](https://github.com/localhuman).


## Donations

Accepted at __ATEMNPSjRVvsXmaJW4ZYJBSVuJ6uR2mjQU__
