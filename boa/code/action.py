
class action():

    method_name = None
    event_name = None
    event_args = None

    def __init__(self, blocks):
        self.method_name = blocks[-1].arg
        self.event_args = [instr.arg for instr in blocks[1:-2]]
        self.event_name = self.event_args[0]
