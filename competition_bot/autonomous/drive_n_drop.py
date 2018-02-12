import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.arms import Arms



class DriveNDrop(AutonomousStateMachine):
    MODE_NAME = 'DriveNDrop'
    DEFAULT = True


    driveTrain = DriveTrain
    arms = Arms

    @timed_state(duration=3, next_state='turn', first=True)
    def drive_forward(self):
        self.driveTrain.forward()

    @state()
    def turn(self):
        if self.driveTrain.getAngle() < 90:
            self.driveTrain.turn()
        else:
            self.next_state('drop')

    @timed_state(duration=2)
    def drop(self):
        self.arms.outtake()