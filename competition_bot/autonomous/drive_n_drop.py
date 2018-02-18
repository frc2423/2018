import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.arms import Arms
from components.elevator import Elevator


class DriveNDrop(AutonomousStateMachine):
    MODE_NAME = 'DriveNDrop'
    DEFAULT = True
    DISABLED = True


    driveTrain = DriveTrain
    arms = Arms
    elevator = Elevator

    # /autonomous/DriveNDrop/robot_position
    robot_position = tunable('L')
    # /autonomous/DriveNDrop/action_if_left_switch
    action_if_left_switch = tunable('nothing')
    # /autonomous/DriveNDrop/action_if_right_switch
    action_if_right_switch = tunable('nothing')


    # actions: nothing, forward, drop
    @state(first=True)
    def selector(self):
        if self.get_action() == 'nothing':
            self.next_state('do_nothing')
        if self.get_action() == 'forward':
            self.next_state('drive_forward')
        if self.get_action() == 'drop':
            self.next_state('set_elevator_height')


    @state
    def drive_forward(self):

        if self.robot_position == self.get_switch_position():
            distance = 2
        else:
            distance = 5


        if self.driveTrain.get_left_distance() < distance:
            self.driveTrain.forward()
        elif self.get_action() == 'forward':
            self.next_state('do_nothing')
        elif self.get_action() == 'drop':
            self.next_state('turn')

    @state
    def set_elevator_height(self):
        self.elevator.set_height(8)
        self.next_state('drive_forward')

    @state()
    def turn(self):
        if self.robot_position() == 'L':
            if self.driveTrain.getAngle() < 90:
                self.driveTrain.turn_right()
            else:
                self.next_state('forward_again')
        elif self.robot_position() == 'R':
            if self.driveTrain.getAngle() > -90:
                self.driveTrain.turn_left()
            else:
                self.next_state('forward_again')

    @state()
    def forward_again(self):


        if self.robot_position == self.get_switch_position():
            distance = 2
        else:
            distance = 10

        if self.driveTrain.get_left_distance() < distance:
            self.driveTrain.forward()
        else:
            self.next_state('drop')
    @state()
    def turn_to_far_switch(self):
        if self.driveTrain.getAngle() < 180:
            if self.robot_position == "R":
                self.driveTrain.turn_left()
            else:
                self.driveTrain.turn_right()
        else:
            self.next_state('')

    @state
    def drive_forward_far_switch(self):
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

    def get_switch_position(self):
        game_data = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if len(game_data)>0:
            return game_data[0]


    def get_action(self):
        if self.get_switch_position() == 'L':
            return self.action_if_left_switch
        else:
            return self.action_if_right_switch

