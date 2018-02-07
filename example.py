from boa.compiler import Compiler
from boa.compiler import Compiler as MyCompiler

#module = Compiler.load('boa/tests/src/AddTest1.py').default
#print(module.bp.code)
module = Compiler.load_and_save('boa/tests/src/AddTest1.py')

print('-----------------')

#myModule = MyCompiler.load('myboa/tests/src/AddTest1.py').default
#print(myModule.bc)
myModule = MyCompiler.load_and_save('myboa/tests/src/AddTest1.py')
