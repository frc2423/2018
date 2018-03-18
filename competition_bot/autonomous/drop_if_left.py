import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.arms import Arms
from components.elevator import Elevator


class DropIfLeft(AutonomousStateMachine):
    MODE_NAME = 'Drop If Left'
    DEFAULT = False

    arms : Arms
    driveTrain = DriveTrain
    elevator : Elevator

    @state(first=True)
    def init(self):
        self.driveTrain.stop()
        self.arms.stop()
        self.elevator.stop()
        self.next_state('forward')

    @timed_state(duration=8, next_state='determine_if_drop')
    def forward(self):
        '''This happens first'''
        self.driveTrain.forward()

    @state()
    def determine_if_drop(self):
        '''This happens second'''
        if self.get_switch_position() == 'L':
            self.driveTrain.stop()
            self.next_state('lift')
        else:
            self.driveTrain.stop()

    @timed_state(duration=.5, next_state='drop')
    def lift(self):
        self.elevator.up()

    @state()
    def drop(self):
        self.elevator.stop()
        self.arms.outtake()

    def get_switch_position(self):
        game_data = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if len(game_data)>0:
            return game_data[0]
