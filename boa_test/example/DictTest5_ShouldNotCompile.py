# tested


def Main():

    # this file should/does not compile

    d = {
        'a': 1,
        'b': {'a': 2},  # loading a dict inline will not compile
    }

    return d['b']
