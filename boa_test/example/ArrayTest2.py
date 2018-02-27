
def Main():

    # lets have fun with strings

    m = ['awesome', 'fun', 'cool', 'neo']

    q = m[1]

    m2 = [1, 'wat', 'huzzah', 8]

    q2 = m[3]

    m3 = [b'\x00', b'\x20', b'\xff', b'\xa0']

    q3 = m3[3]

    m4 = [bytearray(b'\x0f\xf0'), bytearray(b'\xff\xff')]

    # this doesnt work
    q4 = m4[1]

    h = [2, m2[1], 'hello']

    j = h[1]

    print(j)  # prints 'wat'

    return q3
