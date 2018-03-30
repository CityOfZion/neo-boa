from boa.builtins import breakpoint


def another_module_method(m):

    thing = m * 2

    thing2 = thing + 32

    breakpoint()

    return thing2
