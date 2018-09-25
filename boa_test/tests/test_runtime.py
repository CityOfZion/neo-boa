from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild

from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events, SmartContractEvent


class TestContract(BoaFixtureTest):

    def test_Runtime(self):

        dispatched_events = []
        dispatched_logs = []

        def on_notif(evt):
            dispatched_events.append(evt)

        def on_log(evt):
            dispatched_logs.append(evt)
        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.on(SmartContractEvent.RUNTIME_LOG, on_log)

        output = Compiler.instance().load('%s/boa_test/example/blockchain/RuntimeTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['get_time', 1], self.GetWallet1(), '0202', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\xc2Y\xa1['))

        tx, results, total_ops, engine = TestBuild(out, ['check_witness', self.wallet_1_script_hash.Data], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['log', 'hello'], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)
        self.assertEqual(len(dispatched_logs), 1)
        self.assertEqual(dispatched_logs[0].event_payload.Value, 'hello')

        tx, results, total_ops, engine = TestBuild(out, ['notify', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)
        self.assertEqual(len(dispatched_events), 1)
        self.assertEqual(int.from_bytes(dispatched_events[0].event_payload.Value, 'little'), 1234)

        tx, results, total_ops, engine = TestBuild(out, ['get_trigger', 1234], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 16)

        events.off(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.off(SmartContractEvent.RUNTIME_LOG, on_log)

    def test_Triggers(self):

        output = Compiler.instance().load('%s/boa_test/example/blockchain/TriggerTypeTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x10'))

        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x00'))

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x20'))

        tx, results, total_ops, engine = TestBuild(out, [0], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), -1)

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x11'))

        tx, results, total_ops, engine = TestBuild(out, [5], self.GetWallet1(), '02', '02')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x01'))
