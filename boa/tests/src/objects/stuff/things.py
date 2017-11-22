
class Awesome():

    myname = 'NEO'

    mycount = 25

    def awesome_name(self):

        return self.myname


class MoreAwesome():

    thename = 'CoZ'

    intval = 32

    awesome = 42

    def add_thirteen_to_this(self, arg):

        m = arg + self.intval

        return m

    def multiply_nums(self, a, b):

        return a * b

    def multiply_by_awesome(self, a):

        return self.awesome * a


    def do_something_with_awesome(self, awe:Awesome):

        return awe.mycount + 3



    def make_awesome(self):

        awe = Awesome()

        return awe.mycount - 30