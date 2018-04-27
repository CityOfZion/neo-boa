from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Settings import settings

settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_storage_find(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/StorageFindTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['prefix'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 3)
        self.assertEqual([1, 2, 3], sorted([item.GetBigInteger() for item in resItems]))

        tx, results, total_ops, engine = TestBuild(out, ['neo'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 0)

        tx, results, total_ops, engine = TestBuild(out, ['blah'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 1)
        self.assertEqual(resItems[0].GetString(), 'Hello Storage Find')

        tx, results, total_ops, engine = TestBuild(out, ['prefix1e'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 2)

        tx, results, total_ops, engine = TestBuild(out, ['pre'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 2)

        tx, results, total_ops, engine = TestBuild(out, ['pref'], self.GetWallet1(), '', '10')
        self.assertEqual(len(results), 1)
        resItems = results[0].GetArray()
        self.assertEqual(len(resItems), 3)
        self.assertEqual(sorted(['prefix1euo', 'prefix1e', 'prefix1__osetuh', ]), sorted([item.GetString() for item in resItems]))
