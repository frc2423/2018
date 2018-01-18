import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain


class Square(AutonomousStateMachine):
    MODE_NAME = 'Square'
    DEFAULT = True

    driveTrain = DriveTrain
    def __init__(self):
        #self.init_angle = self.driveTrain.getAngle()
        self.interval = 1


    @timed_state(duration=2, next_state='turn', first=True)
    def forward(self):
        '''This happens first'''
        self.driveTrain.forward()


    @state()
    def turn(self):
        '''This happens second'''
        self.driveTrain.turn()

        if self.driveTrain.getAngle() >= (self.interval * 90):
            self.next_state_now('forward')
            self.interval = self.interval + 1
            self.done()


