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

        to_s = default_module.to_s()

        output = sc.write()

        self.assertIsInstance(output, bytes)

        self.assertTrue(len(output) > 0)
