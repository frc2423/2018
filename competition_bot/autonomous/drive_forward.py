import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.direction_pid import Direction_Pid


class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'DriveForward'
    DEFAULT = False


    driveTrain = DriveTrain
    direction_pid = Direction_Pid

    @timed_state(duration=8, next_state='do_nothing', first=True)
    def forward(self):
        '''This happens first'''
        self.direction_pid.set_angle(0)
        self.driveTrain.set_speed(-.5)

    @timed_state(duration=5)
    def do_nothing(self):
        '''This happens second'''
        self.direction_pid.disable()
        self.driveTrain.stop()