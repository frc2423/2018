
from controllers.controller import Controller

class Simple_Controller(Controller):

    def __init__(self, default_value = 0):
        self.set_output('output', default_value)

    def calculate_outputs(self, dt):
        target = self.get_target('output')
        self.set_output('output', target)

    def set(self, value):
        self.set_target('output', value)

    def get(self):
        return self.get_output('output')