from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
import os


class TestContract(BoaTest):

    TEST_SC_OUTPUT = 'boa_test/example/AddTest1.avm'

    @classmethod
    def setUpClass(cls):
        super(TestContract, cls).setUpClass()
        try:
            os.remove(cls.TEST_SC_OUTPUT)
        except Exception as e:
            pass

    def test_compile_1(self):

        try:
            sc = Compiler.load_and_save('%s/boa_test/example/AddTest1.py' % TestContract.dirname)

            expected_output = '%s/%s' % (TestContract.dirname, self.TEST_SC_OUTPUT)

            self.assertTrue(os.path.exists(expected_output))
        except PermissionError:
            pass

    def test_compile_2(self):

        sc = Compiler.load('%s/boa_test/example/AddTest1.py' % TestContract.dirname)

        default_module = sc.default

        output = sc.write()

        self.assertIsInstance(output, bytes)

        self.assertTrue(len(output) > 0)

    def test_compile_3(self):

        sc = """from boa.interop.Neo.App import RegisterAppCall
from boa.interop.Neo.Runtime import Log
from boa.interop.Neo.Iterator import Iterator

enumerate = RegisterAppCall('1e68de2d4442b868c544b4104c8fe2172f580591', 'operation', 'args')

def Main():
    token_iter = enumerate('enumerate',[])
    count = 0
    result = []
    while token_iter.next() and (count < 5):
        result.append(token_iter.Value)
        count += 1
    return result"""

        compiler = Compiler.load_contract(sc)

        avm = compiler.write_contract()
        expected = "59c56b09656e756d657261746500c176c97ce101029105582f17e28f4c10b444c568b842442dde681e6a00527ac4006a51527ac400c176c96a52527ac461616a00c368134e656f2e456e756d657261746f722e4e6578746434006a51c3559f642c006a52c36a00c368124e656f2e4974657261746f722e56616c756561c86a51c351936a51527ac462b6ff6161616a52c36c7566"

        self.assertTrue(avm == expected)
