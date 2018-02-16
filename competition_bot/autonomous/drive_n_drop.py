import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.arms import Arms
from components.elevator import Elevator


class DriveNDrop(AutonomousStateMachine):
    MODE_NAME = 'DriveNDrop'
    DEFAULT = True


    driveTrain = DriveTrain
    arms = Arms
    elevator = Elevator

    @state(first=True)
    def drive_forward(self):
        self.elevator.set_height(8)
        if self.driveTrain.get_left_distance() < 10:
            self.driveTrain.forward()
        else:
            self.next_state('turn')

    @state()
    def turn(self):
        if self.driveTrain.getAngle() < 90:
            self.driveTrain.turn()
        else:
            self.next_state('forward_again')

    @state()
    def forward_again(self):
        if self.driveTrain.get_left_distance() < 2:
            self.driveTrain.forward()
        else:
            self.next_state('drop')

    @timed_state(duration=2, next_state='do_nothing')
    def drop(self):
        self.arms.outtake()

    @state()
    def do_nothing(self):
        pass