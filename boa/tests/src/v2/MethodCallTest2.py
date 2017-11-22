from boa.code.builtins import range

def Main(a):


    # you can call a method that has no arguments like this
    # should I fix it? I kind of like it
    a = dostuff


    # even if a method doesnt return something, its result has to be
    # assigned otherwise stuff gets messed
    b = no_ret_val()


    for i in range(0, 13):

        print(i)

    return a






def dostuff():

 #   print("hello")

    j = 1 + 8

#    print(j)

    return j



def no_ret_val():


    b = 12

