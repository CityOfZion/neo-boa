from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler

from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events, SmartContractEvent


class TestContract(BoaTest):

    def test_Event1(self):

        dispatched_events = []

        def on_notif(evt):
            dispatched_events.append(evt)
        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)

        output = Compiler.instance().load('%s/boa_test/example/blockchain/EventTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [], self.GetWallet1(), '', '07')
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].GetBigInteger(), 7)

        events.off(SmartContractEvent.RUNTIME_NOTIFY, on_notif)

        self.assertEqual(len(dispatched_events), 2)

        transfer_event_payload = dispatched_events[0].event_payload

        self.assertEqual(len(transfer_event_payload), 4)
        self.assertEqual(transfer_event_payload[0], b'transfer_test')
        self.assertEqual(transfer_event_payload[1], 2)
        self.assertEqual(transfer_event_payload[2], 5)
        self.assertEqual(transfer_event_payload[3], 7)

        refund_event_payload = dispatched_events[1].event_payload
        self.assertEqual(len(refund_event_payload), 3)
        self.assertEqual(refund_event_payload[0], b'refund')
        self.assertEqual(refund_event_payload[1], b'me')
        self.assertEqual(int.from_bytes(refund_event_payload[2], 'little'), 52)
