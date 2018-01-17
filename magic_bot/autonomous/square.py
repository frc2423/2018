import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain


class Square(AutonomousStateMachine):
    MODE_NAME = 'Square'
    DEFAULT = True

    driveTrain = DriveTrain
    init_angle = driveTrain.getAngle()
    interval = 1

    @timed_state(duration=2, next_state='turn', first=True)
    def forward(self):
        '''This happens first'''
        self.driveTrain.forward()


    @state()
    def turn(self):
        '''This happens second'''
        self.driveTrain.turn()

        if self.driveTrain.getAngle() == self.interval * (self.init_angle + 90):
            self.next_state_now('forward')
            self.interval = self.interval + 1


