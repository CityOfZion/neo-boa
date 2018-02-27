from boa_test.tests.boa_test import BoaFixtureTest
from neo.Settings import settings
from neo.Core.State.ContractState import ContractState
from neo.SmartContract.StorageContext import StorageContext
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild
import os
import shutil


settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class TestContract(BoaFixtureTest):

    @classmethod
    def tearDownClass(cls):
        super(BoaFixtureTest, cls).tearDownClass()

        try:
            if os.path.exists(settings.DEBUG_STORAGE_PATH):
                shutil.rmtree(settings.DEBUG_STORAGE_PATH)
        except Exception as e:
            print("couldn't remove debug storage %s " % e)

    def test_Contract(self):
        output = Compiler.instance().load('%s/boa_test/example/blockchain/ContractTest.py' % TestContract.dirname).default
        out = output.write()

        contract_hash = bytearray(b"\xccN\xe2\xf1\xc9\xf4\xe0x\'V\xda\xbf$m\nO\xe6\n\x03T")
        contract_script = '746b4c04000000004c04000000004c04000000006161681e416e745368617265732e426c6f636b636861696e2e47657448656967687461681d416e745368617265732e426c6f636b636861696e2e476574426c6f636b744c0400000000948c6c766b947275744c0400000000936c766b9479744c0400000000948c6c766b947961681d416e745368617265732e4865616465722e47657454696d657374616d70a0744c0401000000948c6c766b947275744c0401000000948c6c766b9479641b004c0400000000744c0402000000948c6c766b947275623200744c0401000000936c766b9479744c0402000000936c766b9479617cac744c0402000000948c6c766b947275620300744c0402000000948c6c766b947961748c6c766b946d748c6c766b946d748c6c766b946d746c768c6b946d746c768c6b946d746c768c6b946d6c7566'

        tx, results, total_ops, engine = TestBuild(out, ['get_contract', contract_hash], self.GetWallet1(), '070505', '05')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0].GetInterface(), ContractState)

        tx, results, total_ops, engine = TestBuild(out, ['get_script', contract_hash], self.GetWallet1(), '070505', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray().hex(), contract_script)

        tx, results, total_ops, engine = TestBuild(out, ['get_storage_context', contract_hash], self.GetWallet1(), '070505', '05')
        self.assertEqual(len(results), 0)

        tx, results, total_ops, engine = TestBuild(out, ['destroy', contract_hash], self.GetWallet1(), '070505', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)
