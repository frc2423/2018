import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain


class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'DriveForward'
    DEFAULT = False


    driveTrain = DriveTrain

    @timed_state(duration=3, next_state='do_nothing', first=True)
    def turn(self):
        '''This happens first'''
        self.driveTrain.forward()

    @timed_state(duration=5)
    def do_nothing(self):
        '''This happens second'''
        self.driveTrain.stop()