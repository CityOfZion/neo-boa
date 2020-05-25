<p align="center">
  <img
    src="https://raw.githubusercontent.com/CityOfZion/visual-identity/develop/_CoZ%20Branding/_Logo/_Logo%20icon/_PNG%20200x178px/CoZ_Icon_DARKBLUE_200x178px.png"
    width="125px;">
</p>

<h1 align="center">neo-boa</h1>
<p align="center">
  Python compiler for the Neo Virtual Machine
</p>

<a href="https://pypi.python.org/pypi/neo-boa" rel="nofollow"><img src="https://img.shields.io/pypi/v/neo-boa.svg"></a>
<a href="https://travis-ci.org/CityOfZion/neo-boa" rel="nofollow"><img src="https://img.shields.io/travis/CityOfZion/neo-boa.svg"></a>
<a href="https://neo-boa.readthedocs.io/en/latest/?badge=latest" rel="nofollow"><img src="https://readthedocs.org/projects/neo-boa/badge/?version=latest"></a>
<a href='https://coveralls.io/github/CityOfZion/neo-boa?branch=master'><img src='https://coveralls.io/repos/github/CityOfZion/neo-boa/badge.svg?branch=master' alt='Coverage Status' /></a>
<ul>
<li>Free software: MIT license</li>
<li>Documentation: <a href="https://neo-boa.readthedocs.io" rel="nofollow">https://neo-boa.readthedocs.io</a>.</li>
</ul>



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
- Works for Python 3.6+
- supports dictionaries
- Adds debugging map for debugging in neo-python or other NEO debuggers


#### What will it do

- Compile a larger subset of the Python language

#### Get Help or give help

- Open a new [issue](https://github.com/CityOfZion/neo-boa/issues/new) if you encounter a problem.
- Or ping **@localhuman** on the [NEO official community chatroom](https://discord.gg/R8v48YA).
- Pull requests welcome. New features, writing tests and documentation are all needed.


## Installation

Installation requires a Python 3.6 or later environment.

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
docker run -it --rm -v /absolute/path/input_dir:/python-contracts -v /absolute/path/output_dir:/compiled-contracts neo-boa
```

The -v (volume) command maps the directories on the host to the directories within the container.

#### Manual

Clone the repository and navigate into the project directory. Make a Python 3 virtual environment and activate it via:

```
python3 -m venv venv
source venv/bin/activate
```

or, to install Python 3.6 specifically:

```
virtualenv -p /usr/local/bin/python3.6 venv
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

Or navigate into `boa` directory and use the command:

```
cli.py path/to/your/file.py
```

For legacy functionality without NEP8 stack isolation compatibility, use the following:

```
from boa.compiler import Compiler

Compiler.load_and_save('path/to/your/file.py', use_nep8=False)
```



## Docs

You can [read the docs here](http://neo-boa.readthedocs.io/en/latest/).


## Tests

Install `neo-python` ( or use `requirements_test.txt`) and run the following command
```
python -m unittest discover boa_test

```


## License

- Open-source [MIT](LICENSE.md).
- Main author is [@localhuman](https://github.com/localhuman).


## Donations

Accepted at __ATEMNPSjRVvsXmaJW4ZYJBSVuJ6uR2mjQU__
