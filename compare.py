import os
import sys
from pprint import pprint

from boa.compiler import Compiler
from boa.compiler import Compiler as MyCompiler

ORIGINAL_DIR = 'boa/tests/src/'
NEW_DIR = 'myboa/tests/src/'

def run_all():
    total = 0
    success = 0
    error_list = []
    for filename in sorted(os.listdir(ORIGINAL_DIR)):
        if not filename.endswith('.py'):
            continue
        total += 1
        try:
            if run_one(filename):
                success += 1
            else:
                error_list.append(filename)
        except:
            error_list.append(filename)
            print('Error happened while processing :(')

    print('{}% ({}/{}) passed!'.format(100*success/total, success, total))
    if len(error_list):
        print('These did not pass:')
        pprint(error_list)

def run_one(filename):
    original_file = '{}{}'.format(ORIGINAL_DIR, filename)
    new_file  = '{}{}'.format(NEW_DIR, filename)
    original_avm = original_file.replace('.py', '.avm')
    new_avm = new_file.replace('.py', '.avm')
    print('Evaluating {}...'.format(filename))
    module = Compiler.load_and_save(original_file)
    print('      ')
    print('======')
    print('======')
    print('======')
    print('======')
    print('      ')
    myModule = MyCompiler.load_and_save(new_file)
    f1 = open(original_avm, 'rb')
    f2 = open(new_avm, 'rb')
    original_avm_bytecode = f1.read()
    new_avm_bytecode = f2.read()
    f1.close()
    f2.close()
    if original_avm_bytecode != new_avm_bytecode:
        print('Bytecodes do not match!')
        print(original_avm_bytecode)
        print(new_avm_bytecode)
        return False
    else:
        print('Bytecodes match!')
        return True

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_all()
    else:
        run_one(sys.argv[1])

