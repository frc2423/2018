from magicbot import AutonomousStateMachine, tunable, timed_state


class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'DriveForward'
    DEFAULT = True

    @timed_state(duration=2, next_state='do_something', first=True)
    def dont_do_something(self):
        '''This happens first'''
        pass

    @timed_state(duration=5)
    def do_something(self):
        '''This happens second'''
        self.component2.do_something()
