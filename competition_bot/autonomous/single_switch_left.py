import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.direction_pid import Direction_Pid
from components.elevator import Elevator
from components.elevator_pid import Elevator_Pid
from components.arms import Arms


class SingleSwitchLeft(AutonomousStateMachine):
    MODE_NAME = 'Single Switch Left'

    driveTrain : DriveTrain
    direction_pid : Direction_Pid
    elevator : Elevator
    elevator_pid :Elevator_Pid
    arms : Arms

    @timed_state(duration=6, next_state='decide', first=True)
    def forward(self):
        '''This happens first'''
        self.direction_pid.set_angle(0)
        self.driveTrain.set_speed(-.6)

    @state
    def decide(self):
        self.direction_pid.disable()
        self.driveTrain.set_speed(0)

        if self.is_switch_left():
            self.next_state('increase_altitude')
        else:
            self.next_state('do_nothing')


    @state
    def increase_altitude(self):
        self.elevator_pid.set_height(2)
        if not self.elevator_pid.isEnabled():
            self.next_state('dump')

    @timed_state(duration=3, next_state='do_nothing')
    def dump(self):
        self.elevator.stop()
        self.arms.outtake()



    @state
    def do_nothing(self):
        self.elevator.stop()
        self.driveTrain.stop()
        self.arms.stop()


    def is_switch_left(self):
        game_data = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if len(game_data)>0:
            return game_data[0] == 'L'
        else:
            False