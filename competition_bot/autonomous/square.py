import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain


class Square(AutonomousStateMachine):
    MODE_NAME = 'Square'
    DEFAULT = False

    driveTrain = DriveTrain

    @timed_state(duration=2, next_state='turn', first=True)
    def forward(self):
        '''This happens first'''
        self.driveTrain.forward()
        self.driveTrain.resetGyro()

    @state()
    def turn(self):
        '''This happens second'''
        self.driveTrain.turn()
        print(self.driveTrain.getAngle())
        if self.driveTrain.getAngle() >= 90:
            self.next_state('forward')




