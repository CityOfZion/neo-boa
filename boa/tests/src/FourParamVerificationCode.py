from boa.blockchain.vm.Neo.Runtime import GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Runtime import Notify


OWNER = b'\xaf\x12\xa8h{\x14\x94\x8b\xc4\xa0\x08\x12\x8aU\nci[\xc1\xa5'


def Main(a, b, c, d):
    """

    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """
    print("Executing Four Param Verification code")
    trigger = GetTrigger()

    if trigger == Verification():

        print("Running verification")
        is_owner = CheckWitness(OWNER)
        Notify(is_owner)
        return is_owner

    print("runnig app routine")

    result = a + b - c + d

    Notify(result)

    return result
