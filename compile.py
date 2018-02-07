import os
import sys
from pprint import pprint
from boa.compiler import Compiler

TEST_DIR = 'boa/tests/src/'

def compile_all():
    error_list = []
    total = 0
    success = 0
    for folder in os.walk(TEST_DIR):
        for filename in sorted(folder[2]):
            relative_path = folder[0].replace(TEST_DIR, '')
            if len(relative_path) > 0:
                filename ='{}/{}'.format(relative_path,filename)
            if not filename.endswith('.py'):
                continue
            total += 1
            try:
                compile_one(filename)
                success += 1
            except:
                error_list.append(filename)
                print('Error happened while processing :(')

    print('{}% ({}/{}) compiled!'.format(100*success/total, success, total))
    if len(error_list):
        print('These had errors:')
        pprint(error_list)

def compile_one(filename):
    filepath = '{}{}'.format(TEST_DIR, filename)
    print('Compiling {}...'.format(filename))
    module = Compiler.load_and_save(filepath)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        compile_all()
    else:
        compile_one(sys.argv[1])

