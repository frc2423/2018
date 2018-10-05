import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.direction_pid import Direction_Pid
from components.arms import Arms
from components.elevator import Elevator
from components.elevator_pid import Elevator_Pid


class LeftSideSequence(AutonomousStateMachine):
    MODE_NAME = 'LeftSideSequence'
    DEFAULT = True


    driveTrain = DriveTrain
    direction_pid = Direction_Pid
    arms = Arms
    elevator = Elevator
    elevator_pid = Elevator_Pid

    @state(first = True)
    def stopped_at_position_1(self):
        print("drive forward")
        self.driveTrain.reset_odometry()
        self.next_state('driving_to_posiion_2')


    @state()
    def driving_to_posiion_2(self):
        # state body
        self.driveTrain.calculate_odometry()
        at_position = self.driveTrain.drive_to(0, 8)
        print('position: %1.2f, %1.2f' % self.driveTrain.get_position())
        print('angle: %1.0f' % self.driveTrain.get_angle_from_encoders())
        #print("driving forward!", )

        # transition
        if at_position:
            if self.get_switch_side() is 'L':
                self.next_state('driving_to_position_6')
            else:
                self.next_state("driving_to_position_3")


    @state()
    def driving_to_position_3(self):
        self.driveTrain.calculate_odometry()
        at_position = self.driveTrain.drive_to(0,16)

        if at_position:
            self.next_state("driving_to_position_4")

    @state()
    def driving_to_position_4(self):
        self.driveTrain.calculate_odometry()
        at_position = self.driveTrain.drive_to(14, 16)

        if at_position:
            self.next_state("driving_to_position_5")

    @state()
    def driving_to_position_5(self):
        self.driveTrain.calculate_odometry()
        at_position = self.driveTrain.drive_to(14, 12)

        if at_position:
            self.next_state("drop")

    @state()
    def driving_to_position_6(self):
        self.driveTrain.calculate_odometry()
        at_position = self.driveTrain.drive_to(4, 8)

        if at_position:
            self.next_state("drop")


        pass

    @state()
    def drop(self):
        self.driveTrain.calculate_odometry()
        self.elevator_pid.set_height(2)
        if self.elevator_pid.get_height() > 1.8:
            self.arms.outtake()



    @timed_state(duration=5)
    def do_nothing(self):
        '''This happens second'''
        self.direction_pid.disable()
        self.driveTrain.stop()

    def get_switch_side(self):
        game_data = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if len(game_data)>0:
            return game_data[0]
        else:
            return 'L'