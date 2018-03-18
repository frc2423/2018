import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain


class DoNothing(AutonomousStateMachine):
    MODE_NAME = 'DoNothing'
    DEFAULT = False


    driveTrain = DriveTrain

    @state( first=True)
    def do_nothing(self):
        '''This happens first'''
        self.driveTrain.stop()
