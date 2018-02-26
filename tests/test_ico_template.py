from tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events, SmartContractEvent
from neo.Settings import settings
from neo.Prompt.Utils import parse_param

from example.demo.nex.token import *

import shutil
import os

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


    def test_ICOTemplate(self):

        dispatched_events = []
        dispatched_logs = []

        def on_notif(evt):
            print(evt)
            dispatched_events.append(evt)

        def on_log(evt):
            print(evt)
            dispatched_logs.append(evt)
        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.on(SmartContractEvent.RUNTIME_LOG, on_log)

        output = Compiler.instance().load('example/demo/ICO_Template.py').default
        out = output.write()
#        print(output.to_s())


        tx, results, total_ops, engine = TestBuild(out, ['name', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), TOKEN_NAME)

        tx, results, total_ops, engine = TestBuild(out, ['symbol', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), TOKEN_SYMBOL)

        tx, results, total_ops, engine = TestBuild(out, ['decimals', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_DECIMALS)

        tx, results, total_ops, engine = TestBuild(out, ['totalSupply', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # deploy with wallet 2 should fail CheckWitness
        tx, results, total_ops, engine = TestBuild(out, ['deploy', '[]'], self.GetWallet2(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        tx, results, total_ops, engine = TestBuild(out, ['deploy', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # second time, it should already be deployed and return false
        tx, results, total_ops, engine = TestBuild(out, ['deploy', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        # now total supply should be equal to the initial owner amount
        tx, results, total_ops, engine = TestBuild(out, ['totalSupply', '[]'], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_INITIAL_AMOUNT)


        # now the owner should have a balance of the TOKEN_INITIAL_AMOUNT
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(TOKEN_OWNER)])], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_INITIAL_AMOUNT)
