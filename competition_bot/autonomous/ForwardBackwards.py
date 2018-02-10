import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain



class ForwardBackwards(AutonomousStateMachine):
    MODE_NAME = 'Forward-Backwards'
    DEFAULT = False


    driveTrain = DriveTrain

    @timed_state(duration=3, next_state='backward', first=True)
    def forward(self):
        '''This happens first'''
        self.driveTrain.forward()

    @timed_state(duration=3, next_state='forward')
    def backward(self):
        '''This happens second'''
        self.driveTrain.backward()
        #self.next_state('forward')
        #self.done()