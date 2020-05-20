import argparse
import sys
import os
from boa import __version__
from boa.compiler import Compiler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"neo-boa v{__version__}")
    parser.add_argument("input", help=".py smart contract to compile")
    args = parser.parse_args()

    if not args.input.endswith(".py") or not os.path.isfile(args.input):
        print("Input file is not .py")
        sys.exit(1)

    Compiler.load_and_save(args.input)
    print(f"Wrote {args.input.replace('.py', '.avm')} to {os.path.abspath(os.curdir)}/")


if __name__ == "__main__":
    main()
