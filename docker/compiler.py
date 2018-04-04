import os
from boa.compiler import Compiler

input_file_dir = '/python-contracts'
output_file_dir = '/compiled-contracts'

for file in os.listdir(input_file_dir):
    if file.endswith('.py'):
        file_name = file.replace('.py','')
        input_file_path = os.path.join(input_file_dir, file)
        output_file = file_name + '.avm'
        output_file_path = os.path.join(output_file_dir, output_file)
        try:
            Compiler.load_and_save(path=input_file_path, output_path=output_file_path)
            print(' \033[92mCompiled\t{}'.format(file))
        except Exception as e:
            print(' \033[93mFail\t\t{}\t{}'.format(file, e))

